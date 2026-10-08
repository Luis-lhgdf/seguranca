# Cabeçalhos de segurança

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/CVE, confirme na fonte oficial antes de aplicar.

## 1. Conjunto mínimo nas páginas HTML

| Cabeçalho | Valor de referência | Observação |
|---|---|---|
| `Strict-Transport-Security` | `max-age=63072000; includeSubDomains; preload` | só depois de todo subdomínio ter HTTPS |
| `Content-Security-Policy` | ver [csp.md](csp.md) | **no HTML**, não só na API |
| `X-Content-Type-Options` | `nosniff` | também em `/uploads/` |
| `X-Frame-Options` | `DENY` (ou `SAMEORIGIN` se o site se embute) | `frame-ancestors` na CSP substitui e unifica |
| `Referrer-Policy` | `strict-origin-when-cross-origin`; `no-referrer` em página com token na URL | evita vazar path com dado sensível para terceiros |
| `Permissions-Policy` | desligar o que não usa (`camera=(), microphone=(), geolocation=()`) | |
| `Cross-Origin-Opener-Policy` | `same-origin` | |
| `server_tokens off` / `poweredByHeader: false` | — | não anunciar versão |

Na API JSON: os mesmos + `Content-Security-Policy: default-src 'none'; frame-ancestors 'none'`.

## 2. `Cache-Control` em resposta sensível

- `Cache-Control: no-store` em **toda** resposta autenticada ou com PII (inclusive `FileResponse` de arquivo privado). ASVS V14.3.2.
- Padrão eficiente: emitir `no-store` e `Referrer-Policy` na **dependência de autenticação** — toda rota autenticada herda.
- *Achado típico em auditoria:* nenhuma ocorrência de `Cache-Control` no backend enquanto a rota de termos de consentimento devolvia nome de paciente.

## 3. Armadilha do Nginx: `add_header` não herda

Declarar **um** `add_header` dentro de um `location` **descarta todos** os herdados do `server`.
Repetir o bloco de headers em cada `location` (`/`, `/uploads/`, `/_next/static/`, `/api/`) ou usar
`include` de um snippet. Para não duplicar a CSP, usar `map` (padrão recomendado). Testar cada
location com `curl -sI`.

## 4. Divergências comuns

- `X-Frame-Options: SAMEORIGIN` no Nginx × `DENY` no middleware do backend → padronizar via `frame-ancestors`.
- `next.config` comentando "CSP fica no Nginx" e o Nginx sem CSP → conferir a resposta real, não o comentário.
- Cookie de consentimento sem `Secure` — baixo risco (não é segredo), mas padronizar.

## 5. Como verificar

```bash
for p in / /admin/login /uploads/<arquivo> /_next/static/<arquivo> /api/<rota>; do
  echo "== $p"; curl -sI "$SITE$p" | grep -iE "strict-transport|content-security|x-content-type|x-frame|referrer-policy|permissions-policy|cache-control|server:|x-powered-by"
done
```

Complementos: securityheaders.com, Mozilla Observatory.
