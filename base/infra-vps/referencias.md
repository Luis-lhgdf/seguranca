# Referências — Infra de VPS

> **Revisado em:** 2026-10-07.

- Ubuntu Server — security — https://ubuntu.com/server/docs/security-introduction · unattended-upgrades — https://ubuntu.com/server/docs/package-management#automatic-updates
- Ubuntu Security Notices (USN) / CVE tracker — https://ubuntu.com/security/notices · https://ubuntu.com/security/cves
- Ubuntu Pro / Livepatch — https://ubuntu.com/pro
- OpenSSH `sshd_config` — https://man.openbsd.org/sshd_config
- Mozilla — OpenSSH guidelines — https://infosec.mozilla.org/guidelines/openssh
- ssh-audit — https://github.com/jtesta/ssh-audit
- UFW — https://help.ubuntu.com/community/UFW
- fail2ban — https://github.com/fail2ban/fail2ban · `fail2ban-regex` — https://fail2ban.readthedocs.io/
- Lynis — https://cisofy.com/lynis/
- CIS Benchmarks (Ubuntu Linux) — https://www.cisecurity.org/benchmark/ubuntu_linux
- Kernel sysctl hardening (KSPP) — https://kspp.github.io/Recommended_Settings
- systemd — sandboxing (`systemd.exec`) — https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html · `systemd-analyze security`
- auditd — https://github.com/linux-audit/audit-userspace
- GitHub — IPs dos runners (API meta) — https://api.github.com/meta
- CVE-2024-48990 (needrestart) — https://ubuntu.com/security/CVE-2024-48990

## Mapeamento oficial

Tabela item a item em [checklist/mapeamentos.md](../../checklist/mapeamentos.md#13-infraestrutura-de-vps-sec-vps).

- OWASP Top 10:2025 — [A01 Broken Access Control](https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/) · [A02 Security Misconfiguration](https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/) · [A03 Software Supply Chain Failures](https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/) · [A04 Cryptographic Failures](https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/) · [A07 Authentication Failures](https://owasp.org/Top10/2025/A07_2025-Authentication_Failures/) · [A08 Software or Data Integrity Failures](https://owasp.org/Top10/2025/A08_2025-Software_or_Data_Integrity_Failures/) · [A09 Security Logging and Alerting Failures](https://owasp.org/Top10/2025/A09_2025-Security_Logging_and_Alerting_Failures/) · [A10 Mishandling of Exceptional Conditions](https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/)
- OWASP ASVS 5.0 — V12 Secure Communication · V13 Configuration · V15 Secure Coding and Architecture · V16 Security Logging and Error Handling — https://github.com/OWASP/ASVS/tree/v5.0.0/5.0/en
- OWASP WSTG v4.2 — [CONF Configuração e implantação](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/) · [CRYP Criptografia fraca](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/09-Testing_for_Weak_Cryptography/)
