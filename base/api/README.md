# API e endpoints

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md).

**Cobre:** anatomia de endpoint seguro, bateria de entrada (bytes, Unicode, injeção pelo destino,
forma, abuso, saída), autorização (IDOR/BOLA/BFLA), exposição de dados, mass assignment, CORS,
`/docs`, integrações entre serviços e SSRF.

**Aplica-se quando:** o projeto tem backend que recebe requisições (REST, RPC, server actions).

| Arquivo | Conteúdo |
|---|---|
| [endpoint-seguro.md](endpoint-seguro.md) | anatomia em 8 passos, bateria de testes, checklist de revisão de diff |
| [autorizacao-e-exposicao.md](autorizacao-e-exposicao.md) | IDOR/BOLA, autorização por objeto, `response_model`, mass assignment, CORS, integrações |
| [ssrf.md](ssrf.md) | saída segura, CGNAT, NAT64, redirects, tracker de IP |
| [referencias.md](referencias.md) | fontes oficiais e mapeamento Top 10 / ASVS / WSTG |
| [checklist.md](checklist.md) | itens `SEC-API-*` (com nível ASVS e mapeamento) |

Relacionados: [upload](../upload/README.md) · [rate-limit](../rate-limit/README.md) ·
[pagamentos](../pagamentos/README.md) (webhooks) · [banco](../banco/README.md) (SQLi).
