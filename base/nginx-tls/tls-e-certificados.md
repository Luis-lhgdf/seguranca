# TLS e certificados

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou envolver versão/CVE, confirme na fonte oficial.

## 1. Configuração

- `ssl_protocols TLSv1.2 TLSv1.3;` — sem TLS 1.0/1.1, sem SSLv3.
- Cifras modernas (perfil *intermediate* do Mozilla SSL Config Generator); `ssl_prefer_server_ciphers off` com TLS 1.3.
- Certificado Let's Encrypt via **Certbot**, com renovação automática (`certbot.timer`); desafio ACME isolado num `location /.well-known/acme-challenge/` que não passa pelo app.
- Conta ACME com e-mail monitorado (avisos de expiração).
- OCSP stapling quando suportado.

## 2. Redirecionamentos

- Todo HTTP (80) → HTTPS (301).
- `www` → apex (ou o contrário), forçado — cookies emitidos num host só; evita par de hosts e cookie CSRF ilegível.
- HSTS (ver [headers](../headers/cabecalhos-de-seguranca.md#1-conjunto-mínimo-nas-páginas-html)); `preload` só com todos os subdomínios em HTTPS.

## 3. Banco e serviços internos

Banco em loopback dispensa TLS app↔banco; banco remoto/gerenciado exige TLS com verificação de
certificado.

## 4. Como verificar

```bash
curl -sI http://<dominio> | head -3                     # 301 para https
curl -sI https://www.<dominio> | grep -i location         # para o host canônico
echo | openssl s_client -connect <dominio>:443 -tls1_1 2>&1 | grep -iE "alert|handshake"   # deve falhar
echo | openssl s_client -connect <dominio>:443 -servername <dominio> 2>/dev/null | openssl x509 -noout -dates
ssh $VPS 'systemctl list-timers | grep -i certbot; sudo certbot certificates'
testssl.sh https://<dominio>   # ou SSL Labs (nota A/A+)
```
