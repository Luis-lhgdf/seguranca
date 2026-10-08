# Banco: consultas, concorrência e tipos

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/CVE, confirme na fonte oficial antes de aplicar.

## 1. SQL injection

- ORM/prepared statements com bind params em **100%** das queries — inclusive upsert de integração e scripts de migração.
- `text()`/SQL cru com f-string ou concatenação: proibido. Exceção aceitável: literal fixo (`SELECT 1` de health check).
- **Nome de coluna não é parametrizável:** ordenação dinâmica por dicionário-allowlist (`_ORDER_FIELDS.get(order_by, default)`); direção com `pattern="^(asc|desc)$"`.
- `ilike(f"%{q}%")` com o valor como bind param é seguro (interpola o valor, não a query); limitar `max_length` de `q`.
- Driver com CVE sem correção (ex.: `asyncmy 0.2.11` / PYSEC-2026-286, SQLi via **chaves** de dict) — não explorável quando quem gera as chaves é o ORM; documentar e monitorar.
- NoSQL/LDAP/XPath: só se a stack tiver.
- Verificação: `grep -rnE "text\(|execute\(f\"|execute\(\".*%|\+ *\"(SELECT|UPDATE|DELETE|INSERT)" $REPO`.

## 2. Concorrência (TOCTOU) e idempotência

- Verificar e efetivar **no mesmo bloco atômico**: `SELECT ... FOR UPDATE`, incremento condicional (`UPDATE saldo SET v = v - :p WHERE v >= :p`), índice único, lock distribuído (Redis) com cuidado.
- Contadores públicos (view/clique): `INSERT ... ON DUPLICATE KEY UPDATE` / `ON CONFLICT` (sem lost update e sem crescer tabela).
- Idempotência com chave única em criação de pedido, pagamento, emissão de crédito/voucher, envio de mensagem.
- Teste: 20 requisições simultâneas → 1 sucesso.
- Rate limit com vários baldes: ler-decidir-gravar atômico (script Lua no Redis — `MULTI/EXEC` não ramifica).

## 3. Tipos e integridade

- **Dinheiro em `NUMERIC`/`DECIMAL`**, `Decimal` no código; `float` só para exibição.
- Postgres recusa `NUL` (`\x00`) em `TEXT`/`VARCHAR` → `DataError` → **500 provocável**; recusar na validação (422). MySQL se comporta diferente — testar.
- Regras de unicidade **no banco** (índice único, inclusive parcial — ex.: telefone único só entre verificados), não só no serviço.
- Referência a outra tabela checada antes do insert (404 claro em vez de 500 de FK).
- Soft delete preserva o dado indefinidamente — combinar com política de retenção ([privacidade](../privacidade/README.md)).

## 4. Supabase / banco exposto ao cliente

Se o front fala direto com o banco (Supabase, Firebase, PostgREST): **RLS obrigatório** em toda
tabela e RPC com permissão restrita — sem isso, qualquer usuário lê/escreve qualquer tabela. Se o
banco só é acessado pela API, N/A.
