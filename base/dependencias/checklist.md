# Checklist — Dependências e versões (DEP)

> **Revisado em:** 2026-10-07. Variáveis e regras em [`AGENTS.md`](../../AGENTS.md). Comandos de leitura apenas; nada de `audit fix`/`upgrade` sem autorização. **Pesquisar na web** versão atual e CVEs na data da auditoria.

### SEC-DEP-01 — Inventário de versões completo
- **Aplica-se quando:** sempre.
- **Risco se faltar:** não dá para saber se há CVE no que está rodando.
- **Como verificar:** preencher a tabela da seção 1 de [inventario-e-decisao.md](inventario-e-decisao.md#1-inventário-o-que-levantar-em-todo-projeto) a partir de lockfiles e do servidor.
- **OK quando:** todas as camadas com versão **em uso** registrada no relatório.
- **Referência:** [inventario-e-decisao.md#1-inventário-o-que-levantar-em-todo-projeto](inventario-e-decisao.md#1-inventário-o-que-levantar-em-todo-projeto).
- **Mapeamento:** nível L2 · Top 10 A03:2025 · ASVS V15.1.2 (L2) · WSTG-INFO-02, WSTG-INFO-08 · API9:2023.

### SEC-DEP-02 — Versões conferidas na fonte oficial (atual, EOL, CVE)
- **Aplica-se quando:** sempre.
- **Risco se faltar:** software fora de suporte ou com falha conhecida em produção.
- **Como verificar:** para cada item crítico, consultar releases oficiais, endoflife.date, GitHub Advisory/OSV/USN; anotar link e data.
- **OK quando:** nenhum componente EOL e nenhuma CVE alta/crítica explorável sem plano.
- **Referência:** [inventario-e-decisao.md#2-checar-na-fonte-oficial--sempre-na-web-na-data-da-auditoria](inventario-e-decisao.md#2-checar-na-fonte-oficial--sempre-na-web-na-data-da-auditoria).
- **Mapeamento:** nível L1 · Top 10 A03:2025 · ASVS V15.1.1 (L1), V15.2.1 (L1).

### SEC-DEP-03 — Sem vulnerabilidade alta/crítica nas dependências JS
- **Aplica-se quando:** há `package.json`.
- **Risco se faltar:** falha conhecida explorável no front/SSR ou no build.
- **Como verificar:** `npm audit --omit=dev --audit-level=high` e `npm audit --audit-level=high`.
- **OK quando:** zero high/critical em produção; demais com justificativa.
- **Referência:** [por-ecossistema.md#1-node--npm-e-pnpmyarn](por-ecossistema.md#1-node--npm-e-pnpmyarn).
- **Mapeamento:** nível L1 · Top 10 A03:2025 · ASVS V15.2.1 (L1).

### SEC-DEP-04 — Sem vulnerabilidade alta/crítica nas dependências Python
- **Aplica-se quando:** há projeto Python.
- **Risco se faltar:** falha conhecida explorável no backend.
- **Como verificar:** `pip-audit` sobre o lock exportado (seção 2 de [por-ecossistema.md](por-ecossistema.md#2-python-uv-pip-poetry)).
- **OK quando:** zero alta/crítica; sem correção upstream = documentado como não explorável.
- **Referência:** [por-ecossistema.md#2-python-uv-pip-poetry](por-ecossistema.md#2-python-uv-pip-poetry).
- **Mapeamento:** nível L1 · Top 10 A03:2025 · ASVS V15.2.1 (L1).

### SEC-DEP-05 — Pacotes do SO e imagens Docker em dia
- **Aplica-se quando:** VPS própria ou Docker.
- **Risco se faltar:** CVE de nginx/openssl/openssh/kernel abertas.
- **Como verificar:** comandos das seções 3 e 4 de [por-ecossistema.md](por-ecossistema.md#3-pacotes-do-sistema-ubuntudebian).
- **OK quando:** sem pendência de segurança antiga; imagens base sem CVE crítica.
- **Referência:** [por-ecossistema.md#3-pacotes-do-sistema-ubuntudebian](por-ecossistema.md#3-pacotes-do-sistema-ubuntudebian).
- **Mapeamento:** nível L1 · Top 10 A03:2025, A02:2025 · ASVS V15.2.1 (L1).

### SEC-DEP-06 — Recomendação de subir/voltar justificada
- **Aplica-se quando:** algum item de SEC-DEP-02 a 05 falhou ou há EOL próximo.
- **Risco se faltar:** atualização às cegas quebra produção; ou nada é atualizado.
- **Como verificar:** para cada componente, aplicar a matriz da seção 3.
- **OK quando:** cada recomendação traz atual → alvo, motivo com link, risco e validação.
- **Referência:** [inventario-e-decisao.md#3-decidir-manter-subir-ou-voltar](inventario-e-decisao.md#3-decidir-manter-subir-ou-voltar).
- **Mapeamento:** nível L1 · Top 10 A03:2025 · ASVS V15.1.1 (L1).

### SEC-DEP-07 — Gate de segurança no CI antes do deploy
- **Aplica-se quando:** há CI/CD.
- **Risco se faltar:** push vai direto para produção sem teste nem auditoria.
- **Como verificar:** ler `.github/workflows/*`: testes, audit, SAST e secret scan rodam e bloqueiam antes do deploy?
- **OK quando:** os quatro presentes e bloqueantes.
- **Referência:** [ci-e-supply-chain.md#1-gate-antes-do-deploy](ci-e-supply-chain.md#1-gate-antes-do-deploy).
- **Mapeamento:** nível L1 · Top 10 A03:2025, A08:2025 · ASVS V15.2.1 (L1).

### SEC-DEP-08 — Atualização automática configurada (Dependabot/Renovate)
- **Aplica-se quando:** repositório no GitHub/GitLab.
- **Risco se faltar:** atualizações dependem de alguém lembrar.
- **Como verificar:** `cat $REPO/.github/dependabot.yml` (ecossistemas cobertos, frequência, major isolado).
- **OK quando:** todos os ecossistemas do repo cobertos.
- **Referência:** [ci-e-supply-chain.md#2-atualização-contínua](ci-e-supply-chain.md#2-atualização-contínua).
- **Mapeamento:** nível L1 · Top 10 A03:2025 · ASVS V15.2.1 (L1).

### SEC-DEP-09 — Lockfile commitado e instalação determinística
- **Aplica-se quando:** sempre.
- **Risco se faltar:** cada deploy instala versões diferentes (porta para supply chain).
- **Como verificar:** lockfiles no git; scripts de deploy usam `npm ci`/`uv sync --frozen`.
- **OK quando:** os dois.
- **Referência:** [ci-e-supply-chain.md#3-supply-chain](ci-e-supply-chain.md#3-supply-chain).
- **Mapeamento:** nível L3 · Top 10 A03:2025, A08:2025 · ASVS V15.2.4 (L3).

### SEC-DEP-10 — SAST ativo
- **Aplica-se quando:** há código próprio.
- **Risco se faltar:** padrões inseguros (eval, SQL cru, segredo hardcoded) passam no review.
- **Como verificar:** Ruff com `S` no `pyproject.toml` / Bandit / Semgrep no CI; rodar uma vez localmente.
- **OK quando:** configurado e sem achado alto aberto.
- **Referência:** [ci-e-supply-chain.md#1-gate-antes-do-deploy](ci-e-supply-chain.md#1-gate-antes-do-deploy).
- **Mapeamento:** Top 10 A06:2025 · sem requisito ASVS direto.

### SEC-DEP-11 — Prazos de remediação e SBOM
- **Aplica-se quando:** produção (L2+).
- **Risco se faltar:** CVE conhecida fica aberta indefinidamente.
- **Como verificar:** procurar política de prazos e geração de SBOM.
- **OK quando:** prazos escritos por severidade; SBOM gerado (recomendado).
- **Referência:** [ci-e-supply-chain.md#4-sbom-e-prazos](ci-e-supply-chain.md#4-sbom-e-prazos) · ASVS V15.1.1/V15.1.2.
- **Mapeamento:** nível L1 · Top 10 A03:2025 · ASVS V15.1.1 (L1), V15.1.2 (L2).
