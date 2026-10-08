# Rate limit, carga e abuso

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md).

**Cobre:** por que limite por IP derruba usuário (página pesada, prefetch, CGNAT, SSR), isenção de
assets, IP × identidade, modo observar, camadas (CDN, Nginx, app, fail2ban), IP real atrás de
proxy, teste de regressão e de carga.
**Aplica-se quando:** sempre que há rota pública ou login.

| Arquivo | Conteúdo |
|---|---|
| [camadas-e-cgnat.md](camadas-e-cgnat.md) | incidente, causas, regras, camadas, testes |
| [referencias.md](referencias.md) | fontes oficiais e mapeamento Top 10 / ASVS / WSTG |
| [checklist.md](checklist.md) | itens `SEC-RL-*` (com nível ASVS e mapeamento) |

Limites específicos: login em [autenticacao](../autenticacao/login-e-mfa.md), mensagens em
[mensageria](../mensageria/README.md), cartão em [pagamentos](../pagamentos/card-testing.md).
