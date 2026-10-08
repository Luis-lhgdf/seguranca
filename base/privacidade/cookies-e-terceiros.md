# Cookies, consentimento e terceiros no navegador

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Não é parecer jurídico.

## 1. Consentimento antes de rastrear

- Scripts de analytics/ads (GA4, Google Ads, pixels) **só após o aceite** (consent mode); recusar deve funcionar de verdade (nenhum request ao terceiro).
- Origem da visita (UTM) preservada mesmo quando o aceite vem depois — sem gravar identificador antes do aceite.
- Cookie de consentimento: guarda só a escolha; `SameSite=Lax`, `Secure`.
- Política de privacidade e de cookies listam cada terceiro (inclusive o captcha; o modo *invisible* do Turnstile **obriga** citar o *Turnstile Privacy Addendum*).
- Ephemeral ID/fingerprint de dispositivo = dado pessoal → base legal e aviso.

## 2. Terceiros em página sensível

- Página com dado de saúde no path/querystring vaza via `Referer` para analytics → `Referrer-Policy: strict-origin-when-cross-origin` e termo sensível fora da URL.
- Página de pagamento sem terceiros.
- Transferência internacional (Cloudflare, Google, Meta, AWS) — registrar na política.

## 3. Armazenamento no navegador

- `localStorage` persiste no aparelho: nada de dado sensível nele. Preferir `sessionStorage` para carrinho/favoritos de visitante, com comentário do motivo no código (LGPD art. 11).
- Lembrar e-mail no login do painel: aceitável (não é segredo), consciente.

## 4. Conteúdo sensível público

- Aviso/gate de conteúdo (+18) só no cliente é aviso, não controle de acesso ([upload](../upload/midia-publica-e-privada.md#3-galeria-sensível-e-raspagem)).
- `noindex` em áreas que não devem ser indexadas; `robots.txt` também para crawlers de IA; sitemap sem itens sensíveis; OG neutra em conteúdo sensível.
- Publicidade de serviços de saúde tem regra profissional (ex.: Cofen 554/2017 para enfermagem) além da LGPD — consentimento de imagem por escrito, com canais autorizados e prazo.
