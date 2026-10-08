# Referências — Banco

> **Revisado em:** 2026-10-07.

- OWASP SQL Injection Prevention CS — https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
- OWASP Database Security CS — https://cheatsheetseries.owasp.org/cheatsheets/Database_Security_Cheat_Sheet.html
- OWASP ASVS 5.0 — V1.2.4, V2.3.4, V15.4.2 — https://github.com/OWASP/ASVS
- MySQL 8 — Security Guidelines — https://dev.mysql.com/doc/refman/8.0/en/security-guidelines.html · `mysql_secure_installation` — https://dev.mysql.com/doc/refman/8.0/en/mysql-secure-installation.html · GRANT — https://dev.mysql.com/doc/refman/8.0/en/grant.html
- PostgreSQL — Client Authentication / roles — https://www.postgresql.org/docs/current/client-authentication.html · `SELECT ... FOR UPDATE` — https://www.postgresql.org/docs/current/sql-select.html#SQL-FOR-UPDATE-SHARE
- Redis — Security — https://redis.io/docs/latest/operate/oss_and_stack/management/security/
- Supabase — Row Level Security — https://supabase.com/docs/guides/database/postgres/row-level-security
- SQLAlchemy — ORM / bound parameters — https://docs.sqlalchemy.org/
- PyPI Advisory (ex.: PYSEC-2026-286) — https://github.com/pypa/advisory-database

## Mapeamento oficial

Tabela item a item em [checklist/mapeamentos.md](../../checklist/mapeamentos.md#8-banco-de-dados-sec-bd).

- OWASP Top 10:2025 — [A01 Broken Access Control](https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/) · [A02 Security Misconfiguration](https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/) · [A04 Cryptographic Failures](https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/) · [A05 Injection](https://owasp.org/Top10/2025/A05_2025-Injection/) · [A06 Insecure Design](https://owasp.org/Top10/2025/A06_2025-Insecure_Design/) · [A10 Mishandling of Exceptional Conditions](https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/)
- OWASP ASVS 5.0 — V1 Encoding and Sanitization · V2 Validation and Business Logic · V8 Authorization · V12 Secure Communication · V13 Configuration · V15 Secure Coding and Architecture · V16 Security Logging and Error Handling — https://github.com/OWASP/ASVS/tree/v5.0.0/5.0/en
- OWASP WSTG v4.2 — [CONF Configuração e implantação](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/) · [ATHZ Autorização](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/05-Authorization_Testing/) · [INPV Validação de entrada](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/) · [ERRH Tratamento de erro](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/08-Testing_for_Error_Handling/) · [BUSL Lógica de negócio](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/10-Business_Logic_Testing/)
- OWASP API Security Top 10:2023 — API1 Broken Object Level Authorization — https://owasp.org/API-Security/editions/2023/en/0x11-t10/
