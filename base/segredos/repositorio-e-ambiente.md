# Segredos: repositório, bundle, ambientes e servidor

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/CVE, confirme na fonte oficial antes de aplicar.

## 1. Fora do git

- `.gitignore` cobre `.env`, `.env.*` (exceto `!.env.example`), `*.key`, `*.pem`, `*.p12`, `secrets/`, `private_uploads/`.
- `.env.example` versionado só com placeholder (`TROQUE_ESTE_VALOR`) que o validador **recusa** na subida.
- Varrer o **histórico**, não só a árvore: `gitleaks detect --source $REPO` (ou `git log --all --diff-filter=A --name-only | grep -E '\.env$'`); trufflehog valida se a credencial ainda funciona.
- Segredo vazado no histórico: **rotacionar** (apagar o commit não basta).
- Commits de "teste" e código gerado por assistente de IA são fonte comum de vazamento → gitleaks no CI e/ou pre-commit.
- ⚠️ Armadilha comum: `.gitignore` com regra ampla `.github` → todo workflow novo era descartado em silêncio pelo `git add` (os antigos só sobreviviam por já estarem no índice). Conferir com `git check-ignore -v --no-index .github/workflows/novo.yml`.

## 2. Fora do front

- Só variáveis públicas por desenho no bundle (`NEXT_PUBLIC_*`, `VITE_*`) — e conferir que nenhuma é segredo.
- Sitekey de captcha é pública; secret não. `merchant_key` do gateway só no backend.
- Verificar o bundle gerado: `grep -rEo "(sk_live|secret|token|password|api[_-]?key)[^\"']{0,40}" .next/static dist/ build/`.
- Nunca: chave AES no cliente, credencial de admin no JS, chave privada de gateway no código.

## 3. Validação na subida (fail-closed)

- Recusar placeholder e segredo curto (< 32 chars) para chave de assinatura e pepper — a app **não sobe**.
- Recusar `CORS=*`, chave de captcha de teste e `localhost` nos hostnames em produção.
- Recusar credencial de serviço default (ASVS V13.2.3).

## 4. Por ambiente

- **Segredos distintos** em dev, staging e produção (JWT/pepper iguais = token de dev vale em produção). Gerar no próprio servidor: `python -c "import secrets; print(secrets.token_urlsafe(64))"`.
- Sem staging, o risco vira o `.env` local do desenvolvedor — confirmar que não copia o de produção.

## 5. No servidor

- `.env` com permissão restrita: `640` (dono do deploy, grupo da conta de serviço) ou `600`; diretório não legível por outros.
- Variáveis de ambiente vazam por `/proc/<pid>/environ`, `docker inspect`, dumps de crash — ver [container.md](container.md).
- Cofre (Vault, AWS Secrets Manager) é o ideal (ASVS V13.3.1); em VPS única, `.env` restrito é decisão consciente a registrar.
- **Rotação** com cronograma para segredos críticos (ASVS V13.3.4, L3). Custo de cada um: chave JWT = barato (derruba sessões curtas); pepper = exige plano (ver [autenticacao](../autenticacao/senhas-hash-e-pepper.md#42-o-custo-que-precisa-estar-escrito-antes-do-primeiro-cadastro)); credencial de gateway/WhatsApp = coordenar com o fornecedor.
- Token de bootstrap (`SETUP_TOKEN`) **esvaziado** depois do uso.

## 6. CI/CD

- Segredos de deploy em GitHub Secrets (`VPS_HOST`, `VPS_USER`, `VPS_SSH_KEY`), nunca no workflow.
- Chave SSH do CI com **forced-command** no `authorized_keys` (`command="/opt/app/scripts/ci-deploy.sh",no-port-forwarding,no-pty ...`) — mesmo vazada, não dá shell.
- Credenciais de integração com privilégio mínimo e token de curta duração quando possível.

## 7. Pessoas

Nunca colar `.env`, token de setup ou chave em chat, ticket ou ferramenta de IA.
