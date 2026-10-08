# Referências — Rate limit

> **Revisado em:** 2026-10-07.

- OWASP API4:2023 Unrestricted Resource Consumption — https://api-security.owasp.org/editions/2023/en/0xa4-unrestricted-resource-consumption
- OWASP — Blocking Brute Force Attacks — https://community.owasp.org/controls/Blocking_Brute_Force_Attacks
- OWASP ASVS 5.0 — V2.4.1 (anti-automação) — https://github.com/OWASP/ASVS
- RFC 6585 §4 (429, `Retry-After`) — https://www.rfc-editor.org/rfc/rfc6585.html
- Nginx — `limit_req` — https://nginx.org/en/docs/http/ngx_http_limit_req_module.html · `realip` — https://nginx.org/en/docs/http/ngx_http_realip_module.html
- Cloudflare — rate limiting rules — https://developers.cloudflare.com/waf/rate-limiting-rules/ · IPs da Cloudflare — https://www.cloudflare.com/ips/ · restaurar IP do visitante — https://developers.cloudflare.com/support/troubleshooting/restoring-visitor-ips/restoring-original-visitor-ips/
- redis.io — rate limiters — https://redis.io/tutorials/howtos/ratelimiting/
- Stripe — rate limiters — https://stripe.com/blog/rate-limiters
- slowapi — https://slowapi.readthedocs.io/
- k6 — https://grafana.com/docs/k6/latest/
- Next.js — prefetch do `<Link>` — https://nextjs.org/docs/app/api-reference/components/link#prefetch

## Mapeamento oficial

Tabela item a item em [checklist/mapeamentos.md](../../checklist/mapeamentos.md#11-rate-limit-carga-e-abuso-sec-rl).

- OWASP Top 10:2025 — [A02 Security Misconfiguration](https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/) · [A06 Insecure Design](https://owasp.org/Top10/2025/A06_2025-Insecure_Design/) · [A10 Mishandling of Exceptional Conditions](https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/)
- OWASP ASVS 5.0 — V2 Validation and Business Logic · V4 API and Web Service · V6 Authentication · V15 Secure Coding and Architecture · V16 Security Logging and Error Handling — https://github.com/OWASP/ASVS/tree/v5.0.0/5.0/en
- OWASP WSTG v4.2 — [BUSL Lógica de negócio](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/10-Business_Logic_Testing/)
- OWASP API Security Top 10:2023 — API4 Unrestricted Resource Consumption · API6 Unrestricted Access to Sensitive Business Flows — https://owasp.org/API-Security/editions/2023/en/0x11-t10/
