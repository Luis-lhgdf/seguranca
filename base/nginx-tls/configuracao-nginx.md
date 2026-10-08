# Nginx como proxy reverso seguro

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou envolver versão/CVE, confirme na fonte oficial.

## 1. Esqueleto de referência

| Bloco | O que conter |
|---|---|
| `http` | `server_tokens off`; `limit_req_zone` (ex.: `api_limit` 20r/s, `login_limit` 5r/m); `map` para a CSP |
| `server :80` | ACME + `return 301 https://...` |
| `server www` | redirect para o apex |
| `server :443` | TLS; `client_max_body_size` (ex.: 25m); headers de segurança; locations |
| `location /` | proxy para o front (Next) — prefetch conta se houver `limit_req` aqui |
| `location /api/` | proxy para `127.0.0.1:<porta>`; `limit_req zone=api_limit burst=40 nodelay`; `proxy_set_header X-Real-IP`/`X-Forwarded-For`/`X-Forwarded-Proto` |
| `location = /api/<login>` | `limit_req zone=login_limit burst=5 nodelay` |
| `location /uploads/` | `alias`; `autoindex off`; `nosniff`; `access_log` dedicado; cache conforme sensibilidade |
| `location /_next/static/` | cache longo imutável (é só asset) |
| `location ~ /\.(?!well-known)` | `deny all` |
| isca (honeypot) | `return 404` + log próprio |

## 2. Armadilhas

- **`add_header` não herda** quando a `location` declara qualquer `add_header` — repetir os headers (ou `include` de snippet) em cada location. Ver [headers](../headers/cabecalhos-de-seguranca.md#3-armadilha-do-nginx-add_header-não-herda).
- Root privado (documentos) **nunca** num `alias`/`root`.
- `proxy_pass` para `127.0.0.1`, não para IP público.
- IP real: `set_real_ip_from` só para faixas confiáveis (CDN) — senão o cliente forja `X-Forwarded-For`.
- Mudança de config: `sudo nginx -t` antes de `reload`; rollback rápido de CSP trocando para `-Report-Only`.
- `/admin` cai no `location /` genérico — para restringir por IP, criar location específica.

## 3. Como verificar

```bash
ssh $VPS 'sudo nginx -t && sudo nginx -T' > nginx-efetivo.txt   # config efetiva (não contém segredo; confira antes de anexar)
grep -nE "server_tokens|ssl_protocols|limit_req|client_max_body_size|autoindex|add_header|location|proxy_pass|set_real_ip_from" nginx-efetivo.txt
```
