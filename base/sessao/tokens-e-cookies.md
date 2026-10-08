# Sessão: tokens, cookies, expiração e revogação

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/CVE, confirme na fonte oficial antes de aplicar.

## 1. Padrão de referência

| Item | Valor | Por quê |
|---|---|---|
| Access token | JWT **HS256**, **15 min**, claims `sub`, `type`, `iat`, `exp` | curto limita o estrago de roubo |
| Privilégio no token | **nenhum** — autorização relida do banco a cada request | revogar permissão tem efeito imediato |
| Decodificação | `algorithms` fixo (sem *alg confusion*); `exp`/`type` validados | ASVS V9 |
| Refresh | opaco, `secrets.token_urlsafe(48)`; banco guarda **só o SHA-256**; **7 dias** | SHA-256 sobre token aleatório de 48 bytes é uso correto |
| Rotação | a cada uso; token **já revogado** reapresentado → **revoga a família inteira** | detecção de roubo |
| Cookies | access `HttpOnly`, `path=/api`; refresh `HttpOnly`, `path` estreito (`/api/admin/auth`); `Secure` fora de dev; `SameSite=Lax` | refresh não viaja para as demais rotas |
| Troca de senha/privilégio | revoga todas as sessões | |
| Expurgo | purga de tokens expirados/revogados **agendada** (timer/cron) | comando que existe mas nunca roda não conta |

Alternativa usada na prática: sessão opaca no Redis; logout apaga a chave e `/eu` vira 401.

## 2. Regras gerais

- Token de sessão: CSPRNG, ≥ 128 bits (ASVS V7.2.3). Nunca derivado de credencial (SHA-256 da senha como token = pass-the-hash e sessão eterna).
- Cookie: `Secure`, `HttpOnly`, `SameSite` (Lax/Strict); prefixo `__Host-` quando possível (ASVS V3.3.x). Nenhum token em `localStorage`.
- Logout invalida **no servidor**. Gap aceito e documentado: JWT sem `jti`/denylist continua válido até expirar após logout → só com TTL curto.
- Cookies no **apex** com `www → apex` forçado (evita par de hosts e cookie CSRF ilegível).
- Segredo de assinatura (`SECRET_KEY`) ≥ 32 chars, recusado se placeholder, **distinto por ambiente** e distinto do pepper. Trocá-lo é barato (invalida só access tokens).

## 3. CSRF

- Double-submit: cookie CSRF legível por JS (`httponly=False`, `path=/`) + header `X-CSRF-Token`, comparados com `hmac.compare_digest`; isenta só GET/HEAD/OPTIONS; nega se faltar cookie **ou** header.
- Declarado no **router inteiro** de toda área mutável (rota nova nasce protegida).
- Exceções conscientes, escritas no código: login (sem sessão ainda), logout (SameSite já barra POST cross-site; exigir CSRF poderia prender o operador), setup fail-closed.
- `SameSite=Lax` ajuda, mas não é a defesa declarada.
- Ações públicas com efeito colateral (contadores): conferir `Origin`/host do `Referer` contra a allowlist — barra disparo cross-site **em navegador**; `curl` forja `Origin`, então somar rate limit.
- ⚠️ Cadeia perigosa: XSS na mesma origem lê o cookie CSRF e faz mutação autenticada → CSP e escape são pré-requisito ([headers](../headers/README.md)).

## 4. Step-up e aparelhos

Ver [autenticacao/login-e-mfa.md](../autenticacao/login-e-mfa.md#3-step-up-login-adaptativo).
