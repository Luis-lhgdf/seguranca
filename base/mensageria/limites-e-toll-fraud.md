# Códigos por WhatsApp/SMS/e-mail: limites e toll fraud

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Preços mudam: confirme na fonte oficial antes de usar número.

## 1. O risco

Cada código é mensagem **paga** (WhatsApp *Authentication*, SMS). *Toll fraud / SMS pumping /
artificially inflated traffic*: alguém dispara códigos em massa e quem paga é você. OWASP MFA CS:
*"protect against attackers requesting a large number of messages to exhaust funds"*.

## 2. Ordem da contagem com vários limites (defeito comum)

- Defeito típico: a pessoa é contada **antes** do IP. Com o IP cheio, cada recusa gasta 1 dos 5 envios da pessoa → depois de 5, ela fica 1 h sem código **mesmo trocando de rede**; no "esqueci a senha" a tela diz "enviamos" e nada chega.
- Nenhuma fonte manda gastar o limite de uma dimensão quando outra recusou. Correto: **conferir todos os baldes e só então consumir**, atômico (script Lua no Redis; `MULTI/EXEC` não ramifica) — redis.io: *"avoids inflating the counter on denied requests"*.
- Alternativas piores: `DECR` depois (não atômico, num freio de dinheiro); inverter a ordem (a pessoa que estourou leva os vizinhos de CGNAT junto).
- OWASP: o freio não pode virar **DoS do dono** da conta.
- Separar o balde de IP do **e-mail** (custa ~nada) do balde da **mensagem paga**.

## 3. IP é só uma dimensão

Rate limit por IP falha com muitos IPs e erra com CGNAT. A defesa é a **soma**:

| Dimensão | Recomendação |
|---|---|
| Por conta/pessoa e finalidade | ex.: 5/h, 60 s entre envios |
| Por IP | alto (padrão ~30× a pessoa: 150/h), em **modo observar** primeiro |
| Por **número de destino** / prefixo | essencial onde **quem pede escolhe o destino** (OTP de cadastro); atraso exponencial para o mesmo número (Twilio) |
| Por **país** (DDI) | desligar países sem cliente (Twilio, Vonage). Preço varia por DDI: na tabela da Meta de out/2026, Authentication BR R$ 0,035; Alemanha R$ 0,2831 (8×); Authentication-International até R$ 0,8229 (23×) |
| Teto **global** por hora (disjuntor) | pega ataque distribuído; se apertado, derruba o login de todos — decidir se bloqueia ou só alerta |
| **Conversão** (códigos digitados ÷ enviados) | alarme; Vonage alerta em ≤ 35% |
| Captcha nas rotas de envio | camada, não substituto; fail-**closed** (mensagem é irreversível) |
| Teto de gasto / alerta de cobrança no fornecedor | OWASP API4:2023: *"Configure spending limits... When not possible, billing alerts"* |

Dimensão do risco (cálculo com os preços acima): um IP no teto de 20/h = R$ 16,80/dia; para a Alemanha,
R$ 135,89/dia — por IP.

## 4. Regras de envio

- Código de acesso só para **canal verificado**; a exceção (OTP de cadastro, número ainda não verificado) é a rota de maior risco.
- Meta: *"Confirm the user's WhatsApp phone number before sending the one-time password"*; a mensagem de autenticação só chega no aparelho principal.
- OTP: 6 dígitos CSPRNG, HMAC guardado, validade 10 min (NIST: fora de banda *"SHALL be considered invalid unless completed within 10 minutes"*), teto de palpites.
- Recusa por limite: evento de abuso + **código de referência** para o SAC (exceto no "esqueci a senha", que não pode revelar nada: só log). Resposta 429 com `Retry-After`.
- WhatsApp usado **apenas para OTP** (escolha comum para reduzir custo e superfície) limita templates — avisos de segurança vão por e-mail.
