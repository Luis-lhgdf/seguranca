# VPS: hardening do sistema e dos serviços

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Comandos testados em Ubuntu 24.04 LTS. Se a data estiver antiga (> 6 meses) ou envolver versão/CVE, confirme na fonte oficial.

## 1. Atualizações

- `unattended-upgrades` instalado e ativo (`/etc/apt/apt.conf.d/20auto-upgrades`).
- **Reboot automático** em horário de baixo tráfego (ex.: 04:30) quando há patch de kernel pendente (`Unattended-Upgrade::Automatic-Reboot "true"` + `...-Time`). Fecha CVEs de kernel que só valem após reboot.
- Alternativa sem reboot: **Ubuntu Pro + Livepatch** (grátis para poucas máquinas; exige token Ubuntu One).
- Conferir pendências: `apt list --upgradable`; `/var/run/reboot-required`.
- ⚠️ Efeito colateral comum: o `unattended-upgrades` pode **reiniciar o MySQL** e expor uma dependência que só falha em reconexão → smoke test de resiliência ([operacao-continua.md](operacao-continua.md#2-smoke-test-de-resiliência)).
- Revisar CVEs da versão do SO periodicamente (ex.: needrestart LPE CVE-2024-48990 corrigido em `3.6-7ubuntu4.5`; snapd LPE CVE-2026-3888 N/A sem snapd). Ver [dependencias](../dependencias/README.md).

## 2. Kernel e rede (`sysctl`)

`/etc/sysctl.d/99-hardening.conf` e `98-kernel-hardening.conf`:
- `net.ipv4.conf.all.rp_filter=1`, `net.ipv4.tcp_syncookies=1`
- sem redirects/source route: `accept_redirects=0`, `send_redirects=0`, `accept_source_route=0` (IPv4 e IPv6)
- `kernel.kptr_restrict=2`, `kernel.dmesg_restrict=1`, `kernel.yama.ptrace_scope=1`, `fs.protected_hardlinks=1`, `fs.protected_symlinks=1`
- restrição de user namespaces não privilegiados (mitigação de bypass de 2025): `kernel.apparmor_restrict_unprivileged_userns=1`
- Conferir: `sudo sysctl -a 2>/dev/null | grep -E "rp_filter|syncookies|redirects|kptr|dmesg|ptrace|userns"`

## 3. Auditoria e logs do sistema

- **`auditd`** com regras para identidade (`/etc/passwd`, `shadow`, `group`), sudoers, `sshd_config`, uso de `sudo`/`su`, módulos do kernel, mudança de hora, cron (um conjunto típico tem ~16 regras). `sudo auditctl -l`.
- **journald persistente** com teto (ex.: `Storage=persistent`, `SystemMaxUse=500M`).
- **AppArmor** ativo (`sudo aa-status`).
- Baseline **Lynis** (`sudo lynis audit system`; referência: Hardening Index ~71 numa VPS Ubuntu 24.04 após este hardening) registrada e reexecutada após mudanças; `debsums` sem binário alterado.

## 4. Serviços systemd da aplicação

```
[Service]
User=www-app            # sem sudo, sem shell
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
ReadWritePaths=/opt/app/uploads /opt/app/private_uploads
```

- Backend escutando **só em `127.0.0.1`** (ex.: gunicorn `127.0.0.1:8000`); só o Nginx alcança.
- Avaliar com `systemd-analyze security <servico>` (nota menor = melhor).
- Diretórios: código com dono `deploy`; uploads com dono da conta de serviço; privados `750`.

## 5. Superfície

- Desinstalar o que não usa (snapd, serviços de exemplo); `systemctl list-units --type=service --state=running`.
- Nenhum painel de controle exposto sem necessidade.
