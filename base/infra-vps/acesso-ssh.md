# VPS: acesso SSH e usuários

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Comandos testados em Ubuntu 24.04 LTS. Se a data estiver antiga (> 6 meses) ou envolver versão/CVE, confirme na fonte oficial.

## 1. Ordem segura de configuração

1. **Snapshot inicial** no painel do provedor (ponto de restauração antes de mexer).
2. Gerar chave local: `ssh-keygen -t ed25519 -C "<projeto>-vps"`.
3. Primeiro acesso como root; atualizar o sistema; timezone (`timedatectl set-timezone America/Sao_Paulo`); swap se a RAM for pequena.
4. Criar usuário de deploy com sudo e instalar a chave pública.
5. ⚠️ **Testar login por chave com o novo usuário numa segunda sessão** antes de desligar senha/root.
6. Endurecer o SSH; reiniciar; validar em sessão nova **sem fechar a primeira**.

## 2. `sshd` endurecido

Arquivo `/etc/ssh/sshd_config.d/00-hardening.conf` (confirmar o efetivo com `sudo sshd -T`):

```
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
X11Forwarding no
AllowAgentForwarding no
AllowTcpForwarding no
AllowUsers deploy
```

Criptografia moderna (`60-crypto-hardening.conf`): `Ciphers`, `MACs` e `KexAlgorithms` modernos,
incluindo o pós-quântico `sntrup761x25519-sha512@openssh.com`. Validar externamente com
**`ssh-audit`**.

Porta 22 × alternativa: mudar a porta só reduz ruído; com fail2ban e só chave, manter 22 é aceitável.

## 3. Contas e privilégios

- Contas de serviço **separadas e sem sudo** para cada app (`www-fastapi`, `www-next`); código com dono `deploy`, runtime com dono da conta de serviço.
- `sudo NOPASSWD` no usuário de deploy é concessão à automação → apertar para senha (ou sudoers restrito aos comandos do deploy) quando a automação permitir.
- Chave do CI com **forced-command** (ver [segredos](../segredos/repositorio-e-ambiente.md#6-cicd)).
- `cron` com allowlist (`/etc/cron.allow`: só `root` e `deploy`).
- Revisar `~/.ssh/authorized_keys` de todos os usuários periodicamente (só chaves conhecidas).

## 4. Evidência de não comprometimento (auditoria)

- Logins por senha = 0 e só usuários esperados: `sudo journalctl -u ssh --since "-30d" | grep -E "Accepted|Failed" | awk '{print $6,$7,$9}' | sort | uniq -c`.
- `last -n 50`, `lastb | head` (tentativas).
- `debsums -s` sem binários alterados; scanner de malware ativo (o do provedor da VPS, quando houver, ou ClamAV/rkhunter).
