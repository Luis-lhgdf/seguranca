# Nginx e TLS

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md).

**Cobre:** protocolos e certificados, renovação, redirects HTTP→HTTPS e www→apex, esqueleto do
Nginx (zonas de rate limit, locations, uploads, dotfiles, honeypot), armadilhas (`add_header`,
`set_real_ip_from`, `proxy_pass`).
**Aplica-se quando:** há Nginx (ou outro proxy reverso — adaptar) sob seu controle. Em
hospedagem gerenciada, verificar só o lado externo (TLS, redirects, headers).

| Arquivo | Conteúdo |
|---|---|
| [tls-e-certificados.md](tls-e-certificados.md) | protocolos, Certbot, redirects, como verificar |
| [configuracao-nginx.md](configuracao-nginx.md) | esqueleto, armadilhas, `nginx -T` |
| [referencias.md](referencias.md) | fontes oficiais |
| [checklist.md](checklist.md) | itens `SEC-WEB-*` |

Headers e CSP: [headers](../headers/README.md). Rate limit: [rate-limit](../rate-limit/README.md).
