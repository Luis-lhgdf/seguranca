# Referências — Upload

> **Revisado em:** 2026-10-07.

- OWASP File Upload CS — https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
- OWASP ASVS 5.0 — V5 File Handling (5.2.2, 5.3.1, 5.3.2) — https://github.com/OWASP/ASVS
- OWASP WSTG — Test Upload of Malicious Files (WSTG-BUSL-09) — https://owasp.org/www-project-web-security-testing-guide/
- Pillow — `Image.MAX_IMAGE_PIXELS` / DecompressionBombError — https://pillow.readthedocs.io/en/stable/reference/Image.html
- ExifTool — https://exiftool.org/
- Especificação EXIF (CIPA DC-008) — https://www.cipa.jp/e/std/std-sec.html
- Google — WebP container (RIFF, VP8X, chunks EXIF/XMP) — https://developers.google.com/speed/webp/docs/riff_container
- PNG spec (chunks tEXt/iTXt) — https://www.w3.org/TR/png-3/
- PayloadsAllTheThings — Upload Insecure Files — https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Upload%20Insecure%20Files

## Mapeamento oficial

Tabela item a item em [checklist/mapeamentos.md](../../checklist/mapeamentos.md#6-upload-e-mídia-sec-upl).

- OWASP Top 10:2025 — [A01 Broken Access Control](https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/) · [A02 Security Misconfiguration](https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/) · [A05 Injection](https://owasp.org/Top10/2025/A05_2025-Injection/) · [A06 Insecure Design](https://owasp.org/Top10/2025/A06_2025-Insecure_Design/)
- OWASP ASVS 5.0 — V1 Encoding and Sanitization · V2 Validation and Business Logic · V3 Web Frontend Security · V5 File Handling · V8 Authorization · V13 Configuration · V14 Data Protection — https://github.com/OWASP/ASVS/tree/v5.0.0/5.0/en
- OWASP WSTG v4.2 — [INFO Coleta de informação](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/) · [CONF Configuração e implantação](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/) · [ATHZ Autorização](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/05-Authorization_Testing/) · [BUSL Lógica de negócio](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/10-Business_Logic_Testing/)
- OWASP API Security Top 10:2023 — API4 Unrestricted Resource Consumption · API6 Unrestricted Access to Sensitive Business Flows — https://owasp.org/API-Security/editions/2023/en/0x11-t10/
