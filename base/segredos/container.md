# Segredos no contêiner: por que `docker inspect` mostra tudo

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/CVE, confirme na fonte oficial antes de aplicar.

Aplica-se a projetos com **Docker/Compose**. Medido em contêiner descartável.

## 1. O problema

```bash
docker inspect <conteiner> --format '{{range .Config.Env}}{{println .}}{{end}}'
```

Com `env_file: [.env]`, qualquer pessoa com acesso ao daemon Docker lê **todos** os segredos
(exemplo medido numa aplicação com API + worker: 14 variáveis com nome de segredo na API, 12 no worker; o Postgres, com `*_FILE`, 0).

## 2. `.env` guarda bem, mas entrega mal

| O `.env` serve para | Funciona? |
|---|---|
| **Guardar** o segredo fora do git | ✅ |
| **Entregar** o segredo ao processo como variável de ambiente | ❌ — legível em `docker inspect`, `/proc/<pid>/environ`, `env` de qualquer processo do contêiner, logs de crash |

> *"Environment variables are often available to all processes... They can also be printed in logs when debugging errors without your knowledge."* — docs.docker.com

## 3. `secrets:` do Compose (não precisa de Swarm)

```yaml
secrets:
  jwt_secret:
    file: ./secrets/jwt_secret.txt   # nunca versionado
services:
  api:
    secrets: [jwt_secret]            # vira arquivo em /run/secrets/jwt_secret
```

- O valor vira **arquivo** montado com permissão restrita, não variável. O formato `.txt` não importa — o que protege é **como** chega.
- pydantic-settings lê nativamente: `SettingsConfigDict(secrets_dir="/run/secrets")`. Imagens oficiais aceitam `*_FILE` (ex.: `POSTGRES_PASSWORD_FILE`).
- Só os **segredos** saem do `.env`; porta, ambiente, URLs ficam.

## 4. 🔴 Armadilha medida: precedência

pydantic-settings: **variável de ambiente > `.env` > `secrets_dir`**. Com o mesmo nome nos dois
lugares, vale o ambiente e o `inspect` continua vazando. As duas metades são obrigatórias:
1. `secrets_dir` no Settings;
2. o segredo **sai** do `.env` injetado pelo Compose.
Feito pela metade, dá falsa sensação de segurança.

## 5. O que protege e o que não

| Ataque | `secrets:` protege? |
|---|---|
| `docker inspect` por quem acessa o daemon | ✅ |
| segredo impresso em log de crash | ✅ ajuda muito |
| variável herdada por processo filho | ✅ |
| quem já está **dentro** do contêiner | ❌ (lê `/run/secrets`) |
| root no host | ❌ |
| segredo commitado | ❌ (isso é gitleaks) |

Defesa em profundidade, não muralha. Ganho real é em **produção** (mais gente com acesso ao host);
fazer junto com a configuração da VPS. Custo: onboarding (um script que gera os arquivos).
