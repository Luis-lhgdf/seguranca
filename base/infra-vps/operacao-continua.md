# VPS: monitoramento, smoke test e validação externa

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses), confirme na fonte oficial.

## 1. Healthcheck que sonda de verdade

- Timer/cron a cada ~10 min checando disco (WARN ≥ 85%), memória, status dos serviços **e requisição real**:
  - um endpoint que **consulta o banco** (não só `systemctl is-active` — o serviço "ativo" respondia 500);
  - a porta do frontend ativo (em blue-green, ler a cor ativa em vez de checar um serviço extinto — senão o healthcheck emite WARN falso a cada 10 min).
- 🔴 **Alerta precisa sair do servidor**: escrever `WARN` num log local não avisa ninguém. Usar uptime externo (UptimeRobot, Healthchecks.io, Better Stack), e-mail ou mensagem. Se a VPS cair, o healthcheck interno cai junto.
- `logrotate` dos logs próprios.

## 2. Smoke test de resiliência

Rodar a cada deploy que toque backend, dependências, banco ou systemd (~30 s):

```bash
sudo systemctl restart mysql && sleep 5            # ou postgresql
curl -s -o /dev/null -w 'api apos restart do banco: %{http_code}\n' http://127.0.0.1:8000/<rota-que-consulta-o-banco>
sudo systemctl restart <app-backend> && sleep 5
curl -s -o /dev/null -w 'api apos restart do backend: %{http_code}\n' http://127.0.0.1:8000/<rota-publica>
sudo /usr/local/bin/<healthcheck> && sudo tail -2 /var/log/<healthcheck>.log
```

Esperado: 200 nos dois e healthcheck sem WARN. **Regra:** dependência exercitada só em
*reconexão* (driver, TLS, auth) não aparece em teste de caminho feliz. Incidente típico: 2h40 de
500 por falta do pacote `cryptography` exigido no handshake `caching_sha2_password`, revelado
quando o `unattended-upgrades` reiniciou o MySQL. ⚠️ Em produção, só em janela combinada.

## 3. Snapshots

- Snapshot antes de mudança grande e após deploy estável; saber o prazo de expiração e o tempo de restore do provedor (ex.: snapshot único, expira em 24 h, restore ~30 min).
- Snapshot do provedor **não substitui** backup off-site (ver [copias-de-seguranca](../copias-de-seguranca/README.md)).

## 4. Validação externa (pendência comum — "nunca rodado")

- `ssh-audit <host>` — algoritmos do SSH.
- `testssl.sh https://<dominio>` ou SSL Labs — TLS (ver [nginx-tls](../nginx-tls/README.md)).
- `nmap -Pn --top-ports 1000 <host>` (com autorização) — portas.
- `lynis audit system` — índice de hardening.

## 5. Deploy

- Deploy automatizado (CI → SSH com forced-command → script) com **health check antes de trocar** a versão ativa (blue-green com releases imutáveis permite rollback).
- Build **na VPS de produção** expõe o servidor a dependência hostil (supply chain) — preferir build em runner e enviar artefato.
- Gate de segurança antes do deploy: ver [dependencias](../dependencias/README.md).
