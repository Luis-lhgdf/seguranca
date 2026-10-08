# Checklist — API e endpoints (API)

> **Revisado em:** 2026-10-07. Variáveis e regras em [`AGENTS.md`](../../AGENTS.md). A bateria de entrada (SEC-API-05) só roda em ambiente local/de teste.

### SEC-API-01 — Dono do recurso / autorização em toda rota autenticada
- **Aplica-se quando:** há rotas autenticadas.
- **Risco se faltar:** trocar um número na URL mostra dado de outra pessoa.
- **Como verificar:** listar rotas com parâmetro de id; ler se filtram pelo usuário da sessão ou usam `require(módulo, ação)`; em teste, usuário A pede recurso de B → 403/404; `grep -rnE "user_id|cliente_id" <schemas de entrada>` (não deve vir do corpo).
- **OK quando:** toda rota filtra por dono/permissão; id do usuário só da sessão.
- **Referência:** [autorizacao-e-exposicao.md#1-autorização-idorbola-bfla](autorizacao-e-exposicao.md#1-autorização-idorbola-bfla) · ASVS V8.2.1/V8.2.2 · API1.
- **Mapeamento:** nível L1 · Top 10 A01:2025 · ASVS V8.2.1 (L1), V8.2.2 (L1), V8.3.1 (L1) · WSTG-ATHZ-02, WSTG-ATHZ-04 · API1:2023.

### SEC-API-02 — Recurso mais sensível com permissão própria
- **Aplica-se quando:** o mesmo módulo guarda objetos de sensibilidade diferente (mídia pública × termo assinado).
- **Risco se faltar:** quem tem permissão genérica lê o documento sensível.
- **Como verificar:** ler as rotas que servem o objeto sensível e o guard aplicado após carregá-lo.
- **OK quando:** objeto sensível exige permissão dedicada/superuser e o acesso é auditado.
- **Referência:** [autorizacao-e-exposicao.md#1-autorização-idorbola-bfla](autorizacao-e-exposicao.md#1-autorização-idorbola-bfla).
- **Mapeamento:** nível L1 · Top 10 A01:2025 · ASVS V8.1.1 (L1), V8.2.2 (L1) · WSTG-ATHZ-03 · API5:2023.

### SEC-API-03 — Schema de saída explícito em toda rota
- **Aplica-se quando:** há API.
- **Risco se faltar:** a API devolve CPF, hash de senha ou dado de saúde que a tela nem usa.
- **Como verificar:** `grep -rn "@router\.\(get\|post\|put\|patch\|delete\)" $REPO -A3 | grep -c response_model` × total de rotas; `curl -s $API/<rota pública> | jq 'keys'` em cada rota pública.
- **OK quando:** toda rota com schema (exceções justificadas no docstring) e nenhum campo sensível no público.
- **Referência:** [autorizacao-e-exposicao.md#2-exposição-de-dados-na-resposta](autorizacao-e-exposicao.md#2-exposição-de-dados-na-resposta) · ASVS V15.3.1.
- **Mapeamento:** nível L1 · Top 10 A01:2025 · ASVS V15.3.1 (L1) · API3:2023.

### SEC-API-04 — Mass assignment bloqueado
- **Aplica-se quando:** há rotas de criação/edição.
- **Risco se faltar:** um campo extra vira admin ou muda preço.
- **Como verificar:** procurar `extra="forbid"`/`.strict()`; procurar `**payload`/`setattr` sobre model; em teste, `PATCH` com `{"is_superuser":true}`/`{"role":"admin"}` → 422 ou ignorado sem efeito.
- **OK quando:** campos privilegiados e derivados fora do schema; campo extra recusado (recomendado) ou comprovadamente ignorado.
- **Referência:** [autorizacao-e-exposicao.md#3-mass-assignment](autorizacao-e-exposicao.md#3-mass-assignment) · ASVS V15.3.3.
- **Mapeamento:** nível L2 · Top 10 A01:2025 · ASVS V15.3.3 (L2) · API3:2023.

### SEC-API-05 — Bateria de entrada nas rotas que aceitam dados
- **Aplica-se quando:** há rota que recebe entrada do cliente.
- **Risco se faltar:** erro 500 provocável, lixo no banco, DoS, injeção no destino final.
- **Como verificar:** em ambiente de teste, rodar campo a campo: `\x00`, 10 KB e 1 MB, vazio/espaços, `U+202E`, `U+200B`, homoglyph, `\r\n`, `<script>`, fórmula CSV, `{{7*7}}`, `../../etc/passwd`, `1.5`/`NaN` em inteiro, tipo trocado, campo a mais, JSON malformado.
- **OK quando:** tudo vira 422 (ou é guardado e escapado na saída, conforme a regra); nenhum 500.
- **Referência:** [endpoint-seguro.md#2-a-bateria-campo-a-campo-em-toda-rota-que-aceita-entrada](endpoint-seguro.md#2-a-bateria-campo-a-campo-em-toda-rota-que-aceita-entrada).
- **Mapeamento:** nível L1 · Top 10 A05:2025 · ASVS V2.2.1 (L1), V16.5.1 (L2) · WSTG-INPV-01, WSTG-INPV-05, WSTG-INPV-18.

### SEC-API-06 — `max_length` e limites em todo campo
- **Aplica-se quando:** há schemas de entrada.
- **Risco se faltar:** payload gigante polui o banco ou trava o processamento.
- **Como verificar:** listar campos `str`/`list`/`Any` sem limite nos schemas (`grep -rnE ": (str|list|Any)" <schemas>` e conferir `Field(max_length=...)`); filtros de query com `pattern`/`Literal`.
- **OK quando:** todo texto/lista com teto; `Any` substituído por tipo por chave; filtros fechados.
- **Referência:** [endpoint-seguro.md#passo-2--schema-de-entrada-com-teto-em-tudo](endpoint-seguro.md#passo-2--schema-de-entrada-com-teto-em-tudo).
- **Mapeamento:** nível L1 · Top 10 A06:2025 · ASVS V2.2.1 (L1), V15.2.2 (L2) · API4:2023.

### SEC-API-07 — Erros que não ensinam nada
- **Aplica-se quando:** há API.
- **Risco se faltar:** stack trace, SQL ou nome de coluna ajudam o atacante.
- **Como verificar:** provocar 422/404/500 em teste e ler a resposta; conferir handler global; `DEBUG` falso em produção.
- **OK quando:** mensagens genéricas, sem stack nem SQL.
- **Referência:** [endpoint-seguro.md#passo-7--erro-que-não-ensina-nada](endpoint-seguro.md#passo-7--erro-que-não-ensina-nada).
- **Mapeamento:** nível L2 · Top 10 A10:2025, A02:2025 · ASVS V16.5.1 (L2), V13.4.2 (L2) · WSTG-ERRH-01, WSTG-ERRH-02 · API8:2023.

### SEC-API-08 — Documentação interativa desligada em produção
- **Aplica-se quando:** framework gera `/docs`/OpenAPI.
- **Risco se faltar:** mapa completo da API para quem ataca.
- **Como verificar:** `for p in docs redoc openapi.json api/docs api/openapi.json; do curl -s -o /dev/null -w "$p %{http_code}\n" $SITE/$p; done`.
- **OK quando:** 404 em todos.
- **Referência:** [autorizacao-e-exposicao.md#4-superfície-e-configuração-da-api](autorizacao-e-exposicao.md#4-superfície-e-configuração-da-api).
- **Mapeamento:** nível L2 · Top 10 A02:2025 · ASVS V13.4.5 (L2) · WSTG-CONF-05, WSTG-INFO-06 · API9:2023.

### SEC-API-09 — CORS restrito
- **Aplica-se quando:** API acessada por navegador.
- **Risco se faltar:** qualquer site lê respostas autenticadas.
- **Como verificar:** `curl -si -H 'Origin: https://evil.example' $API/<rota> | grep -i access-control`; ler a config.
- **OK quando:** sem `Access-Control-Allow-Origin` para origem estranha; nunca `*` com credenciais.
- **Referência:** [autorizacao-e-exposicao.md#4-superfície-e-configuração-da-api](autorizacao-e-exposicao.md#4-superfície-e-configuração-da-api).
- **Mapeamento:** nível L1 · Top 10 A02:2025 · ASVS V3.4.2 (L1) · WSTG-CLNT-07 · API8:2023.

### SEC-API-10 — Limite de tamanho de corpo na borda e no app
- **Aplica-se quando:** há API.
- **Risco se faltar:** requisição enorme derruba o serviço.
- **Como verificar:** `ssh $VPS 'sudo nginx -T | grep -n client_max_body_size'`; ler middleware de limite (lida com chunked?).
- **OK quando:** teto na borda e no app, maior só onde precisa (upload).
- **Referência:** [autorizacao-e-exposicao.md#4-superfície-e-configuração-da-api](autorizacao-e-exposicao.md#4-superfície-e-configuração-da-api).
- **Mapeamento:** nível L1 · Top 10 A06:2025 · ASVS V5.2.1 (L1), V15.2.2 (L2) · API4:2023.

### SEC-API-11 — Campos derivados nunca aceitos do cliente
- **Aplica-se quando:** há preço, status, flag de compliance, slug, contador.
- **Risco se faltar:** o cliente muda preço ou publica sem a trava de compliance.
- **Como verificar:** listar campos calculados no serviço e conferir que não estão nos schemas de entrada; em teste, enviar o campo → sem efeito.
- **OK quando:** todos derivados no servidor.
- **Referência:** [../fundamentos/vulnerabilidades.md#v03-confiar-no-frontend-valor-ou-campo-de-compliance](../fundamentos/vulnerabilidades.md#v03-confiar-no-frontend-valor-ou-campo-de-compliance) · ASVS V2.2.2.
- **Mapeamento:** nível L1 · Top 10 A06:2025 · ASVS V2.2.2 (L1), V8.3.1 (L1) · WSTG-BUSL-01, WSTG-BUSL-02.

### SEC-API-12 — Integrações documentadas e com privilégio mínimo
- **Aplica-se quando:** há integração externa (entrada ou saída).
- **Risco se faltar:** credencial estática com poder demais; ninguém sabe o que conversa com o quê.
- **Como verificar:** procurar documento de integrações (destino, credencial, privilégio); ler escopo das credenciais de integração de escrita.
- **OK quando:** todas listadas; escrita externa com auth forte, allowlist, escopo mínimo e log.
- **Referência:** [autorizacao-e-exposicao.md#5-integrações-e-comunicação-entre-serviços-asvs-v1311-v1321-v1322](autorizacao-e-exposicao.md#5-integrações-e-comunicação-entre-serviços-asvs-v1311-v1321-v1322).
- **Mapeamento:** nível L2 · Top 10 A02:2025 · ASVS V13.1.1 (L2), V13.2.2 (L2) · API10:2023.

### SEC-API-13 — Saída segura contra SSRF
- **Aplica-se quando:** o backend faz requisição a URL que vem de fora.
- **Risco se faltar:** o servidor é usado para acessar a rede interna ou metadados da nuvem.
- **Como verificar:** `grep -rnE "requests\.|httpx\.|aiohttp|urlopen|fetch\(|axios" $REPO/<backend>` e classificar; ler a função de validação (HTTPS, allowlist, `is_global`, CGNAT, sem redirect); rodar os testes.
- **OK quando:** toda URL externa passa pela saída segura e os testes de IP interno/CGNAT existem.
- **Referência:** [ssrf.md#2-defesa--função-central-de-saída-segura](ssrf.md#2-defesa--função-central-de-saída-segura) · ASVS V1.3.6.
- **Mapeamento:** nível L2 · Top 10 A01:2025 · ASVS V1.3.6 (L2), V13.2.5 (L2), V15.3.2 (L2) · WSTG-INPV-19 · API7:2023.

### SEC-API-14 — URL de imagem/link limitada a hosts permitidos
- **Aplica-se quando:** campo aceita URL de imagem/arte/avatar exibida a visitantes.
- **Risco se faltar:** tracker de IP de visitantes ou home pichada.
- **Como verificar:** em teste, gravar imagem de `https://evil.example/x.png` → 422; conferir `remotePatterns`.
- **OK quando:** allowlist de host; `data:` recusado.
- **Referência:** [ssrf.md#4-variante-no-front-tracker-de-ip-e-host-de-imagem-livre](ssrf.md#4-variante-no-front-tracker-de-ip-e-host-de-imagem-livre).
- **Mapeamento:** nível L2 · Top 10 A01:2025 · ASVS V1.3.6 (L2), V13.2.4 (L2) · WSTG-INPV-19 · API7:2023.

### SEC-API-15 — Framework do front fora de CVE de bypass de middleware
- **Aplica-se quando:** usa Next.js com `middleware.ts`.
- **Risco se faltar:** header forjado pula a checagem de acesso.
- **Como verificar:** versão do `next` no lockfile; existência de `middleware.ts`; a API autoriza sozinha?
- **OK quando:** versão corrigida e middleware não é a única autorização.
- **Referência:** [autorizacao-e-exposicao.md#1-autorização-idorbola-bfla](autorizacao-e-exposicao.md#1-autorização-idorbola-bfla).
- **Mapeamento:** nível L1 · Top 10 A03:2025, A01:2025 · ASVS V15.2.1 (L1) · WSTG-ATHZ-02.
