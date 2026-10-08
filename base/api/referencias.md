# Referências — API

> **Revisado em:** 2026-10-07.

- OWASP API Security Top 10 (2023) — https://owasp.org/www-project-api-security/ (API1 BOLA, API3 propriedade, API4 recursos, API6 mass assignment)
- OWASP Authorization CS — https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- OWASP Mass Assignment CS — https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html
- OWASP SSRF Prevention CS — https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html
- OWASP Input Validation CS — https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
- OWASP ASVS 5.0 — V1.2, V1.3.6, V2.2, V4, V8, V13.1–V13.2, V15.3 — https://github.com/OWASP/ASVS
- OWASP WSTG — https://owasp.org/www-project-web-security-testing-guide/
- PayloadsAllTheThings (IDOR, mass assignment, SSRF) — https://github.com/swisskyrepo/PayloadsAllTheThings
- Pydantic — `extra="forbid"` — https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.extra
- FastAPI — desligar docs (`docs_url=None`, `openapi_url=None`) — https://fastapi.tiangolo.com/tutorial/metadata/
- Python `ipaddress` (`is_global`, `is_private`) — https://docs.python.org/3/library/ipaddress.html
- Next.js CVE-2025-29927 (bypass de middleware) — https://github.com/advisories/GHSA-f82v-jwr5-mffw
- Next.js `images.remotePatterns` — https://nextjs.org/docs/app/api-reference/components/image#remotepatterns

## Mapeamento oficial

Tabela item a item em [checklist/mapeamentos.md](../../checklist/mapeamentos.md#5-api-e-endpoints-sec-api).

- OWASP Top 10:2025 — [A01 Broken Access Control](https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/) · [A02 Security Misconfiguration](https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/) · [A03 Software Supply Chain Failures](https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/) · [A05 Injection](https://owasp.org/Top10/2025/A05_2025-Injection/) · [A06 Insecure Design](https://owasp.org/Top10/2025/A06_2025-Insecure_Design/) · [A10 Mishandling of Exceptional Conditions](https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/)
- OWASP ASVS 5.0 — V1 Encoding and Sanitization · V2 Validation and Business Logic · V3 Web Frontend Security · V5 File Handling · V8 Authorization · V13 Configuration · V15 Secure Coding and Architecture · V16 Security Logging and Error Handling — https://github.com/OWASP/ASVS/tree/v5.0.0/5.0/en
- OWASP WSTG v4.2 — [INFO Coleta de informação](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/) · [CONF Configuração e implantação](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/) · [ATHZ Autorização](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/05-Authorization_Testing/) · [INPV Validação de entrada](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/) · [ERRH Tratamento de erro](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/08-Testing_for_Error_Handling/) · [BUSL Lógica de negócio](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/10-Business_Logic_Testing/) · [CLNT Lado do cliente](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/11-Client-side_Testing/)
- OWASP API Security Top 10:2023 — API1 Broken Object Level Authorization · API3 Broken Object Property Level Authorization · API4 Unrestricted Resource Consumption · API5 Broken Function Level Authorization · API7 Server Side Request Forgery · API8 Security Misconfiguration · API9 Improper Inventory Management · API10 Unsafe Consumption of APIs — https://owasp.org/API-Security/editions/2023/en/0x11-t10/
