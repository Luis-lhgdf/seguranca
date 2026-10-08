# Checklist — Infraestrutura de VPS (VPS)

> **Revisado em:** 2026-10-07. Variáveis e regras em [`AGENTS.md`](../../AGENTS.md). Comandos **somente de leitura** via `ssh $VPS`; nada de reiniciar serviço, alterar firewall ou escanear sem autorização explícita.

### SEC-VPS-01 — SSH só por chave, sem root
- **Aplica-se quando:** VPS própria.
- **Risco se faltar:** força bruta de senha ou login direto como root.
- **Como verificar:** `ssh $VPS 'sudo sshd -T | grep -iE "^(permitrootlogin|passwordauthentication|kbdinteractiveauthentication|pubkeyauthentication|maxauthtries|x11forwarding|allowusers|allowtcpforwarding|allowagentforwarding) "'`.
- **OK quando:** `permitrootlogin no`, `passwordauthentication no`, `kbdinteractive no`, `maxauthtries ≤ 3`, forwarding desligado, `allowusers` restrito.
- **Referência:** [acesso-ssh.md#2-sshd-endurecido](acesso-ssh.md#2-sshd-endurecido).
- **Mapeamento:** Top 10 A07:2025, A02:2025 · sem requisito ASVS direto · WSTG-CONF-01.

### SEC-VPS-02 — Algoritmos SSH modernos
- **Aplica-se quando:** VPS própria.
- **Risco se faltar:** cifra/troca de chave fraca.
- **Como verificar:** `ssh-audit <host>` (de fora) ou `sshd -T | grep -E "^(ciphers|macs|kexalgorithms)"`.
- **OK quando:** sem alertas vermelhos no ssh-audit.
- **Referência:** [acesso-ssh.md#2-sshd-endurecido](acesso-ssh.md#2-sshd-endurecido).
- **Mapeamento:** Top 10 A04:2025 · sem requisito ASVS direto · WSTG-CONF-01.

### SEC-VPS-03 — Nenhum login suspeito
- **Aplica-se quando:** VPS própria.
- **Risco se faltar:** invasão já ocorrida passa despercebida.
- **Como verificar:** comandos da seção 4 de [acesso-ssh.md](acesso-ssh.md#4-evidência-de-não-comprometimento-auditoria); listar chaves autorizadas por usuário (só tipo e comentário: `awk '{print $1, $NF}'`).
- **OK quando:** só usuários/chaves conhecidos; zero login por senha.
- **Referência:** [acesso-ssh.md#4-evidência-de-não-comprometimento-auditoria](acesso-ssh.md#4-evidência-de-não-comprometimento-auditoria).
- **Mapeamento:** Top 10 A09:2025 · sem requisito ASVS direto.

### SEC-VPS-04 — Contas de serviço sem sudo e sudo do deploy restrito
- **Aplica-se quando:** VPS própria.
- **Risco se faltar:** falha na aplicação vira root.
- **Como verificar:** `ssh $VPS 'sudo -l -U <conta-servico>; sudo ls /etc/sudoers.d; sudo grep -rh NOPASSWD /etc/sudoers.d'`; `systemctl show <servico> -p User`.
- **OK quando:** apps rodam como contas sem sudo; NOPASSWD ausente ou limitado a comandos do deploy.
- **Referência:** [acesso-ssh.md#3-contas-e-privilégios](acesso-ssh.md#3-contas-e-privilégios).
- **Mapeamento:** Top 10 A01:2025, A02:2025 · sem requisito ASVS direto · WSTG-CONF-09.

### SEC-VPS-05 — Firewall default deny com só 22/80/443
- **Aplica-se quando:** VPS própria.
- **Risco se faltar:** serviço interno exposto à internet.
- **Como verificar:** `ssh $VPS 'sudo ufw status verbose; sudo ss -tlnp'`; registrar estado do firewall do provedor.
- **OK quando:** deny incoming, só 22/80/443 (IPv4 e IPv6); demais portas em loopback; decisão sobre o firewall de borda registrada.
- **Referência:** [firewall-e-fail2ban.md#1-firewall-em-duas-camadas](firewall-e-fail2ban.md#1-firewall-em-duas-camadas).
- **Mapeamento:** Top 10 A02:2025 · sem requisito ASVS direto · WSTG-CONF-01.

### SEC-VPS-06 — fail2ban ativo com jails validadas
- **Aplica-se quando:** VPS própria.
- **Risco se faltar:** força bruta e scanners sem consequência.
- **Como verificar:** `ssh $VPS 'sudo fail2ban-client status'` e status de cada jail; perguntar/procurar evidência de `fail2ban-regex`.
- **OK quando:** `sshd` + `recidive` + jails web ativas e validadas com log real.
- **Referência:** [firewall-e-fail2ban.md#2-fail2ban](firewall-e-fail2ban.md#2-fail2ban).
- **Mapeamento:** Top 10 A09:2025 · sem requisito ASVS direto.

### SEC-VPS-07 — Dotfiles bloqueados e honeypot (recomendado)
- **Aplica-se quando:** VPS com Nginx.
- **Risco se faltar:** `.env`/`.git` servidos; scanners livres para mapear.
- **Como verificar:** `for p in .env .git/config .htaccess wp-login.php; do curl -s -o /dev/null -w "$p %{http_code}\n" $SITE/$p; done`; `nginx -T | grep -n 'location ~ /\\.'`.
- **OK quando:** 403/404 em todos; bloqueio proativo no Nginx; isca com jail (recomendado).
- **Referência:** [firewall-e-fail2ban.md#3-bloqueio-proativo-de-dotfiles-e-honeypot](firewall-e-fail2ban.md#3-bloqueio-proativo-de-dotfiles-e-honeypot).
- **Mapeamento:** nível L1 · Top 10 A02:2025 · ASVS V13.4.1 (L1), V13.4.7 (L3) · WSTG-CONF-04.

### SEC-VPS-08 — Atualizações automáticas e reboot de kernel
- **Aplica-se quando:** VPS própria.
- **Risco se faltar:** CVEs conhecidas abertas por meses.
- **Como verificar:** `ssh $VPS 'cat /etc/apt/apt.conf.d/20auto-upgrades; grep -E "Automatic-Reboot" -r /etc/apt/apt.conf.d/; apt list --upgradable 2>/dev/null | wc -l; ls /var/run/reboot-required 2>/dev/null'`.
- **OK quando:** unattended ativo, reboot automático (ou Livepatch), poucas pendências, sem reboot pendente antigo.
- **Referência:** [hardening-do-sistema.md#1-atualizações](hardening-do-sistema.md#1-atualizações).
- **Mapeamento:** nível L1 · Top 10 A03:2025, A02:2025 · ASVS V15.2.1 (L1).

### SEC-VPS-09 — sysctl de rede e kernel endurecidos
- **Aplica-se quando:** VPS própria.
- **Risco se faltar:** spoofing, redirects e vazamento de info do kernel.
- **Como verificar:** comando da seção 2 de [hardening-do-sistema.md](hardening-do-sistema.md#2-kernel-e-rede-sysctl).
- **OK quando:** valores da seção aplicados.
- **Referência:** [hardening-do-sistema.md#2-kernel-e-rede-sysctl](hardening-do-sistema.md#2-kernel-e-rede-sysctl).
- **Mapeamento:** Top 10 A02:2025 · sem requisito ASVS direto · WSTG-CONF-01.

### SEC-VPS-10 — auditd, journald persistente, AppArmor e baseline
- **Aplica-se quando:** VPS própria.
- **Risco se faltar:** sem rastro para investigar incidente.
- **Como verificar:** `ssh $VPS 'sudo auditctl -l | wc -l; grep -E "^Storage|^SystemMaxUse" /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null; sudo aa-status | head -3'`; pedir último índice Lynis.
- **OK quando:** regras auditd presentes, journald persistente com teto, AppArmor ativo, Lynis registrado.
- **Referência:** [hardening-do-sistema.md#3-auditoria-e-logs-do-sistema](hardening-do-sistema.md#3-auditoria-e-logs-do-sistema).
- **Mapeamento:** nível L2 · Top 10 A09:2025, A02:2025 · ASVS V16.4.2 (L2).

### SEC-VPS-11 — Serviços da aplicação isolados no systemd
- **Aplica-se quando:** app rodando via systemd.
- **Risco se faltar:** falha na app escreve em qualquer lugar do sistema.
- **Como verificar:** `ssh $VPS 'systemctl cat <servico> | grep -E "User|NoNewPrivileges|ProtectSystem|ProtectHome|PrivateTmp|ReadWritePaths"; systemd-analyze security <servico> | tail -1'`.
- **OK quando:** usuário dedicado, `NoNewPrivileges`, `ProtectSystem=strict`, `ProtectHome`, `PrivateTmp`, escrita só nas pastas necessárias.
- **Referência:** [hardening-do-sistema.md#4-serviços-systemd-da-aplicação](hardening-do-sistema.md#4-serviços-systemd-da-aplicação).
- **Mapeamento:** nível L2 · Top 10 A02:2025 · ASVS V13.2.2 (L2) · WSTG-CONF-09.

### SEC-VPS-12 — Backend e banco só em loopback
- **Aplica-se quando:** VPS própria.
- **Risco se faltar:** atacante fala direto com o backend, pulando Nginx e rate limit.
- **Como verificar:** `ssh $VPS 'sudo ss -tlnp'`.
- **OK quando:** só Nginx (80/443) e SSH em `0.0.0.0`/`::`; o resto em `127.0.0.1`/`::1`.
- **Referência:** [hardening-do-sistema.md#4-serviços-systemd-da-aplicação](hardening-do-sistema.md#4-serviços-systemd-da-aplicação).
- **Mapeamento:** Top 10 A02:2025 · sem requisito ASVS direto · WSTG-CONF-01.

### SEC-VPS-13 — Healthcheck funcional com alerta externo
- **Aplica-se quando:** sistema em produção.
- **Risco se faltar:** site fora do ar e ninguém sabe.
- **Como verificar:** localizar o healthcheck (timer/cron) e ver se sonda rota que toca o banco; perguntar/procurar monitor externo e canal de alerta.
- **OK quando:** sonda real + alerta que sai do servidor.
- **Referência:** [operacao-continua.md#1-healthcheck-que-sonda-de-verdade](operacao-continua.md#1-healthcheck-que-sonda-de-verdade).
- **Mapeamento:** nível L2 · Top 10 A09:2025 · ASVS V16.4.3 (L2).

### SEC-VPS-14 — Smoke test de resiliência no procedimento de deploy
- **Aplica-se quando:** deploy que toca backend/deps/banco.
- **Risco se faltar:** falha que só aparece em reconexão derruba a API horas depois.
- **Como verificar:** procurar o bloco no checklist/script de deploy e evidência da última execução.
- **OK quando:** procedimento escrito e executado nos deploys relevantes.
- **Referência:** [operacao-continua.md#2-smoke-test-de-resiliência](operacao-continua.md#2-smoke-test-de-resiliência).
- **Mapeamento:** nível L2 · Top 10 A10:2025 · ASVS V16.5.2 (L2).

### SEC-VPS-15 — Validação externa feita (ssh-audit, testssl, portas, Lynis)
- **Aplica-se quando:** VPS em produção.
- **Risco se faltar:** configuração nunca conferida de fora.
- **Como verificar:** procurar relatórios/datas; executar `ssh-audit` e `testssl.sh` (leitura, não intrusivos).
- **OK quando:** executados há < 6 meses sem achado alto.
- **Referência:** [operacao-continua.md#4-validação-externa-pendência-comum--nunca-rodado](operacao-continua.md#4-validação-externa-pendência-comum--nunca-rodado).
- **Mapeamento:** nível L1 · Top 10 A02:2025 · ASVS V12.1.1 (L1) · WSTG-CONF-01, WSTG-CRYP-01.

### SEC-VPS-16 — Deploy com gate e build fora da produção (recomendado)
- **Aplica-se quando:** há CI/CD.
- **Risco se faltar:** push na main vai direto para produção; dependência hostil roda no servidor.
- **Como verificar:** ler `.github/workflows/*` e o script de deploy (testes/auditoria antes? onde roda o build?).
- **OK quando:** gate antes do deploy; build em runner ou risco aceito por escrito.
- **Referência:** [operacao-continua.md#5-deploy](operacao-continua.md#5-deploy).
- **Mapeamento:** nível L2 · Top 10 A08:2025, A03:2025 · ASVS V15.2.3 (L2).
