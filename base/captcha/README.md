# Captcha (Cloudflare Turnstile)

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md).

**Cobre:** quando usar e quando **não** usar, por que Turnstile e não reCAPTCHA, achados medidos
contra a API real (chave de teste aceita qualquer token, HTTP 400, hostname, token de uso único),
configuração de front/back/CSP/painel, fail-open × fail-closed por rota, armadilhas de teste.
**Aplica-se quando:** existe rota pública de escrita enviada por humano (cadastro, recuperação,
OTP, agendamento, cupom, checkout, login). **N/A** sem formulário público que poste no backend.

| Arquivo | Conteúdo |
|---|---|
| [captcha-turnstile.md](captcha-turnstile.md) | decisão, configuração, falhas, testes |
| [referencias.md](referencias.md) | fontes oficiais |
| [checklist.md](checklist.md) | itens `SEC-CAP-*` |
