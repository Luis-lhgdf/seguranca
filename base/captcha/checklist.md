# Checklist — Captcha (CAP)

> **Revisado em:** 2026-10-07. Variáveis e regras em [`AGENTS.md`](../../AGENTS.md). Se o projeto não tem formulário público que poste no backend, marque os itens SEC-CAP-02 a 08 como N/A citando SEC-CAP-01.

### SEC-CAP-01 — Decisão sobre captcha registrada
- **Aplica-se quando:** há qualquer rota pública de escrita.
- **Risco se faltar:** captcha onde não protege nada (custo de conversão) ou ausência onde o abuso custa caro.
- **Como verificar:** listar rotas públicas de escrita e classificar (humano × beacon); procurar a decisão escrita.
- **OK quando:** captcha em toda rota humana com custo de abuso, ou N/A justificado com gatilhos de reavaliação.
- **Referência:** [captcha-turnstile.md#1-precisa-de-captcha-decisão](captcha-turnstile.md#1-precisa-de-captcha-decisão).

### SEC-CAP-02 — Token validado no backend
- **Aplica-se quando:** há captcha.
- **Risco se faltar:** o captcha só existe na tela; scripts postam direto na API.
- **Como verificar:** `grep -rn "siteverify" $REPO`; em teste, POST sem token → 422.
- **OK quando:** `siteverify` chamado antes do trabalho caro, com `max_length` no token.
- **Referência:** [captcha-turnstile.md#3-fluxo-e-ordem](captcha-turnstile.md#3-fluxo-e-ordem).

### SEC-CAP-03 — Produção recusa chave de teste
- **Aplica-se quando:** Turnstile.
- **Risco se faltar:** subir com chave de teste aprova 100% do tráfego sem nada parecer errado.
- **Como verificar:** procurar guard de `result_with_testing_key` e validação de config na subida.
- **OK quando:** os dois existem.
- **Referência:** [captcha-turnstile.md#4-achados-medidos-contra-a-api-real-valem-para-qualquer-projeto](captcha-turnstile.md#4-achados-medidos-contra-a-api-real-valem-para-qualquer-projeto).

### SEC-CAP-04 — HTTP 400, hostname e action tratados
- **Aplica-se quando:** Turnstile.
- **Risco se faltar:** exceção em vez de recusa limpa; token gerado em outro site aceito.
- **Como verificar:** ler o cliente do `siteverify`: status antes do JSON; `hostname` contra lista do ambiente; `action` = rota.
- **OK quando:** os três conferidos.
- **Referência:** [captcha-turnstile.md#4-achados-medidos-contra-a-api-real-valem-para-qualquer-projeto](captcha-turnstile.md#4-achados-medidos-contra-a-api-real-valem-para-qualquer-projeto).

### SEC-CAP-05 — Token renovado após toda tentativa
- **Aplica-se quando:** formulário com captcha que pode falhar por outro motivo (senha errada).
- **Risco se faltar:** segunda tentativa sempre falha ("token já usado") e trava o usuário.
- **Como verificar:** procurar `reset()`/renovação no `finally` do envio.
- **OK quando:** renova sempre; existe botão "Tentar de novo".
- **Referência:** [captcha-turnstile.md#4-achados-medidos-contra-a-api-real-valem-para-qualquer-projeto](captcha-turnstile.md#4-achados-medidos-contra-a-api-real-valem-para-qualquer-projeto).

### SEC-CAP-06 — Comportamento na falha do provedor decidido por rota
- **Aplica-se quando:** há captcha.
- **Risco se faltar:** fail-open silencioso em rota que gasta dinheiro; ou login trancado para todos.
- **Como verificar:** ler o tratamento de timeout/erro por rota; procurar teste com mock fora do ar.
- **OK quando:** cadastro/OTP recusam, login passa com limite apertado, contador + alerta em toda falha.
- **Referência:** [captcha-turnstile.md#6-quando-o-siteverify-falhar-fail-open--fail-closed](captcha-turnstile.md#6-quando-o-siteverify-falhar-fail-open--fail-closed).

### SEC-CAP-07 — Widget por ambiente e secret só no servidor
- **Aplica-se quando:** Turnstile.
- **Risco se faltar:** produção aceita `localhost`; secret exposto.
- **Como verificar:** ler config (hostnames de produção sem `localhost`); grep do secret no front.
- **OK quando:** widgets separados; secret só no backend.
- **Referência:** [captcha-turnstile.md#5-configuração](captcha-turnstile.md#5-configuração).

### SEC-CAP-08 — Captcha não substitui rate limit
- **Aplica-se quando:** há captcha.
- **Risco se faltar:** serviço de resolução de captcha passa sem freio.
- **Como verificar:** as mesmas rotas têm rate limit por IP e identidade?
- **OK quando:** os dois juntos.
- **Referência:** [captcha-turnstile.md#1-precisa-de-captcha-decisão](captcha-turnstile.md#1-precisa-de-captcha-decisão).
