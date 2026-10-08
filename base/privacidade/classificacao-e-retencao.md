# Dado sensível: classificação, minimização e retenção

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Não é parecer jurídico: decisões de prazo e base legal são do responsável/DPO.

## 1. Por que

LGPD art. 11: dado de **saúde** (procedimento contratado, foto clínica, termo de consentimento) é
sensível. Vazamento gera **dever de comunicar ANPD e titulares**. Sem classificação formal, não se
prova cobertura numa auditoria (ASVS V14.1.1/V14.1.2).

## 2. Classificação (cabe numa tabela)

| Nível | Exemplos | Controle mínimo |
|---|---|---|
| Público | conteúdo do site, preço editorial | integridade (quem publica, auditoria) |
| Operacional/interno | configuração, métricas, trilha de auditoria | acesso autenticado, sem exposição pública |
| Pessoal | nome, e-mail, telefone, CPF, IP | schema de saída mínimo, `no-store`, retenção, mascarar em log |
| Sensível (saúde) / financeiro | foto de paciente, termo assinado, vínculo pessoa ↔ procedimento, dado de pagamento | permissão dedicada, auditoria de **acesso**, backup cifrado, nunca em URL/log, retenção curta, L3 do ASVS |

Manter a tabela **por campo** (planilha ou doc) e referenciá-la nas rotas/serviços.

## 3. Minimização

- Não guardar o que não usa; não pedir o que não precisa (ex.: formulário de contato que instrui a **não** enviar dado de saúde e nem passa pelo servidor).
- Remover metadado de imagem ([upload](../upload/metadados-de-imagem.md)).
- Nada sensível em URL (termo de busca de saúde via POST), log, mensagem de erro, `localStorage`.
- `cliente_id` esvaziado em registros que só precisam de agregado (ex.: tabela de mensagens).

## 4. Retenção e expurgo (ASVS V14.2.7, L3)

- Prazo por classe, escrito (ex.: foto com termo revogado há > X dias, pedidos antigos, vouchers expirados, clientes inativos, tokens, trilha, tabela de mensagens).
- **Job agendado** de expurgo/anonimização (comando que existe e nunca roda não conta).
- Soft delete preserva para sempre — combinar com o expurgo.
- Revogar consentimento despublica, mas o arquivo segue no disco e no backup: definir o que acontece com ele.
- Backup expira no seu próprio prazo ([copias-de-seguranca](../copias-de-seguranca/estrategia.md#5-retenção)).
- Termo de imagem tem canais e data — devem gerar consequência automática.

## 5. Direitos do titular

Fluxo para acesso, correção, eliminação e revogação; conta encerrada sem apagar o que a lei manda
guardar (ex.: fiscal) e sem perder voucher pago.
