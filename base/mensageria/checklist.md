# Checklist — Mensageria (MSG)

> **Revisado em:** 2026-10-07. Variáveis e regras em [`AGENTS.md`](../../AGENTS.md). **Nunca** disparar envio real em produção para testar limite — mensagem custa dinheiro: usar ambiente de teste/simulador.

### SEC-MSG-01 — Limite de envio por pessoa e finalidade
- **Aplica-se quando:** o backend envia código/mensagem.
- **Risco se faltar:** um script dispara milhares de mensagens pagas.
- **Como verificar:** localizar o serviço de envio; ler tetos (por hora, intervalo mínimo entre envios).
- **OK quando:** teto por pessoa+finalidade e intervalo mínimo.
- **Referência:** [limites-e-toll-fraud.md#3-ip-é-só-uma-dimensão](limites-e-toll-fraud.md#3-ip-é-só-uma-dimensão).
- **Mapeamento:** nível L2 · Top 10 A06:2025 · ASVS V2.3.2 (L2), V2.4.1 (L2) · WSTG-BUSL-05 · API6:2023.

### SEC-MSG-02 — Recusa de um limite não consome os outros
- **Aplica-se quando:** há mais de um limite (pessoa, IP, destino).
- **Risco se faltar:** cliente legítimo fica sem código por 1 h por causa do vizinho de rede.
- **Como verificar:** ler a ordem de incremento; teste local: encher o balde do IP e pedir códigos de outra conta → o contador da pessoa não sobe.
- **OK quando:** confere tudo e só consome no envio (atômico).
- **Referência:** [limites-e-toll-fraud.md#2-ordem-da-contagem-com-vários-limites-defeito-comum](limites-e-toll-fraud.md#2-ordem-da-contagem-com-vários-limites-defeito-comum).
- **Mapeamento:** nível L2 · Top 10 A06:2025 · ASVS V2.3.2 (L2) · WSTG-BUSL-05.

### SEC-MSG-03 — Limite por número de destino
- **Aplica-se quando:** alguma rota envia para número informado por quem pede (OTP de cadastro).
- **Risco se faltar:** várias contas descartáveis bombardeiam o mesmo número/prefixo.
- **Como verificar:** procurar chave de limite pelo destino.
- **OK quando:** teto por número (e idealmente por prefixo).
- **Referência:** [limites-e-toll-fraud.md#3-ip-é-só-uma-dimensão](limites-e-toll-fraud.md#3-ip-é-só-uma-dimensão).
- **Mapeamento:** nível L2 · Top 10 A06:2025 · ASVS V2.4.1 (L2), V6.6.3 (L2) · WSTG-BUSL-05.

### SEC-MSG-04 — Países de destino restritos
- **Aplica-se quando:** envia SMS/WhatsApp e o público é de poucos países.
- **Risco se faltar:** mensagens para DDI caro multiplicam o prejuízo (até 23×).
- **Como verificar:** ler a validação do telefone (aceita qualquer `+DDI`?); config de geo permission no provedor.
- **OK quando:** só os DDIs atendidos (ou decisão escrita).
- **Referência:** [limites-e-toll-fraud.md#3-ip-é-só-uma-dimensão](limites-e-toll-fraud.md#3-ip-é-só-uma-dimensão).
- **Mapeamento:** nível L2 · Top 10 A06:2025 · ASVS V2.3.2 (L2).

### SEC-MSG-05 — Teto global, alarme de conversão e alerta de gasto
- **Aplica-se quando:** envia mensagem paga.
- **Risco se faltar:** ataque distribuído passa despercebido até a fatura.
- **Como verificar:** procurar disjuntor global, métrica de conversão, AWS Budgets/alerta no fornecedor.
- **OK quando:** os três existem com limiares definidos.
- **Referência:** [custo-e-entregabilidade.md#3-alertas](custo-e-entregabilidade.md#3-alertas) · OWASP API4.
- **Mapeamento:** nível L2 · Top 10 A06:2025 · ASVS V2.1.3 (L2), V2.3.2 (L2) · WSTG-BUSL-07 · API4:2023.

### SEC-MSG-06 — Captcha fail-closed nas rotas que enviam
- **Aplica-se quando:** rota pública dispara envio.
- **Risco se faltar:** automação barata gasta seu dinheiro.
- **Como verificar:** ler a dependência de captcha nas rotas de envio e o comportamento quando o `siteverify` falha.
- **OK quando:** captcha validado no backend e recusa na falha.
- **Referência:** [../captcha/captcha-turnstile.md#6-quando-o-siteverify-falhar-fail-open--fail-closed](../captcha/captcha-turnstile.md#6-quando-o-siteverify-falhar-fail-open--fail-closed).
- **Mapeamento:** nível L2 · Top 10 A10:2025 · ASVS V2.4.1 (L2), V16.5.3 (L2).

### SEC-MSG-07 — Código só para canal verificado
- **Aplica-se quando:** envia código de acesso/recuperação.
- **Risco se faltar:** código vai para número/e-mail de terceiro.
- **Como verificar:** ler a escolha do destino (checa flag de verificado?).
- **OK quando:** só verificado (exceção única: verificação inicial, com limites próprios).
- **Referência:** [limites-e-toll-fraud.md#4-regras-de-envio](limites-e-toll-fraud.md#4-regras-de-envio) · ASVS V6.6.1.
- **Mapeamento:** nível L2 · Top 10 A07:2025 · ASVS V6.6.1 (L2).

### SEC-MSG-08 — Recusas registradas e rastreáveis pelo suporte
- **Aplica-se quando:** há limite de envio.
- **Risco se faltar:** ninguém vê o ataque; o SAC não acha o caso.
- **Como verificar:** recusa gera evento de abuso + código de referência (exceto onde não pode revelar nada).
- **OK quando:** evento registrado em toda recusa.
- **Referência:** [limites-e-toll-fraud.md#4-regras-de-envio](limites-e-toll-fraud.md#4-regras-de-envio).
- **Mapeamento:** nível L2 · Top 10 A09:2025 · ASVS V16.3.3 (L2).

### SEC-MSG-09 — Gasto mensurável (finalidade, preço versionado, entregue × aceito)
- **Aplica-se quando:** envia mensagem paga.
- **Risco se faltar:** impossível saber quanto custa e reconhecer anomalia.
- **Como verificar:** ler o modelo da tabela de envios e a existência de tabela de preços/conciliação.
- **OK quando:** finalidade registrada, preço versionado e conciliação com o provedor.
- **Referência:** [custo-e-entregabilidade.md#2-o-que-registrar-para-saber-quanto-se-gasta](custo-e-entregabilidade.md#2-o-que-registrar-para-saber-quanto-se-gasta).
- **Mapeamento:** nível L2 · Top 10 A06:2025 · ASVS V2.1.3 (L2).

### SEC-MSG-10 — SPF, DKIM e DMARC no domínio remetente
- **Aplica-se quando:** o sistema envia e-mail (ou o domínio é usado para e-mail).
- **Risco se faltar:** e-mails caem no spam; golpistas enviam e-mail falso em nome da empresa.
- **Como verificar:** `dig +short TXT <dominio>`; `dig +short TXT _dmarc.<dominio>`; seletor DKIM do provedor.
- **OK quando:** SPF e DKIM válidos, DMARC publicado (meta `p=quarantine`/`reject`).
- **Referência:** [custo-e-entregabilidade.md#4-entregabilidade-e-autenticidade-do-e-mail](custo-e-entregabilidade.md#4-entregabilidade-e-autenticidade-do-e-mail).
- **Mapeamento:** Top 10 A02:2025 · sem requisito ASVS direto.

### SEC-MSG-11 — Remetente de segurança separado do de marketing
- **Aplica-se quando:** envia e-mail transacional e de marketing.
- **Risco se faltar:** código de segurança cai em Promoções/spam.
- **Como verificar:** listar remetentes por template.
- **OK quando:** endereço distinto por categoria.
- **Referência:** [custo-e-entregabilidade.md#4-entregabilidade-e-autenticidade-do-e-mail](custo-e-entregabilidade.md#4-entregabilidade-e-autenticidade-do-e-mail).
- **Mapeamento:** Top 10 A06:2025 · sem requisito ASVS direto.
