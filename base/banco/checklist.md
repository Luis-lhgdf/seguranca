# Checklist — Banco de dados (BD)

> **Revisado em:** 2026-10-07. Variáveis e regras em [`AGENTS.md`](../../AGENTS.md). Em produção, **só consultas de leitura** e com autorização; testes de concorrência só em ambiente de teste.

### SEC-BD-01 — Nenhuma query montada com texto do usuário
- **Aplica-se quando:** há banco SQL.
- **Risco se faltar:** SQL injection — leitura ou destruição do banco inteiro.
- **Como verificar:** grep da seção 1 de [consultas-e-transacoes.md](consultas-e-transacoes.md#1-sql-injection); em teste, `' OR 1=1--` em busca/login.
- **OK quando:** só ORM/bind params; SQL textual apenas literal fixo.
- **Referência:** [consultas-e-transacoes.md#1-sql-injection](consultas-e-transacoes.md#1-sql-injection) · ASVS V1.2.4.

### SEC-BD-02 — Ordenação/coluna dinâmica por allowlist
- **Aplica-se quando:** listagens com `order_by` vindo do cliente.
- **Risco se faltar:** injeção pelo nome de coluna, que o ORM não protege.
- **Como verificar:** localizar `order_by` nos serviços; conferir dicionário-allowlist e `pattern` na direção.
- **OK quando:** valor fora da lista cai no default.
- **Referência:** [consultas-e-transacoes.md#1-sql-injection](consultas-e-transacoes.md#1-sql-injection).

### SEC-BD-03 — Operações de consumo atômicas
- **Aplica-se quando:** há saldo, estoque, voucher, cupom, reembolso ou qualquer recurso de uso único.
- **Risco se faltar:** requisições simultâneas usam o mesmo recurso várias vezes.
- **Como verificar:** ler o fluxo (`FOR UPDATE`, update condicional, índice único); em teste, 20 requisições paralelas (`xargs -P 20 curl ...`) → 1 sucesso.
- **OK quando:** check+uso atômico e teste de concorrência existente.
- **Referência:** [consultas-e-transacoes.md#2-concorrência-toctou-e-idempotência](consultas-e-transacoes.md#2-concorrência-toctou-e-idempotência) · ASVS V15.4.2.

### SEC-BD-04 — Dinheiro em tipo decimal
- **Aplica-se quando:** há valor monetário.
- **Risco se faltar:** arredondamento errado em cobrança ou exibição.
- **Como verificar:** `grep -rnE "Float|float\(|DOUBLE|REAL" $REPO/<models>` nos campos de preço/valor.
- **OK quando:** `NUMERIC/DECIMAL` + `Decimal`; `float` só para formatação.
- **Referência:** [consultas-e-transacoes.md#3-tipos-e-integridade](consultas-e-transacoes.md#3-tipos-e-integridade).

### SEC-BD-05 — Unicidade garantida no banco
- **Aplica-se quando:** há regra "um por pessoa" (e-mail, CPF, telefone verificado, chave de idempotência).
- **Risco se faltar:** duas requisições simultâneas criam duplicata.
- **Como verificar:** ler migrations/índices (`UNIQUE`, índice parcial).
- **OK quando:** índice único para cada regra de unicidade.
- **Referência:** [consultas-e-transacoes.md#3-tipos-e-integridade](consultas-e-transacoes.md#3-tipos-e-integridade).

### SEC-BD-06 — Banco e Redis inacessíveis pela internet
- **Aplica-se quando:** há banco/Redis em VPS ou Docker.
- **Risco se faltar:** o banco fica a uma senha (ou nenhuma) de distância de qualquer um.
- **Como verificar:** `ssh $VPS 'sudo ss -tlnp | grep -E ":(3306|33060|5432|6379)"'`; ler `ports:` do compose; de fora, `nc -zvw3 <host> 3306`.
- **OK quando:** só loopback/rede interna; conexão externa recusada.
- **Referência:** [acesso-e-privilegios.md#1-rede](acesso-e-privilegios.md#1-rede).

### SEC-BD-07 — Usuário da aplicação com privilégio mínimo
- **Aplica-se quando:** há banco.
- **Risco se faltar:** uma injeção ou credencial vazada pode apagar/alterar tudo.
- **Como verificar:** `SHOW GRANTS` / `\dp` (comando da seção 2) com autorização.
- **OK quando:** app só DML no próprio schema; DDL num usuário de migração separado (ou risco aceito por escrito).
- **Referência:** [acesso-e-privilegios.md#2-usuários-e-privilégios](acesso-e-privilegios.md#2-usuários-e-privilégios).

### SEC-BD-08 — Instalação endurecida
- **Aplica-se quando:** banco autogerenciado.
- **Risco se faltar:** usuário anônimo ou root remoto.
- **Como verificar:** `ssh $VPS "sudo mysql -e \"SELECT user,host FROM mysql.user\""` (sem anônimo, root só local); `SHOW DATABASES` sem `test`.
- **OK quando:** sem anônimos, sem `test`, root local.
- **Referência:** [acesso-e-privilegios.md#2-usuários-e-privilégios](acesso-e-privilegios.md#2-usuários-e-privilégios).

### SEC-BD-09 — Banco gerenciado com rede privada, TLS e backup
- **Aplica-se quando:** usa banco gerenciado na nuvem.
- **Risco se faltar:** instância exposta ou sem recuperação.
- **Como verificar:** console/CLI do provedor (acesso público, allowlist, TLS forçado, backup/PITR, logs).
- **OK quando:** os quatro atendidos.
- **Referência:** [acesso-e-privilegios.md#3-banco-gerenciado-na-nuvem-se-usar](acesso-e-privilegios.md#3-banco-gerenciado-na-nuvem-se-usar).

### SEC-BD-10 — RLS em banco acessado pelo front
- **Aplica-se quando:** o front fala direto com o banco (Supabase/Firebase/PostgREST).
- **Risco se faltar:** qualquer usuário lê e escreve qualquer tabela.
- **Como verificar:** listar tabelas e políticas (`select * from pg_policies`); checar RPCs expostas.
- **OK quando:** RLS em todas as tabelas expostas; RPCs restritas.
- **Referência:** [consultas-e-transacoes.md#4-supabase--banco-exposto-ao-cliente](consultas-e-transacoes.md#4-supabase--banco-exposto-ao-cliente).

### SEC-BD-11 — Entrada com null byte não vira 500
- **Aplica-se quando:** Postgres (e testar no MySQL).
- **Risco se faltar:** qualquer um provoca erro 500 e poluição de alerta.
- **Como verificar:** em teste, enviar `\u0000` num campo de texto → 422.
- **OK quando:** recusado na validação.
- **Referência:** [consultas-e-transacoes.md#3-tipos-e-integridade](consultas-e-transacoes.md#3-tipos-e-integridade).
