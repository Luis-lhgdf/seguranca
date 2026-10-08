# Repositórios de referência

> **Revisado em:** 2026-10-08 · **Origem:** API pública do GitHub (estrelas, último push, licença
> consultados nesta data) e páginas oficiais dos projetos. Nada foi clonado, baixado ou executado.

Objetivo: ver como os projetos mais respeitados de segurança organizam conteúdo e o que vale adotar
nesta base. Números de estrelas são aproximados e mudam; o "último push" indica atividade, não
qualidade.

**Juízo de confiança:** **oficial** = mantido pela organização dona do padrão (OWASP, MITRE, Mozilla,
fundação/empresa do produto); **comunidade confiável** = autor reconhecido, anos de histórico,
muito usado; **cuidado** = útil, mas com licença restritiva, conteúdo ofensivo bruto ou manutenção
parada.

## Bases, padrões e guias

| Repositório | Dono | ★ | Último push | Licença | O que oferece | Confiança |
|---|---|---|---|---|---|---|
| [OWASP/CheatSheetSeries](https://github.com/OWASP/CheatSheetSeries) | OWASP | ~33,5 mil | 2026-10 | CC BY-SA 4.0 | ~100 cheat sheets curtas, uma por assunto (sessão, CSP, upload, SSRF…) | oficial |
| [OWASP/wstg](https://github.com/OWASP/wstg) | OWASP | ~10 mil | 2026-10 | CC BY-SA 4.0 | Web Security Testing Guide: metodologia de teste com IDs `WSTG-<CAT>-NN` (v4.2 estável, v5 em desenvolvimento) | oficial |
| [OWASP/ASVS](https://github.com/OWASP/ASVS) | OWASP | ~3,7 mil | 2026-10 | CC BY-SA 4.0 | Requisitos verificáveis por nível (L1–L3), v5.0 | oficial |
| [OWASP/Top10](https://github.com/OWASP/Top10) | OWASP | ~6,2 mil | 2026-09 | CC BY-SA (site) | Top 10:2025 (lançado em nov/2025; entrou *Software Supply Chain Failures* e *Mishandling of Exceptional Conditions*; SSRF foi para A01) | oficial |
| [OWASP/API-Security](https://github.com/OWASP/API-Security) | OWASP | ~2,4 mil | 2026-09 | CC BY-SA (site) | API Security Top 10 (edição 2023 ainda vigente) | oficial |
| [OWASP/mastg](https://github.com/OWASP/mastg) e [OWASP/masvs](https://github.com/OWASP/masvs) | OWASP | ~13 mil / ~2,5 mil | 2026-10 / 2026-09 | CC BY-SA 4.0 | Padrão e guia de teste mobile (só referência aqui) | oficial |
| [OWASP/www-project-secure-headers](https://github.com/OWASP/www-project-secure-headers) | OWASP | ~200 | 2026-10 | Apache-2.0 | Valores recomendados de cabeçalhos, lista de cabeçalhos a remover | oficial |
| [mitre-attack/attack-stix-data](https://github.com/mitre-attack/attack-stix-data) | MITRE | ~700 | 2026-08 | termos MITRE | ATT&CK em STIX (táticas/técnicas de adversário) — referência para logs e detecção | oficial |

## Hardening de servidor e TLS

| Repositório | Dono | ★ | Último push | Licença | O que oferece | Confiança |
|---|---|---|---|---|---|---|
| [dev-sec/ansible-collection-hardening](https://github.com/dev-sec/ansible-collection-hardening) | DevSec Project | ~5,5 mil | 2026-10 | Apache-2.0 | Baselines testadas para Linux, SSH, nginx, MySQL (+ perfis InSpec/cinc-auditor para verificar) | comunidade confiável |
| [CISOfy/lynis](https://github.com/CISOfy/lynis) | CISOfy | ~16,4 mil | 2026-09 | GPL-3.0 | Auditoria local de Linux, sem agente; índice de hardening e sugestões com ID | comunidade confiável |
| [mozilla/ssl-config-generator](https://github.com/mozilla/ssl-config-generator) → [tlsref/configurator](https://github.com/tlsref/configurator) | Mozilla → tlsref | ~440 → novo | 2026-05 (arquivado) / 2026-10 | MPL-2.0 | Perfis TLS *modern/intermediate/old* por servidor. O repositório da Mozilla foi **arquivado** e aponta para o novo endereço | oficial (migração recente: conferir) |
| CIS Benchmarks (cisecurity.org, não é GitHub) | CIS | — | contínuo | gratuito p/ uso não comercial, cadastro | Benchmarks de Ubuntu, Debian, nginx, Docker, PostgreSQL | oficial |

## Conteúdo ofensivo e listas (consulta, nunca copiar payload para cá)

| Repositório | Dono | ★ | Último push | Licença | O que oferece | Confiança |
|---|---|---|---|---|---|---|
| [swisskyrepo/PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings) | swisskyrepo | ~81,5 mil | 2026-08 | MIT | Uma pasta por classe de vulnerabilidade: resumo, metodologia, payloads, referências | comunidade confiável (conteúdo ofensivo) |
| [HackTricks-wiki/hacktricks](https://github.com/HackTricks-wiki/hacktricks) | Carlos Polop | ~12,5 mil | 2026-10 | licença própria (sem SPDX; restringe uso comercial) | Wiki enorme de técnicas por tecnologia/porta | **cuidado** (licença; não reproduzir texto) |
| [danielmiessler/SecLists](https://github.com/danielmiessler/SecLists) | Daniel Miessler | ~74 mil | 2026-10 | MIT | Wordlists (diretórios, parâmetros, senhas, fuzzing) — contém web shells e amostras que antivírus detecta | comunidade confiável (**cuidado** ao baixar) |
| [enaqx/awesome-pentest](https://github.com/enaqx/awesome-pentest) | enaqx | ~27 mil | 2026-07 | sem SPDX | Índice de ferramentas/recursos de pentest por categoria | comunidade confiável (só índice) |
| [qazbnm456/awesome-web-security](https://github.com/qazbnm456/awesome-web-security) | qazbnm456 | ~13,9 mil | 2026-09 | sem SPDX | Índice de material de segurança web por classe (XSS, SSRF, CSP…) | comunidade confiável (só índice) |
| [trimstray/the-book-of-secret-knowledge](https://github.com/trimstray/the-book-of-secret-knowledge) | trimstray | ~250 mil | **2024-11** | MIT | One-liners, ferramentas e manuais de sysadmin/segurança | **cuidado** (parado desde 2024) |

## O que adotar de cada um

### Organização
- **WSTG — IDs estáveis por categoria de teste** (`WSTG-INFO`, `-CONF`, `-IDNT`, `-ATHN`, `-ATHZ`,
  `-SESS`, `-INPV`, `-ERRH`, `-CRYP`, `-BUSL`, `-CLNT`, `-APIT`) e, em cada teste, a sequência
  *Resumo → Objetivos → Como testar → Remediação → Ferramentas → Referências*. Já temos IDs
  `SEC-*` estáveis; falta o eixo "teste ativo" e o mapeamento cruzado.
- **Cheat Sheet Series — um assunto por arquivo, curto, com índice por tema e por Top 10/ASVS**.
  Já seguimos isso; adotar o "índice reverso" (de Top 10:2025 e ASVS para nossos arquivos).
- **ASVS — nível por requisito (L1/L2/L3)**. Hoje o nível é decidido por projeto; marcar o nível em
  cada item `SEC-*` permitiria filtrar o checklist por nível.
- **PayloadsAllTheThings — pasta por classe com `README` padronizado** (resumo, metodologia, como
  detectar, referências). Bom modelo para `pentest/classes/`, **sem** a parte de payloads em massa.
- **awesome-* — curadoria com critério explícito de entrada**. Copiar a ideia de um
  `CONTRIBUTING.md` com critérios (fonte oficial, licença, atividade) quando o repositório abrir.
- **dev-sec — "baseline + teste que verifica a baseline"**. Cada regra de hardening tem um controle
  automatizado; casa com nosso "Como verificar / OK quando".

### Conteúdo
- **Top 10:2025**: atualizar `base/fundamentos/` com as categorias novas (supply chain já coberta em
  `SEC-DEP-*`; *exceptional conditions* → reforçar `SEC-API-07`, fail-open/fail-closed em
  `SEC-CAP-06`).
- **WSTG**: preencher lacunas que nossa base cobre pouco — lógica de negócio (`WSTG-BUSL`: limites de
  fluxo, replay, ordem de passos), testes de cliente (`WSTG-CLNT`: clickjacking, CORS, postMessage,
  open redirect), fingerprinting/descoberta (`WSTG-INFO`), métodos HTTP e arquivos esquecidos
  (`WSTG-CONF`).
- **API Security Top 10 2023**: conferir cobertura de API6 (*Unrestricted Access to Sensitive
  Business Flows*) e API9 (*Improper Inventory Management*: versões antigas de API e rotas de debug).
- **Secure Headers**: lista de cabeçalhos a **remover** e valores de referência para `SEC-NAV-*`.
- **Lynis/CIS/dev-sec**: usar como baseline externa citada em `SEC-VPS-10` e `SEC-VPS-15`.
- **MITRE ATT&CK**: só como vocabulário para `base/logs/` (o que detectar), não como checklist.

### O que **não** adotar
- Payloads e wordlists dentro do repositório (risco de antivírus, de má reputação ao abrir o código e
  de uso fora do escopo). Referenciar por link.
- Texto de HackTricks (licença própria). Citar link, escrever com palavras próprias.
- Conteúdo de red team/pós-exploração (persistência, evasão, movimento lateral): fora do escopo de
  "dono auditando o próprio sistema".
