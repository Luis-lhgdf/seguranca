# Cabeçalhos, CSP e XSS (navegador)

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md).

**Cobre:** cabeçalhos de segurança, `Cache-Control` em resposta sensível, armadilha do
`add_header` do Nginx, CSP (implantação, nonce, SRI), XSS e escape por destino.
**Aplica-se quando:** o projeto serve HTML a navegador (praticamente sempre).

| Arquivo | Conteúdo |
|---|---|
| [cabecalhos-de-seguranca.md](cabecalhos-de-seguranca.md) | conjunto mínimo, `no-store`, Nginx, como verificar |
| [csp.md](csp.md) | implantação Report-Only → enforcing, nonce, diretivas, SRI |
| [xss-e-escape.md](xss-e-escape.md) | escape por destino, caso JSON-LD, sinks |
| [referencias.md](referencias.md) | fontes oficiais |
| [checklist.md](checklist.md) | itens `SEC-NAV-*` |

Cookies e CSRF: [sessao](../sessao/README.md). TLS: [nginx-tls](../nginx-tls/README.md).
