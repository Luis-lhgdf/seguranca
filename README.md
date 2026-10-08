# Segurança — base de conhecimento e checklist de auditoria

Base de conhecimento de segurança **genérica e reutilizável** para qualquer site ou sistema web,
mais um **checklist** que um agente de IA (Claude Code ou similar) percorre item a item num
projeto: decide se cada item se aplica, testa, registra a evidência e propõe correções.

Conteúdo compilado de **fontes públicas da internet** — OWASP (Top 10, API Security Top 10, ASVS,
Cheat Sheets), NIST, CWE, documentação oficial de frameworks e ferramentas, avisos de CVE e artigos
técnicos — organizado como regra + parâmetros + trade-offs, com os links das fontes em cada
`referencias.md`.

## Estrutura

```
AGENTS.md            protocolo do agente auditor (CLAUDE.md só importa este arquivo)
checklist/INDICE.md  ordem dos temas e contagem de itens
checklist/mapeamentos.md  item SEC-* → Top 10:2025, ASVS 5.0 (nível), WSTG, API Top 10
base/<tema>/         um tema por pasta:
  README.md            o que cobre, quando se aplica, índice
  <conteudo>.md        arquivos curtos (até ~150-200 linhas)
  referencias.md       fontes oficiais (OWASP, ASVS, docs, CVEs)
  checklist.md         itens SEC-<AREA>-NN
relatorios/MODELO.md modelo do relatório
relatorios/<projeto>/<AAAA-MM-DD>.md   relatórios gerados (locais, fora do Git)
scripts/verificar-links.py   confere links e âncoras entre os .md
pesquisa/            estudos de apoio (ex.: repositórios de referência)
```

Temas: `fundamentos` (contexto, sem checklist) · `dependencias` · `segredos` · `autenticacao` ·
`sessao` · `api` · `upload` · `headers` · `banco` · `pagamentos` · `mensageria` · `rate-limit` ·
`captcha` · `infra-vps` · `nginx-tls` · `copias-de-seguranca` · `logs` · `privacidade` · `operacao`.

## Como usar

**Agente (auditoria):** abra o Claude Code nesta pasta (ou aponte o agente para ela) e peça, por
exemplo: *"Audite o projeto em `C:\...\meu-projeto` (site `https://...`, VPS `meu-alias`) seguindo
o AGENTS.md."* O agente começa entendendo o cenário, faz o inventário de versões (com pesquisa na
web), percorre os checklists na ordem e grava o relatório em `relatorios/<projeto>/<data>.md`.
Por padrão ele só **lê** produção; qualquer teste de escrita, carga ou varredura exige sua
autorização na conversa.

**Relatórios ficam locais.** `relatorios/<projeto>/` está no `.gitignore`: um relatório de auditoria
descreve infraestrutura real (rotas, versões, falhas abertas) e não deve ir para o Git nem para um
repositório público. Só `relatorios/MODELO.md` é versionado.

**Humano (consulta):** comece pelo `README.md` do tema; cada um aponta os arquivos de conteúdo e as
fontes. Para uma visão geral, `base/fundamentos/`. Para partir de uma categoria do OWASP Top 10, de um
requisito do ASVS ou de um teste do WSTG, use [`checklist/mapeamentos.md`](checklist/mapeamentos.md).

## Como adicionar conhecimento

1. Escolha o tema (ou crie `base/<tema-novo>/` com `README.md`, `referencias.md` e `checklist.md`).
2. Um assunto por arquivo; se passar de ~200 linhas, quebre em dois.
3. Primeira linha após o título: `> **Revisado em:** AAAA-MM-DD · **Origem:** ...`. Atualize a data a cada revisão.
4. Generalize: regra primeiro, exemplo genérico depois ("uma loja virtual", "um site institucional"). Mantenha números medidos, parâmetros e links. **Nunca** inclua nome de projeto ou cliente, caminho local, segredo, IP de servidor, domínio privado, e-mail ou dado pessoal.
5. Toda recomendação acionável vira item no `checklist.md` do tema, no formato do [`checklist/INDICE.md`](checklist/INDICE.md), com o próximo número livre; atualize a contagem no índice e o mapeamento (linha **Mapeamento** e [`checklist/mapeamentos.md`](checklist/mapeamentos.md)), conferindo os IDs na fonte oficial.
6. Fontes oficiais no `referencias.md` do tema.
7. Rode `python scripts/verificar-links.py` (precisa dar 0 problemas) e faça commit em português.

## Origem do conteúdo

Tudo aqui foi compilado de fontes públicas: OWASP (Top 10, API Security Top 10, ASVS v5, Cheat
Sheet Series, WSTG, Automated Threats), NIST (SP 800-63B e outras), CWE/MITRE, documentação oficial
de frameworks, bancos, servidores web e provedores, avisos de CVE/GHSA e artigos técnicos. As fontes
de cada tema estão no respectivo `referencias.md`; a visão geral está em
[`base/fundamentos/referencias-gerais.md`](base/fundamentos/referencias-gerais.md).
