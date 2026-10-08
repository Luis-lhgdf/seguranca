# Trilha de auditoria

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses), confirme na fonte oficial.

## 1. O que registrar (ASVS V16.2.1, V16.3.1, V16.3.2)

Cada registro: **quando, onde (IP real), quem (ator id + e-mail), o quê (ação + desfecho), alvo
(tipo + id)** e, em mudança de configuração, **valor anterior e novo**.

| Evento | Por quê |
|---|---|
| login: sucesso, **falha**, **lockout**, logout | sem isso, tentativa de invasão não deixa rastro (contador zerado no sucesso apaga o histórico) |
| detecção de **reuso de refresh token** | o sinal mais forte de roubo de sessão |
| toda ação sobre dado sensível, inclusive **leitura/exibição** e **download** | LGPD: "quem acessou o quê" |
| **delete** (irreversível) | lacuna comum: create/update auditados e delete não |
| mudança de permissão, criação de usuário, troca de senha | escalada de privilégio |
| mudança de configuração com **antes/depois** — em especial flags que desarmam controle de compliance | ex.: flag que dispensa termo para publicar foto sensível; restringir a superuser |
| emissão/uso de voucher/crédito, eventos de pagamento | prova contra chargeback; reconciliação |
| recusas de rate limit/abuso (evento + código de referência) | ver o ataque; SAC acha o caso |
| troca de número de telefone entre contas | sem o número no log |

## 2. Como registrar

- Gravar **na mesma transação** da ação (antes do commit): ação falhou → log some junto; nunca ação sem registro.
- `action` com desfecho (`result.create.published`, `consent.revoke(unpublished=3)`).
- IP real via proxy confiável.
- Leitura da trilha só por superuser; trilha não editável pela aplicação (append-only).
- Log do servidor web dedicado para mídia sensível (`/uploads/`) — responde "quem baixou qual foto".

## 3. O que **não** registrar

- Senha, token, pepper, código OTP, segredo, cabeçalho `Authorization`/`Cookie`.
- Vínculo pessoa ↔ dado sensível (nome do paciente, procedimento) — usar `target_type` + `target_id`.
- Número de telefone/CPF completos quando não necessário (mascarar).
- Nada disso também no Sentry/APM (filtros de PII ligados).

## 4. Retenção

Definir prazo da trilha (é dado pessoal: IP, e-mail) e expurgo agendado — ver [privacidade](../privacidade/README.md).
