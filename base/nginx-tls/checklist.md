# Checklist — Nginx e TLS (WEB)

> **Revisado em:** 2026-10-07. Variáveis e regras em [`AGENTS.md`](../../AGENTS.md). Só leitura: `nginx -t`/`nginx -T`, `curl`, `openssl`, `testssl.sh`. Não recarregar o Nginx sem autorização.

### SEC-WEB-01 — Só TLS 1.2 e 1.3
- **Aplica-se quando:** site em HTTPS.
- **Risco se faltar:** protocolos antigos quebráveis.
- **Como verificar:** `openssl s_client -tls1_1` deve falhar; `testssl.sh -p https://<dominio>`.
- **OK quando:** apenas TLS 1.2/1.3, cifras do perfil intermediate.
- **Referência:** [tls-e-certificados.md#1-configuração](tls-e-certificados.md#1-configuração) · ASVS V12.
- **Mapeamento:** nível L1 · Top 10 A04:2025 · ASVS V12.1.1 (L1), V12.1.2 (L2) · WSTG-CRYP-01.

### SEC-WEB-02 — Certificado válido e renovação automática
- **Aplica-se quando:** certificado gerido por você.
- **Risco se faltar:** site fora do ar quando o certificado vence.
- **Como verificar:** datas via `openssl x509 -noout -dates`; `ssh $VPS 'systemctl list-timers | grep certbot'`.
- **OK quando:** válido por > 15 dias e timer ativo.
- **Referência:** [tls-e-certificados.md#4-como-verificar](tls-e-certificados.md#4-como-verificar).
- **Mapeamento:** nível L1 · Top 10 A04:2025 · ASVS V12.2.2 (L1) · WSTG-CRYP-01.

### SEC-WEB-03 — HTTP→HTTPS e host canônico
- **Aplica-se quando:** sempre.
- **Risco se faltar:** acesso em texto claro; cookies divididos entre dois hosts.
- **Como verificar:** `curl -sI http://<dominio>`; `curl -sI https://www.<dominio>`.
- **OK quando:** 301 para `https://` no host canônico.
- **Referência:** [tls-e-certificados.md#2-redirecionamentos](tls-e-certificados.md#2-redirecionamentos).
- **Mapeamento:** nível L1 · Top 10 A04:2025 · ASVS V12.2.1 (L1), V4.1.2 (L2) · WSTG-CRYP-03, WSTG-ATHN-01.

### SEC-WEB-04 — Nota de TLS externa
- **Aplica-se quando:** produção.
- **Risco se faltar:** configuração fraca não percebida.
- **Como verificar:** `testssl.sh https://<dominio>` ou SSL Labs.
- **OK quando:** nota A/A+ sem achado alto.
- **Referência:** [tls-e-certificados.md#4-como-verificar](tls-e-certificados.md#4-como-verificar).
- **Mapeamento:** nível L2 · Top 10 A04:2025 · ASVS V12.1.2 (L2) · WSTG-CRYP-01.

### SEC-WEB-05 — `server_tokens off`
- **Aplica-se quando:** Nginx.
- **Risco se faltar:** versão exposta facilita mirar CVE.
- **Como verificar:** `curl -sI $SITE | grep -i ^server:`.
- **OK quando:** sem número de versão.
- **Referência:** [configuracao-nginx.md#1-esqueleto-de-referência](configuracao-nginx.md#1-esqueleto-de-referência).
- **Mapeamento:** nível L3 · Top 10 A02:2025 · ASVS V13.4.6 (L3) · WSTG-INFO-02.

### SEC-WEB-06 — Proxy só para loopback e IP real confiável
- **Aplica-se quando:** Nginx na frente do app.
- **Risco se faltar:** app exposto direto; IP do cliente forjável.
- **Como verificar:** `grep -nE "proxy_pass|set_real_ip_from|real_ip_header" nginx-efetivo.txt`.
- **OK quando:** `proxy_pass` para `127.0.0.1`/socket; real IP só de faixas confiáveis.
- **Referência:** [configuracao-nginx.md#2-armadilhas](configuracao-nginx.md#2-armadilhas).
- **Mapeamento:** nível L2 · Top 10 A02:2025 · ASVS V4.1.3 (L2), V15.3.4 (L2).

### SEC-WEB-07 — Raiz privada nunca servida
- **Aplica-se quando:** há arquivos privados no servidor.
- **Risco se faltar:** documentos sensíveis acessíveis por URL.
- **Como verificar:** `grep -nE "alias|root " nginx-efetivo.txt` e comparar com os diretórios privados.
- **OK quando:** nenhum `alias/root` aponta para pasta privada.
- **Referência:** [configuracao-nginx.md#2-armadilhas](configuracao-nginx.md#2-armadilhas).
- **Mapeamento:** nível L1 · Top 10 A02:2025 · ASVS V13.4.1 (L1), V13.4.7 (L3) · WSTG-CONF-04.

### SEC-WEB-08 — Zonas de rate limit dedicadas (API e login)
- **Aplica-se quando:** Nginx com API.
- **Risco se faltar:** sem freio na borda.
- **Como verificar:** `grep -nE "limit_req" nginx-efetivo.txt`.
- **OK quando:** zona da API e zona estreita no login aplicadas nas locations certas.
- **Referência:** [configuracao-nginx.md#1-esqueleto-de-referência](configuracao-nginx.md#1-esqueleto-de-referência).
- **Mapeamento:** nível L2 · Top 10 A06:2025 · ASVS V2.4.1 (L2) · WSTG-ATHN-03 · API4:2023.

### SEC-WEB-09 — Config válida e versionada
- **Aplica-se quando:** Nginx sob seu controle.
- **Risco se faltar:** config do servidor diverge do repositório; ninguém sabe o que está no ar.
- **Como verificar:** `ssh $VPS 'sudo nginx -t'`; comparar `nginx -T` com o arquivo versionado no repositório (`diff`).
- **OK quando:** `nginx -t` ok e config do servidor igual à versionada.
- **Referência:** [configuracao-nginx.md#3-como-verificar](configuracao-nginx.md#3-como-verificar).
- **Mapeamento:** Top 10 A02:2025 · sem requisito ASVS direto · WSTG-CONF-02.
