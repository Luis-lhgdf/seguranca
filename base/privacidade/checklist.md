# Checklist — Privacidade, LGPD e cookies (LGPD)

> **Revisado em:** 2026-10-07. Variáveis e regras em [`AGENTS.md`](../../AGENTS.md). O agente aponta lacunas técnicas e documentais; decisões de base legal e prazo são do responsável/DPO.

### SEC-LGPD-01 — Classificação de dados por campo
- **Aplica-se quando:** há dado pessoal.
- **Risco se faltar:** não se sabe quais controles cada dado exige; não se prova cobertura.
- **Como verificar:** procurar tabela de classificação no repositório/docs; amostrar modelos do banco e conferir se cada campo pessoal/sensível aparece nela.
- **OK quando:** tabela existe, cobre os campos e diz o controle mínimo.
- **Referência:** [classificacao-e-retencao.md#2-classificação-cabe-numa-tabela](classificacao-e-retencao.md#2-classificação-cabe-numa-tabela) · ASVS V14.1.1.

### SEC-LGPD-02 — Política de retenção com expurgo agendado
- **Aplica-se quando:** há dado pessoal.
- **Risco se faltar:** dado guardado para sempre (multiplica o dano de um vazamento).
- **Como verificar:** procurar política escrita e job agendado (`systemctl list-timers`, crontab, scheduler da app).
- **OK quando:** prazo por classe + expurgo rodando.
- **Referência:** [classificacao-e-retencao.md#4-retenção-e-expurgo-asvs-v1427-l3](classificacao-e-retencao.md#4-retenção-e-expurgo-asvs-v1427-l3) · ASVS V14.2.7.

### SEC-LGPD-03 — Dado sensível fora de URL, log e storage do navegador
- **Aplica-se quando:** há dado sensível.
- **Risco se faltar:** vazamento por histórico, Referer, log ou aparelho compartilhado.
- **Como verificar:** listar rotas GET com parâmetros sensíveis; grep de `localStorage`; amostrar logs (mascarando).
- **OK quando:** nenhum dado sensível nesses lugares.
- **Referência:** [classificacao-e-retencao.md#3-minimização](classificacao-e-retencao.md#3-minimização).

### SEC-LGPD-04 — Analytics/ads só após consentimento
- **Aplica-se quando:** há analytics, pixel ou ads.
- **Risco se faltar:** coleta sem base legal; terceiros recebendo navegação de pacientes.
- **Como verificar:** abrir o site sem aceitar (navegador limpo) e listar requests a terceiros (DevTools/Playwright); ler o componente de consentimento.
- **OK quando:** nenhum request de rastreamento antes do aceite; recusa respeitada.
- **Referência:** [cookies-e-terceiros.md#1-consentimento-antes-de-rastrear](cookies-e-terceiros.md#1-consentimento-antes-de-rastrear).

### SEC-LGPD-05 — Política de privacidade lista os terceiros reais
- **Aplica-se quando:** há política publicada.
- **Risco se faltar:** tratamento não informado ao titular.
- **Como verificar:** comparar terceiros da política com os do inventário (analytics, captcha, CDN, e-mail, WhatsApp, gateway).
- **OK quando:** todos listados, inclusive transferência internacional.
- **Referência:** [cookies-e-terceiros.md#2-terceiros-em-página-sensível](cookies-e-terceiros.md#2-terceiros-em-página-sensível).

### SEC-LGPD-06 — Conteúdo sensível público com controles coerentes ao consentimento
- **Aplica-se quando:** o site publica imagem/dado de pessoas (antes/depois, depoimentos).
- **Risco se faltar:** exposição além do que a pessoa consentiu.
- **Como verificar:** consentimento escrito vinculado a cada publicação; gate no servidor ou desvio aceito por escrito; `noindex`/robots; OG neutra.
- **OK quando:** publicação exige termo válido e os controles cobrem o que o termo promete.
- **Referência:** [cookies-e-terceiros.md#4-conteúdo-sensível-público](cookies-e-terceiros.md#4-conteúdo-sensível-público).

### SEC-LGPD-07 — Fluxo de direitos do titular
- **Aplica-se quando:** há dado pessoal de clientes/usuários.
- **Risco se faltar:** pedido do titular sem resposta no prazo.
- **Como verificar:** procurar canal e procedimento (exportar, corrigir, eliminar, revogar).
- **OK quando:** procedimento escrito e executável.
- **Referência:** [classificacao-e-retencao.md#5-direitos-do-titular](classificacao-e-retencao.md#5-direitos-do-titular).
