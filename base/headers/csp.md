# Content-Security-Policy (CSP)

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/CVE, confirme na fonte oficial antes de aplicar.

## 1. Por que

A CSP impede a **execução** do payload mesmo quando a injeção passa (XSS de conteúdo, script de
terceiro comprometido — Magecart) e limita para onde dado pode ser exfiltrado. Sem CSP, qualquer
falha de escape vira execução imediata. CSP só na API JSON **não protege nada** — JSON não executa.

## 2. Como implantar sem quebrar

1. Inventariar origens: scripts próprios, analytics (só após consentimento), captcha (`challenges.cloudflare.com` em `script-src` e `frame-src`), gateway de pagamento (tokenização), fontes, imagens.
2. Subir em **`Content-Security-Policy-Report-Only`** e navegar por todas as telas (inclusive painel logado) sem violação.
3. Promover para enforcing. **Rollback rápido:** trocar o nome do header de volta para `-Report-Only` e recarregar o Nginx — sem deploy.
4. Revalidar depois de virar enforcing.

## 3. `unsafe-inline` × nonce

- Frameworks com hidratação (Next.js App Router) exigem `'unsafe-inline'` em `script-src` **sem nonce** — essa CSP **não** impede XSS inline (ex.: o do JSON-LD); ela cobre script de terceiro, exfiltração e clickjacking. *Estado comum na prática:* enforcing com `unsafe-inline`; versão com nonce no backlog.
- Meta: **nonce (CSP3) + `strict-dynamic`** — o nonce na tag propaga para o que ela carrega (o Turnstile suporta).
- Nunca adicionar `unsafe-inline` "para resolver" na página de pagamento — cada terceiro com seus domínios.

## 4. Diretivas de referência (ponto de partida)

```
default-src 'self';
script-src 'self' 'nonce-<aleatório>' 'strict-dynamic' https://challenges.cloudflare.com;
frame-src https://challenges.cloudflare.com <gateway>;
img-src 'self' data: <storage>;
connect-src 'self' <analytics>;
style-src 'self' 'unsafe-inline';
frame-ancestors 'none';
base-uri 'self';
form-action 'self';
object-src 'none';
```

Ajustar ao inventário. `frame-ancestors` substitui `X-Frame-Options`.

## 5. SRI em script externo

Subresource Integrity (`integrity="sha384-..."`) quando o fornecedor publica arquivo estável.
Quando não publica (ex.: `gtag.js`, `api.js` do Turnstile, que não pode ser cacheado/proxiado),
a mitigação é a CSP com allowlist de host. Página de pagamento: **zero** script de terceiro.

## 6. Como verificar

- `curl -sI $SITE/ | grep -i content-security-policy` em cada location.
- Console do navegador sem violações nas telas principais.
- `csp-evaluator.withgoogle.com` para avaliar a política.
