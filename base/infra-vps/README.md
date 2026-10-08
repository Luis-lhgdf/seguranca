# Infraestrutura de VPS

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md).

**Cobre:** acesso SSH e usuários, firewall em duas camadas, fail2ban, honeypot, atualizações e
reboot automático, `sysctl`, `auditd`, AppArmor, Lynis, hardening de serviços systemd,
healthcheck, smoke test de resiliência, snapshots, validação externa, deploy.
**Aplica-se quando:** o projeto roda em servidor próprio (VPS/dedicado). **N/A** em hospedagem
gerenciada/serverless (registrar quem é o responsável pela camada).

| Arquivo | Conteúdo |
|---|---|
| [acesso-ssh.md](acesso-ssh.md) | ordem segura, `sshd`, contas, evidência de não comprometimento |
| [firewall-e-fail2ban.md](firewall-e-fail2ban.md) | UFW + borda, jails, dotfiles, honeypot |
| [hardening-do-sistema.md](hardening-do-sistema.md) | updates, sysctl, auditd, systemd |
| [operacao-continua.md](operacao-continua.md) | healthcheck, smoke test, snapshots, validação externa, deploy |
| [referencias.md](referencias.md) | fontes oficiais e mapeamento Top 10 / ASVS / WSTG |
| [checklist.md](checklist.md) | itens `SEC-VPS-*` (com nível ASVS e mapeamento) |

Nginx/TLS: [nginx-tls](../nginx-tls/README.md). Backups: [copias-de-seguranca](../copias-de-seguranca/README.md).
