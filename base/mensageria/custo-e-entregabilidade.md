# Mensageria: custo, monitoramento e entregabilidade de e-mail

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Preços e cotações mudam: confirme na fonte oficial.

## 1. Custo por código (referência de out/2026)

| Canal | Preço oficial | Em R$ | 1.000 códigos |
|---|---|---|---|
| WhatsApp *Authentication*, Brasil | R$ 0,035 por mensagem **entregue** (lista até 500 mil/mês; descontos acima) | 0,035 | R$ 35,00 |
| SES à la carte | US$ 0,10 / 1.000 | ~0,0005 | ~R$ 0,50 |
| SES *Essentials* | US$ 0,16 / 1.000 | ~0,0008 | ~R$ 0,80 |

Cotação usada: PTAX venda de 05/10/2026 = R$ 4,9859. WhatsApp ~44–70× mais caro. Reenvio e
"pedir pelo outro canal" **somam**. SES: sem cota gratuita por e-mail; conta AWS nova ganha
créditos de até US$ 200 em 12 meses.

## 2. O que registrar para saber quanto se gasta

- Tabela de envios com: canal, template, **finalidade** (coluna própria, não prefixo de chave), status, ids externos, tentativas.
- ⚠️ `enviada` = **a API aceitou**, não entregou. A Meta cobra entregue — sem webhook de status, a conta é teto; conciliar com `pricing_analytics` (COST/VOLUME por dia, país, categoria; até 1 ano; não retorna COST se a WABA usa linha de crédito de parceiro).
- **Tabela de preços versionada** (canal, categoria, país, preço `NUMERIC`, moeda, vigência, fonte).
- Registrar conferências de código (para a conversão).
- Separar produção de dev (simulador não grava como envio real).
- Retenção da tabela (o destinatário fica) — decisão LGPD.

## 3. Alertas

- Orçamento do mês (gasto projetado > X), pico diário (> N× a média de 7 dias), conversão < Y%.
- **AWS Budgets** (alerta real e previsto; atualiza até 3×/dia, com atraso) assim que a conta SES existir.
- Meta: verificar no Billing Hub/WhatsApp Manager se há teto de gasto (não confirmado em fonte oficial) e quem recebe a fatura.
- Conciliação mensal: estimativa × fatura × métricas do provedor; divergência acima de X% vira alerta.

## 4. Entregabilidade e autenticidade do e-mail

- **SPF, DKIM e DMARC** no domínio remetente (Gmail exige SPF ou DKIM; DMARC acima de 5.000/dia; spam < 0,3%).
- Sair do **sandbox** do SES antes do go-live.
- **Remetente por categoria**: código de segurança não sai do mesmo endereço das ofertas.
- E-mail de segurança só para endereço **confirmado**.
- DMARC também protege a marca contra e-mail falso em nome da empresa (phishing/BEC).
- Verificação: `dig +short TXT <dominio>`, `dig +short TXT _dmarc.<dominio>`, `dig +short TXT <seletor>._domainkey.<dominio>`.
