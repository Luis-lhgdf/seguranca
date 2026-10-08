# Autenticação, cadastro e recuperação de conta

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md).

**Cobre:** armazenamento de senha, login, lockout, MFA, step-up, cadastro (contas falsas,
verificação, enumeração), "esqueci a senha" e telefone como 2º fator.

**Aplica-se quando:** o projeto tem qualquer login (mesmo um painel de um operador só).
Cadastro, recuperação e telefone só se esses fluxos existirem — senão, N/A com motivo.

| Arquivo | Conteúdo |
|---|---|
| [senhas-hash-e-pepper.md](senhas-hash-e-pepper.md) | Argon2id, parâmetros, rehash, pepper (ordem HMAC), fluxo de login, testes |
| [login-e-mfa.md](login-e-mfa.md) | rate limit/lockout, MFA, step-up, reautenticação, painel de operador único, login social |
| [cadastro-e-enumeracao.md](cadastro-e-enumeracao.md) | OAT-019, verificar antes de liberar função, e-mail sequestrado, enumeração |
| [recuperacao-de-senha.md](recuperacao-de-senha.md) | fluxo de referência, PIN × link, palpites acumulados, canal × 2º fator |
| [telefone-em-varias-contas.md](telefone-em-varias-contas.md) | troca de número, número reciclado, mesmo número em várias contas |
| [referencias.md](referencias.md) | fontes oficiais |
| [checklist.md](checklist.md) | itens `SEC-AUTH-*` |

Relacionados: [sessao](../sessao/README.md) · [captcha](../captcha/README.md) ·
[mensageria](../mensageria/README.md) · [rate-limit](../rate-limit/README.md).
