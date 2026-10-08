# VPS: firewall, fail2ban e honeypot

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou envolver versão/CVE, confirme na fonte oficial.

## 1. Firewall em duas camadas

⚠️ Sempre **liberar o SSH primeiro**, depois ativar.

**UFW (servidor):**
```bash
sudo ufw default deny incoming && sudo ufw default allow outgoing
sudo ufw allow OpenSSH && sudo ufw allow 80/tcp && sudo ufw allow 443/tcp
sudo ufw enable && sudo ufw status verbose   # IPv4 e IPv6
```

**Firewall do provedor (borda):** regras TCP 22/80/443 e default deny.
⚠️ Armadilha comum: o firewall de borda do provedor é ativado e depois **desativado de
propósito** porque bloqueia o runner do GitHub Actions (IPs variáveis) e quebra o deploy. Se
desativar, registrar o motivo; alternativas: allowlist das faixas do GitHub (mudam; API `meta`),
runner próprio, ou deploy por *pull* em vez de *push* por SSH.

Resultado esperado: só **22, 80, 443** abertos; banco, backend e Redis só em loopback
(`sudo ss -tlnp`). Validar de fora com `nmap -Pn -p- <host>` (com autorização).

## 2. fail2ban

| Jail | Função | Valores de referência |
|---|---|---|
| `sshd` | força bruta SSH | maxretry 5, bantime 1 h |
| `recidive` | reincidentes | ban de 1 semana |
| `nginx-limit-req` | quem estoura `limit_req` | maxretry 20 / 5 min, ban 30 min — **validar**: só funciona se o `error.log` registra os eventos |
| jail própria de caminhos de exploit (`/.env`, `/.git`, `wp-login.php`, `.php`) | scanners | 3 / 10 min, ban 1 h |
| jail de volume em `uploads.log` (proposta) | raspagem de mídia | N imagens/IP/min |

- **Validar filtro com log real**: `sudo fail2ban-regex /var/log/nginx/access.log /etc/fail2ban/filter.d/<filtro>.conf` (exemplo de validação: 97 matches, 0 falso positivo; o `nginx-botsearch` nativo pode não casar nada na sua instalação — confira).
- Comprovar o ban nos dois sentidos (bane e desbane).
- Status: `sudo fail2ban-client status` e `sudo fail2ban-client status <jail>`.

## 3. Bloqueio proativo de dotfiles e honeypot

- Não depender só do fail2ban (reativo): `location ~ /\.(?!well-known) { deny all; }` no Nginx — três linhas.
- **Honeypot:** `location` de isca (`/wp-login.php`, `/admin.php`, `/config.php`) retornando 403/404 com `access_log` próprio + jail sobre esse log → ban preventivo. Útil porque `Disallow: /admin` no `robots.txt` anuncia onde o painel fica.

## 4. Proteção DDoS

O provedor costuma cobrir só **L3/L4**; L7 exige CDN/WAF (ver [rate-limit](../rate-limit/camadas-e-cgnat.md#4-camadas)).
