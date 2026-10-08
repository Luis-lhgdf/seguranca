# Referências

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/preço/CVE, confirme na fonte oficial antes de aplicar.

> Lista consolidada de fontes públicas usadas pela base e pelo checklist (OWASP, ASVS, NIST, CWE,
> documentação oficial de frameworks e ferramentas, avisos de CVE e artigos técnicos). Os links
> apontam para as fontes oficiais; reconfira antes de citar número ou versão em decisão nova.

## 1. Espinha dorsal — OWASP

| Recurso | Para que serve aqui | Link |
|---|---|---|
| **OWASP ASVS v5.0.0** (release 2025-05-30) | checklist de ~280+ requisitos verificáveis em 3 níveis; é o único material já em formato item a item e auditável. Ver [`04-asvs.md`](../fundamentos/asvs.md) | https://owasp.org/www-project-application-security-verification-standard/ · repo https://github.com/OWASP/ASVS (tem tradução PT-BR) |
| **OWASP Top 10 (2025)** | checklist de alto nível para não deixar classe de risco de fora; cobre o lado HTML/SSR que o API Top 10 não alcança | https://owasp.org/Top10/2025/ · https://github.com/OWASP/Top10 |
| **OWASP API Security Top 10 (2023)** | para backend 100% API: API1 (BOLA/IDOR), API2 (autenticação quebrada), API3 (autorização por propriedade), API4 (consumo sem limite), API6 (mass assignment) | https://owasp.org/www-project-api-security/ · https://github.com/OWASP/API-Security |
| **OWASP WSTG** (v4.2 estável; v5 em desenvolvimento) | o "como testar": IDs `WSTG-<categoria>-<nº>` para o passo de verificação | https://owasp.org/www-project-web-security-testing-guide/ · https://github.com/OWASP/wstg |
| **OWASP Proactive Controls (2024)** | o "o que fazer", na ordem do desenvolvedor; bom para onboarding | http://top10proactive.owasp.org/ |
| **OWASP Automated Threats (OAT)** | catálogo de abuso automatizado — OAT-019 Account Creation, OAT-015 Denial of Service | https://owasp.org/www-project-automated-threats-to-web-applications/ |

> ⚠️ A OWASP **não** mantém checklist específico de e-commerce/pagamento. O substituto mais
> completo é ASVS (L2/L3) + API Security Top 10 + cheat sheets de autenticação e sessão.

## 2. OWASP Cheat Sheet Series (o "como implementar")

Índice: https://cheatsheetseries.owasp.org/ · repo https://github.com/OWASP/CheatSheetSeries

| Cheat sheet | Tema na base |
|---|---|
| [Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) | login, mensagens genéricas, lockout que não vira DoS — [autenticacao/senhas-hash-e-pepper](../autenticacao/senhas-hash-e-pepper.md), [autenticacao/cadastro-e-enumeracao](../autenticacao/cadastro-e-enumeracao.md) |
| [Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) | Argon2id, parâmetros, pepper — [autenticacao/senhas-hash-e-pepper](../autenticacao/senhas-hash-e-pepper.md) |
| [Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) | cookies, expiração, revogação |
| [Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) | dono do recurso, permissão por módulo/ação |
| [Multifactor Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html) | troca de fator, SIM swap, custo de SMS — [autenticacao/telefone-em-varias-contas](../autenticacao/telefone-em-varias-contas.md) |
| [Forgot Password](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html) | PIN × link, mensagem consistente — [autenticacao/recuperacao-de-senha](../autenticacao/recuperacao-de-senha.md) |
| [Email Validation and Verification](https://cheatsheetseries.owasp.org/cheatsheets/Email_Validation_and_Verification_Cheat_Sheet.html) | verificar antes de liberar função; não normalizar Gmail |
| [Bot Management and Anti-Automation](https://cheatsheetseries.owasp.org/cheatsheets/Bot_Management_and_Anti-Automation_Cheat_Sheet.html) | velocidade de cadastro por IP/ASN/dispositivo |
| [SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) | ORM/prepared statements |
| [Cross Site Scripting Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) | escape por destino — [headers](../headers/README.md) |
| [Content Security Policy](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html) | CSP no HTML |
| [CSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) | double-submit, SameSite |
| [File Upload](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html) | magic bytes, SVG, metadado — [upload](../upload/README.md) |
| [Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) | `.env`, cofre, rotação — [segredos](../segredos/README.md) |
| [Logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) | trilha de auditoria — [logs](../logs/README.md) |

## 3. Normas e padrões externos

- **NIST SP 800-63B-4** (autenticação digital) — https://pages.nist.gov/800-63-4/sp800-63b.html.
  Política de senha (tamanho > complexidade, sem troca periódica forçada, checar senha vazada),
  OTP fora de banda válido por **10 min**, teto de falhas consecutivas na conta (**≤ 100**),
  e-mail não é fator fora de banda, celular compartilhado ("family phone"). A edição anterior
  (800-63-3) ainda é citada em material antigo: https://pages.nist.gov/800-63-3/sp800-63b.html
- **NIST SP 800-63A-4** (identidade) — https://pages.nist.gov/800-63-4/sp800-63a.html — código de
  confirmação ≥ 6 dígitos; validade 10 min (telefone) e 24 h (e-mail).
- **PCI-DSS v4.0.1** — https://www.pcisecuritystandards.org/standards/pci-dss/ · biblioteca
  https://www.pcisecuritystandards.org/document_library/. Se o gateway processa o cartão, o escopo
  tende a SAQ A/A-EP; "nunca armazenar dado de cartão" vale sempre. **8.4.1**: MFA em todo acesso
  administrativo — https://blog.pcisecuritystandards.org/understanding-new-pci-guidance-on-mfa
- **RFC 6585 §4** (HTTP 429, `Retry-After`) — https://www.rfc-editor.org/rfc/rfc6585.html
- **OpenID Connect Core** §5.1/§5.7 (`email_verified`) — https://openid.net/specs/openid-connect-core-1_0.html
- **LGPD** (Lei 13.709/2018), art. 11 — dado pessoal sensível (saúde). Ver [privacidade](../privacidade/README.md).

## 4. Pagamento e fraude

- **Stripe — card testing** — https://docs.stripe.com/disputes/prevention/card-testing
- **Visa — anti-enumeration e account testing (guia para lojistas, jun/2026)** —
  https://usa.visa.com/content/dam/VCOM/global/support-legal/documents/anti-enumeration-and-account-testing-best-practices-merchant.pdf
- **FBI/IC3 PSA240911 (BEC)** — 305.033 incidentes, US$ 55,5 bi (out/2013–dez/2023) — https://www.ic3.gov/PSA/2024/PSA240911
- **CISA AA24-290A** (força bruta, password spraying, push bombing) — https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-290a
- **CISA — MFA** (padrão-ouro: FIDO/WebAuthn) — https://www.cisa.gov/MFA
- Detalhes em [`11-gateway-de-pagamento.md`](../pagamentos/README.md).

## 5. Mensageria, OTP e toll fraud

- Meta — preços do WhatsApp Business — https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing
- Meta — templates de autenticação — https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/authentication-templates/authentication-templates
- Meta — analytics (`pricing_analytics`) — https://developers.facebook.com/documentation/business-messaging/whatsapp/analytics/
- Twilio — toll fraud — https://www.twilio.com/docs/verify/preventing-toll-fraud · rate limits programáveis — https://www.twilio.com/docs/verify/api/programmable-rate-limits · erro 60203 — https://www.twilio.com/docs/api/errors/60203 · Fraud Guard — https://www.twilio.com/docs/verify/preventing-toll-fraud/sms-fraud-guard
- Vonage — alerta de conversão — https://developer.vonage.com/en/blog/verify-conversion-alerts-in-fraud-defender · SMS Burst Protection — https://developer.vonage.com/en/fraud-defender/guides/sms-burst-protection
- OWASP API4:2023 (unrestricted resource consumption) — https://api-security.owasp.org/editions/2023/en/0xa4-unrestricted-resource-consumption
- AWS SES — preço https://aws.amazon.com/ses/pricing/ · monitoramento https://docs.aws.amazon.com/ses/latest/dg/monitor-sending-activity.html · Cost Explorer https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html · Budgets https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html
- Gmail — diretrizes de remetente (SPF/DKIM/DMARC, spam < 0,3%) — https://support.google.com/a/answer/81126
- Microsoft Defender Safe Links (scanner abre link antes da pessoa) — https://learn.microsoft.com/en-us/defender-office-365/safe-links-about
- Anatel — Ato 12.712/2024 (quarentena de 6 meses do número) — https://informacoes.anatel.gov.br/legislacao/component/content/article/154-atos-de-numera%C3%A7%C3%A3o/2140-ato-12712

## 6. Rate limit

- redis.io — 5 rate limiters (janela fixa × deslizante × balde de fichas; ler-decidir-gravar em Lua) — https://redis.io/tutorials/howtos/ratelimiting/ · token bucket — https://redis.io/docs/latest/develop/use-cases/rate-limiter/redis-py/
- Stripe — rate limiters em camadas — https://stripe.com/blog/rate-limiters
- Cloudflare — rate limiting rules ("IP with NAT support" só acima do plano básico) — https://developers.cloudflare.com/waf/rate-limiting-rules/
- OWASP — Blocking Brute Force — https://community.owasp.org/controls/Blocking_Brute_Force_Attacks

## 7. Captcha

- Cloudflare Turnstile — visão geral https://developers.cloudflare.com/turnstile/ · planos https://developers.cloudflare.com/turnstile/plans/ · modos https://developers.cloudflare.com/turnstile/concepts/widget/ · cliente https://developers.cloudflare.com/turnstile/get-started/client-side-rendering/ · servidor https://developers.cloudflare.com/turnstile/get-started/server-side-validation/ · CSP https://developers.cloudflare.com/turnstile/reference/content-security-policy/ · chaves de teste https://developers.cloudflare.com/turnstile/troubleshooting/testing/ · privacidade https://www.cloudflare.com/turnstile-privacy-policy/
- reCAPTCHA (Google Cloud Fraud Defense) — FAQ https://docs.cloud.google.com/recaptcha/docs/faq · migração https://docs.cloud.google.com/recaptcha/docs/migration-overview

## 8. Segredos e contêiner

- Docker Compose — use secrets — https://docs.docker.com/compose/how-tos/use-secrets/
- pydantic-settings — `secrets_dir` — https://pydantic.dev/docs/validation/latest/concepts/pydantic_settings/

## 9. Identidade e cadastro

- Firebase — email link auth / provedores confiáveis — https://firebase.google.com/docs/auth/android/email-link-auth · https://firebase.google.com/docs/auth/users
- Google Identity Platform — proteção contra enumeração — https://docs.cloud.google.com/identity-platform/docs/admin/email-enumeration-protection
- Microsoft Entra External ID — https://learn.microsoft.com/en-us/entra/external-id/customers/concept-authentication-methods-customers
- Auth0 — não vincular contas por e-mail — https://auth0.com/docs/manage-users/user-accounts/user-profiles/verified-email-usage
- Google — verificar ID token (`hd`, domínio não Gmail) — https://developers.google.com/identity/gsi/web/guides/verify-google-id-token
- Baymard — abandono de carrinho — https://baymard.com/lists/cart-abandonment-rate · conta adiada https://baymard.com/blog/delayed-account-creation
- NN/g — checklist de cadastro — https://www.nngroup.com/articles/checklist-registration-login/ · login walls https://www.nngroup.com/articles/login-walls/

## 10. Ferramentas

| Categoria | Ferramenta | Link |
|---|---|---|
| Dependências (Python) | **pip-audit** (PyPA Advisory DB) · safety | https://github.com/pypa/pip-audit · https://github.com/pyupio/safety |
| Dependências (JS) | **npm audit** | https://docs.npmjs.com/cli/v10/commands/npm-audit |
| SCA multi-linguagem | OWASP Dependency-Check (repo novo; o `jeremylong/` foi arquivado) · Snyk | https://github.com/dependency-check/DependencyCheck · https://snyk.io/product/open-source-security-management/ |
| Atualização automática | Dependabot (npm, pip/uv, github-actions) | https://docs.github.com/code-security/dependabot |
| SAST | **Bandit** (ou Ruff com regras `S`) · **Semgrep** | https://github.com/PyCQA/bandit · https://github.com/semgrep/semgrep |
| DAST | OWASP ZAP (contra staging/local; cuidado em produção) | https://www.zaproxy.org/ |
| Segredos | **gitleaks** (histórico incluso) · trufflehog (valida credencial) | https://github.com/gitleaks/gitleaks · https://github.com/trufflesecurity/trufflehog |
| Payloads de teste | PayloadsAllTheThings | https://github.com/swisskyrepo/PayloadsAllTheThings |
| Carga | k6 | https://k6.io/ |
| Infra | Lynis · ssh-audit · testssl.sh · SSL Labs · debsums | https://cisofy.com/lynis/ · https://github.com/jtesta/ssh-audit · https://testssl.sh/ · https://www.ssllabs.com/ssltest/ |

## 11. Recomendação de uso

1. **ASVS como espinha dorsal**: L2 como piso; L3 só nos fluxos que concentram o risco real
   (dinheiro, dado de saúde). Ver [`04-asvs.md`](../fundamentos/asvs.md).
2. Cada requisito → a **cheat sheet** correspondente (como fazer) → o **WSTG** (como testar).
3. Para API, cruzar com o **API Security Top 10** (mass assignment, consumo de recursos).
4. Automatizar: SAST (Bandit/Semgrep), dependências (pip-audit/npm audit), segredos (gitleaks)
   no CI; ZAP antes do go-live contra staging.
