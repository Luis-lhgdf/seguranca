# Login, lockout, MFA e step-up

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/preço/CVE, confirme na fonte oficial antes de aplicar.

## 1. Camadas contra força bruta e credential stuffing

| Camada | Exemplo de valor (usado na prática) | Observação |
|---|---|---|
| Rate limit na borda (Nginx) só na rota de login | `limit_req_zone ... rate=5r/m`, `burst=5 nodelay` | é o teto real quando o app tem vários workers |
| Rate limit na aplicação | `5/minute` por IP; ou 5 tentativas/15 min por e-mail | em memória = por processo; com Redis = global |
| Lockout por conta | 10 falhas → 15 min | contador **na conta**, não no IP (OWASP); curto e sem escalonar para não virar DoS do dono |
| Captcha | Turnstile no login, fail-open com limite apertado | ver [captcha](../captcha/README.md) |
| Hash caro | Argon2id + pepper | ver [senhas-hash-e-pepper.md](senhas-hash-e-pepper.md) |
| Anti-enumeração | `dummy_verify` + mensagem única | inclusive conta inativa/bloqueada |

⚠️ Lockout por conta + e-mail do admin conhecido = qualquer um tranca o operador. Aceitável com
lockout curto e rate limit na borda; **saber que existe** antes de descobrir num momento ruim.

## 2. MFA

- **Obrigatório em toda conta administrativa** (quem publica, edita preço, vê dado sensível) — PCI DSS 8.4.1; ASVS L2 trata como esperado para conta que administra dado sensível.
- Em conta de cliente com valor ativo (voucher, saldo) ou dado sensível, MFA ao menos como **step-up** (abaixo).
- TOTP é barato (uma tabela, um segredo, códigos de recuperação). Padrão-ouro: **FIDO2/WebAuthn/passkey** (resistente a phishing — CISA).
- SMS/telefone é autenticador **restrito** (NIST): oferecer alternativa e avisar do risco; OWASP MFA CS: SMS não deveria proteger app com PII de saúde ou risco financeiro sozinho.
- **E-mail não é fator** de autenticação fora de banda (NIST 800-63B-4 §3.1.3.1; ASVS 6.3.6). Código por e-mail serve para **verificar endereço** e **recuperar** conta, não como 2º fator.
- Bypass clássico: cliente decide o 2FA (resposta 401→200 manipulada; `TFA_enabled:false` no payload). O servidor é quem decide.
- Contas satélites também precisam de MFA: e-mail corporativo, registrador de domínio, hospedagem, GitHub, redes sociais, portal do gateway, CMS externo.

## 3. Step-up (login adaptativo)

Padrão recomendado:
- **Aparelho novo** (cookie de aparelho confiável de 30 dias, hash no banco) **ou** 3 senhas erradas seguidas → pede código no canal de 2º fator.
- Vale também para login social.
- Trocar/redefinir senha **esquece os aparelhos**; tela "Meus aparelhos".
- IP só é registrado (não decide sozinho).
- Gatilhos que rendem (aparelho novo, IP incomum) exigem rastreio de dispositivo; sem ele, "OTP após N erros" soma pouco sobre rate limit + captcha.

## 4. Reautenticação e notificação

- Reautenticação completa antes de trocar e-mail, telefone, senha ou fator (ASVS **V7.5.1**). Sessão roubada não pode plantar credencial permanente — exemplo: definir a **primeira** senha de conta só-social exige OTP no celular verificado.
- Superuser trocando a própria senha ou criando outro superuser deve redigitar a senha atual.
- Notificar o titular por canal **independente** após mudança de credencial, celular, aparelho novo, recuperação de conta (ASVS **V6.3.7**; NIST: *"all notification addresses"*), com instrução para "não fui eu".

## 5. Painel de operador único

- Restringir `/admin` e `/api/admin` por IP/VPN ou geobloqueio quando o operador é fixo — mais barato que captcha.
- `noindex` no `/admin`; robots não é controle de acesso.
- Bootstrap do 1º admin: fail-closed em produção (exige `SETUP_TOKEN`, `hmac.compare_digest`), 409 depois do 1º usuário, **token esvaziado do `.env`** após o uso, rate limit na rota de setup.
- Login, falha, lockout e logout **auditados** (ver [logs](../logs/README.md)).

## 6. Login social (OAuth/OIDC) — se houver

- Não **auto-vincular** contas pelo e-mail (Auth0).
- `email_verified` do Google só é autoritativo para `@gmail.com` ou com claim `hd`; para outro domínio sem `hd`, *"Google is not authoritative"*.
- Facebook: não assumir e-mail verificado sem fonte oficial (Firebase o classifica como provedor não confiável).
- Avatar do provedor baixado pelo backend = **SSRF** (ver [api/ssrf.md](../api/ssrf.md)).
