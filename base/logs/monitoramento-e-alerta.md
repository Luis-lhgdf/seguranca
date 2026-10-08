# Monitoramento e alerta

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses), confirme na fonte oficial.

## 1. Princípio

Não adianta logar e ninguém ver. Alerta precisa **sair do servidor** e chegar a uma pessoa.

## 2. O que monitorar

| Sinal | Fonte |
|---|---|
| site/API fora do ar | uptime externo (sonda que toca o banco) |
| disco ≥ 85%, memória, serviço caído | healthcheck interno + alerta externo |
| erros 5xx e exceções | Sentry/APM (sem PII) |
| picos de 401/429, lockouts | log de auditoria / Nginx |
| volume anômalo de leitura/download de mídia sensível | `uploads.log` por IP/minuto |
| bans do fail2ban repetidos | fail2ban / journald |
| falhas do `siteverify` (captcha) | contador próprio |
| gasto com mensagens, conversão de OTP, taxa de recusa de cartão | painel de custos/abuso |
| certificado perto de vencer | monitor externo / certbot |
| backup do dia ausente | checagem do arquivo mais recente |

## 3. Detecção de ataque (lacunas típicas)

- login bloqueado **sem log**; falha sem identificar a conta; nenhuma coleta de log **fora da VPS** (se o servidor é comprometido, o log local é apagado junto).
- Envio de logs para fora (journald remoto, Loki, serviço gerenciado) com retenção própria.

## 4. Painéis

Exemplos de painéis úteis: disponibilidade/latência, autenticação (sucesso/falha/lockout),
abuso (recusas por regra, modo observar), pagamentos (recusas, conciliação), mensagens (envios,
custo, conversão), segurança da VPS (bans, logins SSH).

## 5. Resposta

Alerta sem dono não funciona: definir quem recebe, em que canal, e o que fazer (runbook —
ver [operacao](../operacao/README.md)).
