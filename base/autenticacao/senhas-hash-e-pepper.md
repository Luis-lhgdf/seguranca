# Senhas: Argon2id, salt e pepper

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/preço/CVE, confirme na fonte oficial antes de aplicar.

> Fonte: [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html).
> Abaixo, duas configurações usadas na prática (loja virtual com conta de cliente e backoffice;
> painel com operador único), com parâmetros diferentes — ambas no mínimo recomendado ou acima.

## 1. Por que Argon2id, e não bcrypt

> *"Use **Argon2id** with a minimum configuration of 19 MiB of memory, an iteration count of 2,
> and 1 degree of parallelism."*
> *"The bcrypt password hashing function should **only be used for password storage in legacy
> systems** where Argon2 and scrypt are not available."*

⚠️ **Armadilha do bcrypt:** limite de **72 bytes** de entrada — senha mais longa é **truncada em
silêncio** (aceita 100 caracteres de gerenciador de senha e valida só os 72 primeiros).

Proibido para senha: texto puro, MD5/SHA-1/SHA-256 rápidos (com ou sem salt), cifra reversível,
"senha como token" (SHA-256 da senha usado como token de sessão — determinístico, permite
pass-the-hash e persistência indefinida).

## 2. Parâmetros do Argon2id

A OWASP lista cinco configurações equivalentes em segurança (troca CPU por RAM):

| memória | iterações (t) | paralelismo (p) |
|---|---|---|
| 47104 KiB (46 MiB) | 1 | 1 |
| **19456 KiB (19 MiB)** — mínimo citado no texto | **2** | **1** |
| 12288 KiB (12 MiB) | 3 | 1 |
| 9216 KiB (9 MiB) | 4 | 1 |
| 7168 KiB (7 MiB) | 5 | 1 |

| Cenário | Configuração | Observação |
|---|---|---|
| Padrão recomendado (mínimo OWASP, explícito) | `m=19456, t=2, p=1` (explícito) | o mínimo recomendado; 19 MiB **por hash simultâneo** (20 logins = ~380 MiB de pico) — medir na VPS; se apertar, `m=12288, t=3` é equivalente |
| Alternativa usada na prática (painel de operador único) | defaults do `argon2-cffi` 25.1.0: `m=65536 (64 MiB), t=3, p=4`, `hash_len=32`, `salt_len=16` | 3,4× a memória e 1,5× as iterações do mínimo. Medido: ~43 ms em máquina de dev; **226 ms na VPS de 1 vCPU**, pico de 320 MiB no pior caso. `p=4` com menos vCPUs serializa (mais latência, mesma segurança) |

- **Medir na VPS de produção** antes de fechar: latência de login e pico de memória sob concorrência realista (limitada pelo rate limit).
- **Salt**: por senha, aleatório, gerado pela biblioteca. Nunca inventar salt.
- **Coluna**: a string PHC tem ~97 caracteres (`$argon2id$v=19$m=…,t=…,p=…$<salt>$<hash>`); `VARCHAR(255)`/`TEXT` sobra. Subir o custo não aumenta o tamanho de forma relevante.
- Biblioteca de referência em Python: **`argon2-cffi`** (MIT, ligada à libargon2 em C).

## 3. Rehash automático

> *"One key advantage of having a work factor is that it can be increased over time."*

No login bem-sucedido, se o hash guardado usa parâmetros abaixo do atual, re-hashear e regravar —
é a única janela em que a senha em claro existe. `argon2-cffi`: `check_needs_rehash()`.

## 4. Pepper — o que resolve e o que cobra

**Salt** fica junto do hash (público por desenho). **Pepper** é segredo do servidor, **fora do banco**:

> *"the pepper should not be public and **should not be stored along with the generated hash**."*

- **Cobre:** vazamento **apenas do banco** (dump por SQLi, backup mal guardado, leitura indevida) — os hashes ficam inúteis para ataque offline.
- **Não cobre:** comprometimento do servidor da aplicação (quem lê o `.env` tem o pepper).

### 4.1 A ordem correta: pré-hash com HMAC

```
argon2id( hmac_sha256(chave=PEPPER, msg=senha) )
```

🔴 **Erro clássico (armadilha comum):** `hmac(PEPPER, argon2id(senha))`
(pós-hash) **quebra todos os logins** — o Argon2 sorteia salt novo a cada chamada e o guarda na
string PHC; guardando só o HMAC, o salt se perde e não há como reconferir. O argumento contra
"pré-hash" vale para **concatenar** `pepper + senha`, não para HMAC: a saída é fixa (64 hex) e o
limite de 72 bytes é do bcrypt, não do Argon2.

### 4.2 O custo que precisa estar escrito antes do primeiro cadastro

> *"Peppers cannot be changed without knowledge of a user's password."*

- **Onde vive:** cofre/HSM é o ideal; em VPS única, o `.env` (permissão restrita) é decisão consciente — registrar como decisão, não esquecimento, e revisitar se houver cofre.
- **Backup do pepper separado do backup do banco.** Perder o pepper = ninguém loga, sem recuperação. Guardar junto do dump anula o propósito.
- **Versionar** (`pepper_versao SMALLINT` na linha do usuário): permite duas versões na transição e migrar cada usuário no login seguinte. *Com um único usuário (ex.: painel de operador único), pode ser considerado desnecessário* — mas então o procedimento de rotação precisa estar escrito: gerar o hash novo com o pepper novo fora da aplicação → trocar a variável → reiniciar. Atenção: se o bootstrap do admin se desliga quando já há usuário, trocar o pepper sem plano tranca o operador fora (só se recupera mexendo direto no banco).
- **Segredos distintos por ambiente.** Pepper e chave do JWT iguais em dev e produção = hash/token de dev válido em produção.
- Nunca logar, nunca mandar ao Sentry, nunca commitar.
- Validador na subida: recusar placeholder (`TROQUE…`) e menos de 32 caracteres. Gerar com `secrets.token_urlsafe(64)` **no servidor**.

## 5. Fluxo de login seguro

1. Buscar por identificador. **Usuário inexistente, conta bloqueada e conta inativa** passam todos por `dummy_verify` (verify contra um hash isca pré-computado) — mesmo custo de CPU, sem oráculo de tempo. *Achado típico em auditoria:* o ramo "conta inativa" retornava sem `dummy_verify` (~0 ms × ~43 ms).
2. Comparação pela biblioteca (tempo constante); segredo comparado em Python só com `hmac.compare_digest`.
3. Mensagem **única** para toda falha ("Credenciais inválidas").
4. Senha errada incrementa contador da conta; no teto, lockout temporário (ex.: 10 falhas → 15 min). ⚠️ Lockout por conta é vetor de DoS contra o dono (OWASP: *"care must be taken to prevent it from being used to cause a denial of service"*) — manter curto, não escalonar, e somar rate limit por IP na borda.
5. Persistir o contador **antes** de levantar o 401 (commit antes da exceção).
6. Rehash se necessário (§3).

## 6. Política de senha (NIST SP 800-63B)

- Mínimo longo (ex.: **12** para admin), máximo generoso (ex.: 128 — evita payload de 1 MB no Argon2).
- Tamanho > complexidade; sem troca periódica forçada; checar contra lista de senhas vazadas (HIBP k-anonymity).
- No login, `min_length=1` — validar tamanho no login seria oráculo inútil.
- Trocar senha **revoga todas as sessões** e, se houver, "esquece" aparelhos confiáveis; notificar o titular.

## 7. Onde mais aplicar

Toda senha do sistema: cliente, backoffice/SAC, admin. **Admin exige MFA além da senha.**
Nunca devolver `senha_hash` em resposta de API (schema de saída explícito).

## 8. Testes mínimos (baratos e de alto valor)

- [ ] mesma senha em dois usuários → hashes diferentes (prova o salt);
- [ ] hash **não confere** se o pepper mudar (prova que o pepper entra no cálculo; `VerifyMismatchError`);
- [ ] hash começa com `$argon2id$` e traz os parâmetros esperados;
- [ ] rehash acontece ao mudar parâmetro;
- [ ] tempo de resposta equivalente para usuário inexistente/bloqueado/inativo.

Sem eles, uma refatoração remove o `_pepper()` e nada acusa.
