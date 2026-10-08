# Referências — Autenticação

> **Revisado em:** 2026-10-07. Confira versões/IDs na fonte antes de citar em decisão nova.

- OWASP Password Storage CS — https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- OWASP Authentication CS — https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
- OWASP Multifactor Authentication CS — https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html
- OWASP Forgot Password CS — https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html
- OWASP Email Validation and Verification CS — https://cheatsheetseries.owasp.org/cheatsheets/Email_Validation_and_Verification_Cheat_Sheet.html
- OWASP Bot Management and Anti-Automation CS — https://cheatsheetseries.owasp.org/cheatsheets/Bot_Management_and_Anti-Automation_Cheat_Sheet.html
- OWASP OAT-019 Account Creation — https://owasp.org/www-project-automated-threats-to-web-applications/assets/oats/EN/OAT-019_Account_Creation
- OWASP ASVS 5.0 — capítulo V6 Authentication — https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md (6.3.6, 6.3.7, 6.3.8, 6.4.3, 6.4.4, 6.6.1, 6.6.3; V7.5.1)
- NIST SP 800-63B-4 — https://pages.nist.gov/800-63-4/sp800-63b.html (§3.1.3.1, §3.1.3.3, §3.2.2, §3.2.9, §4.2.1.2, §4.6)
- NIST SP 800-63A-4 — https://pages.nist.gov/800-63-4/sp800-63a.html (§2.1, §3.8)
- PCI DSS 8.4.1 (MFA administrativo) — https://blog.pcisecuritystandards.org/understanding-new-pci-guidance-on-mfa
- CISA — MFA — https://www.cisa.gov/MFA · AA24-290A — https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-290a
- argon2-cffi — https://pypi.org/project/argon2-cffi/ · docs https://argon2-cffi.readthedocs.io/
- Have I Been Pwned — Pwned Passwords (k-anonymity) — https://haveibeenpwned.com/API/v3#PwnedPasswords
- Firebase — provedores confiáveis — https://firebase.google.com/docs/auth/users · email link — https://firebase.google.com/docs/auth/android/email-link-auth
- Google Identity Platform — enumeração — https://docs.cloud.google.com/identity-platform/docs/admin/email-enumeration-protection
- Google — verificar ID token — https://developers.google.com/identity/gsi/web/guides/verify-google-id-token
- Auth0 — verified email — https://auth0.com/docs/manage-users/user-accounts/user-profiles/verified-email-usage
- OpenID Connect Core — https://openid.net/specs/openid-connect-core-1_0.html
- Microsoft Defender Safe Links — https://learn.microsoft.com/en-us/defender-office-365/safe-links-about
- Anatel — Ato 12.712/2024 — https://informacoes.anatel.gov.br/legislacao/component/content/article/154-atos-de-numera%C3%A7%C3%A3o/2140-ato-12712
- Baymard — https://baymard.com/lists/cart-abandonment-rate · NN/g — https://www.nngroup.com/articles/checklist-registration-login/

## Mapeamento oficial

Tabela item a item em [checklist/mapeamentos.md](../../checklist/mapeamentos.md#3-autenticação-cadastro-recuperação-sec-auth).

- OWASP Top 10:2025 — [A01 Broken Access Control](https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/) · [A02 Security Misconfiguration](https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/) · [A04 Cryptographic Failures](https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/) · [A06 Insecure Design](https://owasp.org/Top10/2025/A06_2025-Insecure_Design/) · [A07 Authentication Failures](https://owasp.org/Top10/2025/A07_2025-Authentication_Failures/)
- OWASP ASVS 5.0 — V2 Validation and Business Logic · V3 Web Frontend Security · V6 Authentication · V7 Session Management · V8 Authorization · V10 OAuth and OIDC · V11 Cryptography · V13 Configuration · V14 Data Protection · V15 Secure Coding and Architecture — https://github.com/OWASP/ASVS/tree/v5.0.0/5.0/en
- OWASP WSTG v4.2 — [CONF Configuração e implantação](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/) · [IDNT Gestão de identidade](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/03-Identity_Management_Testing/) · [ATHN Autenticação](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/04-Authentication_Testing/) · [BUSL Lógica de negócio](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/10-Business_Logic_Testing/)
- OWASP API Security Top 10:2023 — API4 Unrestricted Resource Consumption · API6 Unrestricted Access to Sensitive Business Flows — https://owasp.org/API-Security/editions/2023/en/0x11-t10/
