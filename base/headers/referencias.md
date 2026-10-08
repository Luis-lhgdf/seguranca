# Referências — Cabeçalhos, CSP e XSS

> **Revisado em:** 2026-10-07.

- OWASP HTTP Headers CS — https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
- OWASP Content Security Policy CS — https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html
- OWASP XSS Prevention CS — https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
- OWASP DOM based XSS Prevention CS — https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html
- OWASP CSV Injection — https://owasp.org/www-community/attacks/CSV_Injection
- OWASP ASVS 5.0 — V1.2/V1.3 (encoding), V3.2/V3.4 (frontend), V14.3 (cache/storage) — https://github.com/OWASP/ASVS
- MDN — CSP — https://developer.mozilla.org/docs/Web/HTTP/CSP · SRI — https://developer.mozilla.org/docs/Web/Security/Subresource_Integrity
- Next.js — CSP com nonce — https://nextjs.org/docs/app/guides/content-security-policy
- Cloudflare Turnstile — CSP — https://developers.cloudflare.com/turnstile/reference/content-security-policy/
- Nginx — `add_header` (herança) — https://nginx.org/en/docs/http/ngx_http_headers_module.html#add_header
- Google CSP Evaluator — https://csp-evaluator.withgoogle.com/ · Mozilla Observatory — https://developer.mozilla.org/en-US/observatory · securityheaders.com
- HSTS preload — https://hstspreload.org/

## Mapeamento oficial

Tabela item a item em [checklist/mapeamentos.md](../../checklist/mapeamentos.md#7-cabeçalhos-csp-e-xss-sec-nav).

- OWASP Top 10:2025 — [A02 Security Misconfiguration](https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/) · [A03 Software Supply Chain Failures](https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/) · [A04 Cryptographic Failures](https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/) · [A05 Injection](https://owasp.org/Top10/2025/A05_2025-Injection/) · [A08 Software or Data Integrity Failures](https://owasp.org/Top10/2025/A08_2025-Software_or_Data_Integrity_Failures/)
- OWASP ASVS 5.0 — V1 Encoding and Sanitization · V3 Web Frontend Security · V13 Configuration · V14 Data Protection — https://github.com/OWASP/ASVS/tree/v5.0.0/5.0/en
- OWASP WSTG v4.2 — [INFO Coleta de informação](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/) · [CONF Configuração e implantação](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/) · [ATHN Autenticação](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/04-Authentication_Testing/) · [INPV Validação de entrada](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/) · [CLNT Lado do cliente](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/11-Client-side_Testing/)
