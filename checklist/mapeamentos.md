# Mapeamentos — itens `SEC-*` × OWASP Top 10, ASVS, WSTG e API Top 10

> **Revisado em:** 2026-10-08 · **Origem:** OWASP Top 10:2025, ASVS 5.0.0 (CSV oficial da tag
> `v5.0.0`), WSTG v4.2 (versão estável) e API Security Top 10:2023. Os IDs foram conferidos
> nas fontes nesta data; ao citar um ID novo, confira de novo na fonte.

Para que serve: filtrar o checklist por nível ASVS, citar a referência oficial no relatório e
achar quais itens cobrem uma categoria do Top 10 ou um teste do WSTG. O mesmo mapeamento aparece
na linha **Mapeamento** de cada item, dentro do `checklist.md` do tema.

## Como ler

- **Nível** — o menor nível ASVS entre os requisitos citados: `L1` vale para todo projeto, `L2` é o
  piso desta base para sistema com login e dado pessoal, `L3` só nos fluxos de dinheiro ou dado
  sensível (ver [asvs.md](../base/fundamentos/asvs.md#1-como-escolher-o-nível)). Item `L3` é
  obrigatório nos fluxos L3 e recomendado nos demais (ver [AGENTS.md](../AGENTS.md#etapa-3--contexto-da-base)).
- **—** — sem correspondência direta. É o caso de quase tudo de servidor, backup e operação: o ASVS
  trata da aplicação, não do sistema operacional. Para esses itens a baseline externa é CIS
  Benchmarks, Lynis e dev-sec (ver [infra-vps/referencias.md](../base/infra-vps/referencias.md)).
- **Aproximação** — o mapeamento aponta o requisito ou teste mais próximo; o critério que vale para
  `OK`/`FALHA` continua sendo o "OK quando" do item.
- **WSTG** — IDs da v4.2 estável. A v5, em desenvolvimento, renomeia `INPV` para `INJT` e acrescenta
  testes (CSP, MFA, OAuth, JWT, mass assignment); atualizar quando for publicada.
- **ASVS** — numeração da v5.0, diferente da v4.x (Autorização é V8, API é V4).

## Legenda — OWASP Top 10:2025

| ID | Categoria | Itens |
|---|---|---|
| [A01](https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/) | Broken Access Control | 20 |
| [A02](https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/) | Security Misconfiguration | 47 |
| [A03](https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/) | Software Supply Chain Failures | 16 |
| [A04](https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/) | Cryptographic Failures | 19 |
| [A05](https://owasp.org/Top10/2025/A05_2025-Injection/) | Injection | 11 |
| [A06](https://owasp.org/Top10/2025/A06_2025-Insecure_Design/) | Insecure Design | 40 |
| [A07](https://owasp.org/Top10/2025/A07_2025-Authentication_Failures/) | Authentication Failures | 33 |
| [A08](https://owasp.org/Top10/2025/A08_2025-Software_or_Data_Integrity_Failures/) | Software or Data Integrity Failures | 7 |
| [A09](https://owasp.org/Top10/2025/A09_2025-Security_Logging_and_Alerting_Failures/) | Security Logging and Alerting Failures | 15 |
| [A10](https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/) | Mishandling of Exceptional Conditions | 6 |

API Security Top 10:2023: API1 Broken Object Level Authorization · API2 Broken Authentication · API3 Broken Object Property Level Authorization · API4 Unrestricted Resource Consumption · API5 Broken Function Level Authorization · API6 Unrestricted Access to Sensitive Business Flows · API7 Server Side Request Forgery · API8 Security Misconfiguration · API9 Improper Inventory Management · API10 Unsafe Consumption of APIs — https://owasp.org/API-Security/editions/2023/en/0x11-t10/

## 1. Dependências e versões (`SEC-DEP`)

| Item | Nível | Top 10:2025 | ASVS 5.0 | WSTG v4.2 | API:2023 |
|---|---|---|---|---|---|
| [SEC-DEP-01](../base/dependencias/checklist.md#sec-dep-01--inventário-de-versões-completo) | L2 | A03 | V15.1.2 (L2) | INFO-02, INFO-08 | API9 |
| [SEC-DEP-02](../base/dependencias/checklist.md#sec-dep-02--versões-conferidas-na-fonte-oficial-atual-eol-cve) | L1 | A03 | V15.1.1 (L1), V15.2.1 (L1) | — | — |
| [SEC-DEP-03](../base/dependencias/checklist.md#sec-dep-03--sem-vulnerabilidade-altacrítica-nas-dependências-js) | L1 | A03 | V15.2.1 (L1) | — | — |
| [SEC-DEP-04](../base/dependencias/checklist.md#sec-dep-04--sem-vulnerabilidade-altacrítica-nas-dependências-python) | L1 | A03 | V15.2.1 (L1) | — | — |
| [SEC-DEP-05](../base/dependencias/checklist.md#sec-dep-05--pacotes-do-so-e-imagens-docker-em-dia) | L1 | A03, A02 | V15.2.1 (L1) | — | — |
| [SEC-DEP-06](../base/dependencias/checklist.md#sec-dep-06--recomendação-de-subirvoltar-justificada) | L1 | A03 | V15.1.1 (L1) | — | — |
| [SEC-DEP-07](../base/dependencias/checklist.md#sec-dep-07--gate-de-segurança-no-ci-antes-do-deploy) | L1 | A03, A08 | V15.2.1 (L1) | — | — |
| [SEC-DEP-08](../base/dependencias/checklist.md#sec-dep-08--atualização-automática-configurada-dependabotrenovate) | L1 | A03 | V15.2.1 (L1) | — | — |
| [SEC-DEP-09](../base/dependencias/checklist.md#sec-dep-09--lockfile-commitado-e-instalação-determinística) | L3 | A03, A08 | V15.2.4 (L3) | — | — |
| [SEC-DEP-10](../base/dependencias/checklist.md#sec-dep-10--sast-ativo) | — | A06 | — | — | — |
| [SEC-DEP-11](../base/dependencias/checklist.md#sec-dep-11--prazos-de-remediação-e-sbom) | L1 | A03 | V15.1.1 (L1), V15.1.2 (L2) | — | — |

## 2. Segredos e configuração (`SEC-SEG`)

| Item | Nível | Top 10:2025 | ASVS 5.0 | WSTG v4.2 | API:2023 |
|---|---|---|---|---|---|
| [SEC-SEG-01](../base/segredos/checklist.md#sec-seg-01--nenhum-segredo-no-histórico-do-git) | L2 | A02, A04 | V13.3.1 (L2) | — | — |
| [SEC-SEG-02](../base/segredos/checklist.md#sec-seg-02--gitignore-correto-e-sem-regra-que-esconda-o-que-deve-ser-versionado) | L1 | A02 | V13.4.1 (L1) | CONF-04 | — |
| [SEC-SEG-03](../base/segredos/checklist.md#sec-seg-03--nenhum-segredo-no-bundle-do-front) | L2 | A02 | V13.3.1 (L2) | INFO-05 | — |
| [SEC-SEG-04](../base/segredos/checklist.md#sec-seg-04--app-recusa-subir-com-segredo-fraco-ou-placeholder) | L2 | A02 | V13.2.3 (L2) | — | — |
| [SEC-SEG-05](../base/segredos/checklist.md#sec-seg-05--segredos-distintos-por-ambiente) | L2 | A02 | V13.3.1 (L2) | — | — |
| [SEC-SEG-06](../base/segredos/checklist.md#sec-seg-06--env-de-produção-com-permissão-restrita) | L2 | A02 | V13.3.2 (L2) | CONF-09 | — |
| [SEC-SEG-07](../base/segredos/checklist.md#sec-seg-07--segredos-não-vazam-por-docker-inspect) | L2 | A02 | V13.3.1 (L2), V13.3.2 (L2) | — | — |
| [SEC-SEG-08](../base/segredos/checklist.md#sec-seg-08--chave-de-deploy-do-ci-com-forced-command) | L2 | A08, A03 | V13.3.2 (L2) | — | — |
| [SEC-SEG-09](../base/segredos/checklist.md#sec-seg-09--rotação-de-segredos-planejada) | L3 | A02 | V13.1.4 (L3), V13.3.4 (L3) | — | — |
| [SEC-SEG-10](../base/segredos/checklist.md#sec-seg-10--token-de-bootstrap-removido-após-uso) | L1 | A07 | V6.4.1 (L1) | — | — |
| [SEC-SEG-11](../base/segredos/checklist.md#sec-seg-11--varredura-de-segredos-no-ci) | L2 | A03, A02 | V13.3.1 (L2) | — | — |

## 3. Autenticação, cadastro, recuperação (`SEC-AUTH`)

| Item | Nível | Top 10:2025 | ASVS 5.0 | WSTG v4.2 | API:2023 |
|---|---|---|---|---|---|
| [SEC-AUTH-01](../base/autenticacao/checklist.md#sec-auth-01--senha-guardada-com-argon2id) | L2 | A04, A07 | V11.4.2 (L2) | — | — |
| [SEC-AUTH-02](../base/autenticacao/checklist.md#sec-auth-02--parâmetros-do-argon2id--mínimo-owasp-e-medidos-no-servidor) | L2 | A04 | V11.4.2 (L2) | — | — |
| [SEC-AUTH-03](../base/autenticacao/checklist.md#sec-auth-03--pepper-aplicado-antes-do-hash-hmac-e-guardado-fora-do-banco) | L2 | A04 | V11.4.2 (L2), V13.3.1 (L2) | — | — |
| [SEC-AUTH-04](../base/autenticacao/checklist.md#sec-auth-04--rehash-automático-no-login) | L2 | A04 | V11.2.2 (L2) | — | — |
| [SEC-AUTH-05](../base/autenticacao/checklist.md#sec-auth-05--plano-do-pepper-escrito-backup-separado-rotação-versão) | L2 | A04 | V11.1.1 (L2) | — | — |
| [SEC-AUTH-06](../base/autenticacao/checklist.md#sec-auth-06--testes-automatizados-de-salt-e-de-pepper) | L2 | A04 | V11.4.2 (L2) | — | — |
| [SEC-AUTH-07](../base/autenticacao/checklist.md#sec-auth-07--login-sem-enumeração-mensagem-e-tempo-iguais) | L3 | A07 | V6.3.8 (L3) | IDNT-04 | — |
| [SEC-AUTH-08](../base/autenticacao/checklist.md#sec-auth-08--rate-limit-no-login-na-borda-e-na-aplicação) | L1 | A07 | V6.1.1 (L1), V6.3.1 (L1) | ATHN-03 | API4 |
| [SEC-AUTH-09](../base/autenticacao/checklist.md#sec-auth-09--lockout-por-conta-curto-e-persistido) | L1 | A07 | V6.3.1 (L1) | ATHN-03 | — |
| [SEC-AUTH-10](../base/autenticacao/checklist.md#sec-auth-10--mfa-em-toda-conta-administrativa) | L2 | A07 | V6.3.3 (L2) | — | — |
| [SEC-AUTH-11](../base/autenticacao/checklist.md#sec-auth-11--step-up-em-aparelho-novo--sinais-de-risco) | L3 | A07 | V7.5.3 (L3), V8.2.4 (L3) | — | — |
| [SEC-AUTH-12](../base/autenticacao/checklist.md#sec-auth-12--reautenticação-para-mudar-senha-e-mail-telefone-ou-fator) | L2 | A07 | V7.5.1 (L2) | ATHN-09 | — |
| [SEC-AUTH-13](../base/autenticacao/checklist.md#sec-auth-13--aviso-ao-titular-após-mudança-de-credencial) | L3 | A07 | V6.3.7 (L3) | — | — |
| [SEC-AUTH-14](../base/autenticacao/checklist.md#sec-auth-14--política-de-senha-tamanho-mínimomáximo-senha-vazada) | L1 | A07 | V6.2.1 (L1), V6.2.9 (L2), V6.2.12 (L2) | ATHN-07 | — |
| [SEC-AUTH-15](../base/autenticacao/checklist.md#sec-auth-15--bootstrap-do-primeiro-admin-fechado) | L1 | A07 | V6.3.2 (L1), V6.4.1 (L1) | ATHN-02 | — |
| [SEC-AUTH-16](../base/autenticacao/checklist.md#sec-auth-16--acesso-ao-painel-restrito-por-origem-recomendado) | L3 | A01 | V8.4.2 (L3) | CONF-05 | — |
| [SEC-AUTH-17](../base/autenticacao/checklist.md#sec-auth-17--login-social-sem-auto-vínculo-e-com-email_verified-confiável) | L2 | A07 | V6.8.1 (L2), V10.5.2 (L2) | — | — |
| [SEC-AUTH-18](../base/autenticacao/checklist.md#sec-auth-18--funções-barradas-até-verificar-e-mailtelefone) | L1 | A07 | V2.3.1 (L1) | IDNT-02 | — |
| [SEC-AUTH-19](../base/autenticacao/checklist.md#sec-auth-19--cadastro-e-recuperação-sem-enumeração) | L3 | A07 | V6.3.8 (L3) | IDNT-04 | — |
| [SEC-AUTH-20](../base/autenticacao/checklist.md#sec-auth-20--velocidade-de-cadastro-limitada) | L1 | A06 | V2.4.1 (L2), V6.1.1 (L1) | IDNT-02, BUSL-05 | API6 |
| [SEC-AUTH-21](../base/autenticacao/checklist.md#sec-auth-21--e-mail-não-verificado-não-prende-o-endereço-do-dono) | — | A07 | — | IDNT-02 | — |
| [SEC-AUTH-22](../base/autenticacao/checklist.md#sec-auth-22--nenhuma-conta-de-testeseed-em-produção) | L1 | A07, A02 | V6.3.2 (L1), V15.2.3 (L2) | ATHN-02 | — |
| [SEC-AUTH-23](../base/autenticacao/checklist.md#sec-auth-23--código-de-recuperação-forte-e-de-uso-único) | L2 | A07 | V6.5.1 (L2), V6.5.3 (L2), V6.5.5 (L2) | ATHN-09 | — |
| [SEC-AUTH-24](../base/autenticacao/checklist.md#sec-auth-24--palpites-contados-por-conta-sobrevivendo-ao-código-novo) | L2 | A07 | V6.6.3 (L2) | ATHN-09 | — |
| [SEC-AUTH-25](../base/autenticacao/checklist.md#sec-auth-25--recuperação-não-contorna-o-2º-fator) | L2 | A07 | V6.4.3 (L2) | ATHN-09 | — |
| [SEC-AUTH-26](../base/autenticacao/checklist.md#sec-auth-26--autorização-de-senha-nova-fora-da-url-e-sessões-derrubadas) | L1 | A07 | V14.2.1 (L1), V7.4.3 (L2) | ATHN-09 | — |
| [SEC-AUTH-27](../base/autenticacao/checklist.md#sec-auth-27--link-de-e-mail-se-houver-resistente-a-scanner-e-referer) | L2 | A07 | V6.5.1 (L2), V3.4.5 (L2) | ATHN-09 | — |
| [SEC-AUTH-28](../base/autenticacao/checklist.md#sec-auth-28--troca-de-telefone-verificado-prova-posse-do-atual) | L2 | A07 | V7.5.1 (L2), V6.6.1 (L2) | ATHN-09 | — |
| [SEC-AUTH-29](../base/autenticacao/checklist.md#sec-auth-29--política-para-o-mesmo-telefone-em-várias-contas) | L2 | A06 | V6.6.1 (L2) | — | — |

## 4. Sessão e tokens (`SEC-SESS`)

| Item | Nível | Top 10:2025 | ASVS 5.0 | WSTG v4.2 | API:2023 |
|---|---|---|---|---|---|
| [SEC-SESS-01](../base/sessao/checklist.md#sec-sess-01--cookies-de-sessão-com-httponly-secure-e-samesite) | L1 | A07 | V3.3.1 (L1), V3.3.2 (L2), V3.3.3 (L2), V3.3.4 (L2) | SESS-02 | — |
| [SEC-SESS-02](../base/sessao/checklist.md#sec-sess-02--nenhum-token-em-localstoragesessionstorage) | L2 | A07 | V14.3.3 (L2) | CLNT-12 | — |
| [SEC-SESS-03](../base/sessao/checklist.md#sec-sess-03--token-aleatório-forte-nunca-derivado-de-credencial) | L1 | A07 | V7.2.3 (L1), V11.5.1 (L2) | SESS-01 | — |
| [SEC-SESS-04](../base/sessao/checklist.md#sec-sess-04--access-curto-sem-privilégio-no-token-algoritmo-fixo) | L1 | A07 | V9.1.1 (L1), V9.1.2 (L1), V9.2.1 (L1), V9.2.2 (L2) | SESS-01 | API2 |
| [SEC-SESS-05](../base/sessao/checklist.md#sec-sess-05--refresh-rotativo-guardado-como-hash-com-detecção-de-reuso) | L1 | A07 | V7.2.4 (L1), V10.4.5 (L1) | SESS-01 | API2 |
| [SEC-SESS-06](../base/sessao/checklist.md#sec-sess-06--logout-e-troca-de-senhaprivilégio-revogam-no-servidor) | L1 | A07 | V7.4.1 (L1), V7.4.3 (L2), V8.3.2 (L3) | SESS-06 | — |
| [SEC-SESS-07](../base/sessao/checklist.md#sec-sess-07--purga-de-sessõestokens-agendada) | L2 | A07 | V7.3.2 (L2) | SESS-07 | — |
| [SEC-SESS-08](../base/sessao/checklist.md#sec-sess-08--csrf-em-toda-rota-que-muda-estado) | L1 | A01 | V3.5.1 (L1), V3.5.2 (L1), V3.5.3 (L1) | SESS-05 | — |
| [SEC-SESS-09](../base/sessao/checklist.md#sec-sess-09--ações-públicas-com-efeito-colateral-conferem-a-origem) | L1 | A01 | V3.5.1 (L1) | SESS-05 | — |
| [SEC-SESS-10](../base/sessao/checklist.md#sec-sess-10--segredo-de-assinatura-forte-e-distinto-por-ambiente) | L2 | A04 | V11.2.3 (L2), V13.3.1 (L2) | — | — |

## 5. API e endpoints (`SEC-API`)

| Item | Nível | Top 10:2025 | ASVS 5.0 | WSTG v4.2 | API:2023 |
|---|---|---|---|---|---|
| [SEC-API-01](../base/api/checklist.md#sec-api-01--dono-do-recurso--autorização-em-toda-rota-autenticada) | L1 | A01 | V8.2.1 (L1), V8.2.2 (L1), V8.3.1 (L1) | ATHZ-02, ATHZ-04 | API1 |
| [SEC-API-02](../base/api/checklist.md#sec-api-02--recurso-mais-sensível-com-permissão-própria) | L1 | A01 | V8.1.1 (L1), V8.2.2 (L1) | ATHZ-03 | API5 |
| [SEC-API-03](../base/api/checklist.md#sec-api-03--schema-de-saída-explícito-em-toda-rota) | L1 | A01 | V15.3.1 (L1) | — | API3 |
| [SEC-API-04](../base/api/checklist.md#sec-api-04--mass-assignment-bloqueado) | L2 | A01 | V15.3.3 (L2) | — | API3 |
| [SEC-API-05](../base/api/checklist.md#sec-api-05--bateria-de-entrada-nas-rotas-que-aceitam-dados) | L1 | A05 | V2.2.1 (L1), V16.5.1 (L2) | INPV-01, INPV-05, INPV-18 | — |
| [SEC-API-06](../base/api/checklist.md#sec-api-06--max_length-e-limites-em-todo-campo) | L1 | A06 | V2.2.1 (L1), V15.2.2 (L2) | — | API4 |
| [SEC-API-07](../base/api/checklist.md#sec-api-07--erros-que-não-ensinam-nada) | L2 | A10, A02 | V16.5.1 (L2), V13.4.2 (L2) | ERRH-01, ERRH-02 | API8 |
| [SEC-API-08](../base/api/checklist.md#sec-api-08--documentação-interativa-desligada-em-produção) | L2 | A02 | V13.4.5 (L2) | CONF-05, INFO-06 | API9 |
| [SEC-API-09](../base/api/checklist.md#sec-api-09--cors-restrito) | L1 | A02 | V3.4.2 (L1) | CLNT-07 | API8 |
| [SEC-API-10](../base/api/checklist.md#sec-api-10--limite-de-tamanho-de-corpo-na-borda-e-no-app) | L1 | A06 | V5.2.1 (L1), V15.2.2 (L2) | — | API4 |
| [SEC-API-11](../base/api/checklist.md#sec-api-11--campos-derivados-nunca-aceitos-do-cliente) | L1 | A06 | V2.2.2 (L1), V8.3.1 (L1) | BUSL-01, BUSL-02 | — |
| [SEC-API-12](../base/api/checklist.md#sec-api-12--integrações-documentadas-e-com-privilégio-mínimo) | L2 | A02 | V13.1.1 (L2), V13.2.2 (L2) | — | API10 |
| [SEC-API-13](../base/api/checklist.md#sec-api-13--saída-segura-contra-ssrf) | L2 | A01 | V1.3.6 (L2), V13.2.5 (L2), V15.3.2 (L2) | INPV-19 | API7 |
| [SEC-API-14](../base/api/checklist.md#sec-api-14--url-de-imagemlink-limitada-a-hosts-permitidos) | L2 | A01 | V1.3.6 (L2), V13.2.4 (L2) | INPV-19 | API7 |
| [SEC-API-15](../base/api/checklist.md#sec-api-15--framework-do-front-fora-de-cve-de-bypass-de-middleware) | L1 | A03, A01 | V15.2.1 (L1) | ATHZ-02 | — |

## 6. Upload e mídia (`SEC-UPL`)

| Item | Nível | Top 10:2025 | ASVS 5.0 | WSTG v4.2 | API:2023 |
|---|---|---|---|---|---|
| [SEC-UPL-01](../base/upload/checklist.md#sec-upl-01--tipo-real-por-magic-bytes-com-whitelist) | L1 | A06 | V5.2.2 (L1) | BUSL-08 | — |
| [SEC-UPL-02](../base/upload/checklist.md#sec-upl-02--svg-recusado) | L1 | A05 | V1.3.4 (L2), V5.2.2 (L1) | BUSL-09 | — |
| [SEC-UPL-03](../base/upload/checklist.md#sec-upl-03--proteção-contra-bomba-de-descompressão) | L2 | A06 | V5.2.3 (L2) | BUSL-09 | — |
| [SEC-UPL-04](../base/upload/checklist.md#sec-upl-04--nome-gerado-pelo-servidor-e-sem-path-traversal) | L1 | A01 | V5.3.2 (L1), V5.4.1 (L2) | ATHZ-01 | — |
| [SEC-UPL-05](../base/upload/checklist.md#sec-upl-05--limite-de-tamanho-no-app-e-na-borda) | L1 | A06 | V5.2.1 (L1) | BUSL-09 | API4 |
| [SEC-UPL-06](../base/upload/checklist.md#sec-upl-06--metadados-removidos-exif-gps-miniatura-texto) | L3 | A01 | V14.2.8 (L3) | — | — |
| [SEC-UPL-07](../base/upload/checklist.md#sec-upl-07--diretório-de-upload-sem-listagem-e-com-nosniff) | L1 | A02 | V5.3.1 (L1), V13.4.3 (L2), V3.4.4 (L2) | CONF-03 | — |
| [SEC-UPL-08](../base/upload/checklist.md#sec-upl-08--mídia-privada-fora-do-alcance-público) | L1 | A01 | V8.2.2 (L1) | ATHZ-02 | — |
| [SEC-UPL-09](../base/upload/checklist.md#sec-upl-09--acervo-sensível-não-raspável-sem-controle) | L2 | A06 | V2.4.1 (L2) | BUSL-07 | API6 |
| [SEC-UPL-10](../base/upload/checklist.md#sec-upl-10--cache-de-mídia-sensível-permite-recolher) | L2 | A01 | V14.2.2 (L2) | — | — |
| [SEC-UPL-11](../base/upload/checklist.md#sec-upl-11--crawlers-fora-das-pastas-de-mídia) | — | A02 | — | INFO-03 | — |

## 7. Cabeçalhos, CSP e XSS (`SEC-NAV`)

| Item | Nível | Top 10:2025 | ASVS 5.0 | WSTG v4.2 | API:2023 |
|---|---|---|---|---|---|
| [SEC-NAV-01](../base/headers/checklist.md#sec-nav-01--hsts-ativo) | L1 | A04, A02 | V3.4.1 (L1) | CONF-07 | — |
| [SEC-NAV-02](../base/headers/checklist.md#sec-nav-02--csp-nas-páginas-html) | L2 | A02, A05 | V3.4.3 (L2) | — | — |
| [SEC-NAV-03](../base/headers/checklist.md#sec-nav-03--csp-sem-unsafe-inline-em-script-meta) | L2 | A05 | V3.4.3 (L2) | — | — |
| [SEC-NAV-04](../base/headers/checklist.md#sec-nav-04--nosniff-proteção-contra-frame-referrer-policy-permissions-policy) | L2 | A02 | V3.4.4 (L2), V3.4.5 (L2), V3.4.6 (L2) | CLNT-09 | — |
| [SEC-NAV-05](../base/headers/checklist.md#sec-nav-05--headers-repetidos-em-todo-location-do-nginx) | L1 | A02 | V3.4.1 (L1), V3.4.4 (L2) | — | — |
| [SEC-NAV-06](../base/headers/checklist.md#sec-nav-06--cache-control-no-store-em-resposta-autenticadacom-pii) | L2 | A02 | V14.3.2 (L2) | ATHN-06 | — |
| [SEC-NAV-07](../base/headers/checklist.md#sec-nav-07--sem-versão-de-servidorframework-nos-headers) | L3 | A02 | V13.4.6 (L3) | INFO-02, INFO-08 | — |
| [SEC-NAV-08](../base/headers/checklist.md#sec-nav-08--nenhum-sink-de-html-com-conteúdo-controlável) | L1 | A05 | V1.2.1 (L1), V1.3.1 (L1), V3.2.2 (L1) | INPV-01, INPV-02, CLNT-01 | — |
| [SEC-NAV-09](../base/headers/checklist.md#sec-nav-09--json-em-script-escapado) | L1 | A05 | V1.2.3 (L1) | CLNT-01 | — |
| [SEC-NAV-10](../base/headers/checklist.md#sec-nav-10--urls-do-cmsusuário-com-esquema-validado) | L1 | A05 | V1.2.2 (L1) | CLNT-01, CLNT-04 | — |
| [SEC-NAV-11](../base/headers/checklist.md#sec-nav-11--scripts-de-terceiros-mínimos-após-consentimento-com-sricsp) | L2 | A08, A03 | V3.6.1 (L3), V14.2.3 (L2) | — | — |
| [SEC-NAV-12](../base/headers/checklist.md#sec-nav-12--exportações-protegidas-contra-fórmula-csv) | L3 | A05 | V1.2.10 (L3) | — | — |

## 8. Banco de dados (`SEC-BD`)

| Item | Nível | Top 10:2025 | ASVS 5.0 | WSTG v4.2 | API:2023 |
|---|---|---|---|---|---|
| [SEC-BD-01](../base/banco/checklist.md#sec-bd-01--nenhuma-query-montada-com-texto-do-usuário) | L1 | A05 | V1.2.4 (L1) | INPV-05 | — |
| [SEC-BD-02](../base/banco/checklist.md#sec-bd-02--ordenaçãocoluna-dinâmica-por-allowlist) | L1 | A05 | V1.2.4 (L1), V2.2.1 (L1) | INPV-05 | — |
| [SEC-BD-03](../base/banco/checklist.md#sec-bd-03--operações-de-consumo-atômicas) | L2 | A06 | V15.4.2 (L3), V2.3.3 (L2), V2.3.4 (L2) | BUSL-05 | — |
| [SEC-BD-04](../base/banco/checklist.md#sec-bd-04--dinheiro-em-tipo-decimal) | L2 | A06 | V15.3.5 (L2) | — | — |
| [SEC-BD-05](../base/banco/checklist.md#sec-bd-05--unicidade-garantida-no-banco) | L3 | A06 | V15.4.2 (L3) | BUSL-05 | — |
| [SEC-BD-06](../base/banco/checklist.md#sec-bd-06--banco-e-redis-inacessíveis-pela-internet) | — | A02 | — | CONF-01 | — |
| [SEC-BD-07](../base/banco/checklist.md#sec-bd-07--usuário-da-aplicação-com-privilégio-mínimo) | L2 | A02 | V13.2.2 (L2) | — | — |
| [SEC-BD-08](../base/banco/checklist.md#sec-bd-08--instalação-endurecida) | L2 | A02 | V13.2.3 (L2) | CONF-02 | — |
| [SEC-BD-09](../base/banco/checklist.md#sec-bd-09--banco-gerenciado-com-rede-privada-tls-e-backup) | L2 | A02, A04 | V12.3.1 (L2) | CONF-01 | — |
| [SEC-BD-10](../base/banco/checklist.md#sec-bd-10--rls-em-banco-acessado-pelo-front) | L1 | A01 | V8.2.2 (L1), V8.3.1 (L1) | ATHZ-04 | API1 |
| [SEC-BD-11](../base/banco/checklist.md#sec-bd-11--entrada-com-null-byte-não-vira-500) | L1 | A10, A05 | V2.2.1 (L1), V16.5.3 (L2) | ERRH-01 | — |

## 9. Pagamentos (`SEC-PAG`)

| Item | Nível | Top 10:2025 | ASVS 5.0 | WSTG v4.2 | API:2023 |
|---|---|---|---|---|---|
| [SEC-PAG-01](../base/pagamentos/checklist.md#sec-pag-01--cartão-processado-pelo-gateway-nunca-armazenado) | L2 | A04 | V14.1.2 (L2) | — | — |
| [SEC-PAG-02](../base/pagamentos/checklist.md#sec-pag-02--valor-recalculado-no-servidor) | L1 | A06 | V2.2.2 (L1), V8.3.1 (L1) | BUSL-01, BUSL-02 | — |
| [SEC-PAG-03](../base/pagamentos/checklist.md#sec-pag-03--webhook-revalida-o-status-na-api-do-gateway) | L3 | A08 | V4.1.5 (L3) | BUSL-03 | — |
| [SEC-PAG-04](../base/pagamentos/checklist.md#sec-pag-04--idempotência-no-processamento-de-pagamento) | L2 | A06 | V2.3.3 (L2), V2.3.4 (L2) | BUSL-05 | — |
| [SEC-PAG-05](../base/pagamentos/checklist.md#sec-pag-05--emissãouso-de-crédito-atômicos-e-auditados) | L2 | A06 | V2.3.3 (L2), V15.4.2 (L3) | BUSL-05 | — |
| [SEC-PAG-06](../base/pagamentos/checklist.md#sec-pag-06--limite-de-recusas-contra-card-testing) | L2 | A06 | V2.3.2 (L2), V2.4.1 (L2) | BUSL-07 | API6 |
| [SEC-PAG-07](../base/pagamentos/checklist.md#sec-pag-07--página-de-pagamento-sem-scripts-de-terceiros) | L2 | A08 | V3.6.1 (L3), V14.2.3 (L2) | — | — |
| [SEC-PAG-08](../base/pagamentos/checklist.md#sec-pag-08--portal-do-gateway-com-mfa-em-todos-e-login-nominal) | L2 | A07 | V6.3.3 (L2) | — | — |
| [SEC-PAG-09](../base/pagamentos/checklist.md#sec-pag-09--alteração-de-dado-bancário-confirmada-fora-de-banda-e-conciliação-diária) | L3 | A06 | V7.5.3 (L3) | — | — |
| [SEC-PAG-10](../base/pagamentos/checklist.md#sec-pag-10--aprovação-dupla-em-reembolso-manual-de-alto-valor) | L3 | A06 | V2.3.5 (L3) | — | — |

## 10. Mensageria (`SEC-MSG`)

| Item | Nível | Top 10:2025 | ASVS 5.0 | WSTG v4.2 | API:2023 |
|---|---|---|---|---|---|
| [SEC-MSG-01](../base/mensageria/checklist.md#sec-msg-01--limite-de-envio-por-pessoa-e-finalidade) | L2 | A06 | V2.3.2 (L2), V2.4.1 (L2) | BUSL-05 | API6 |
| [SEC-MSG-02](../base/mensageria/checklist.md#sec-msg-02--recusa-de-um-limite-não-consome-os-outros) | L2 | A06 | V2.3.2 (L2) | BUSL-05 | — |
| [SEC-MSG-03](../base/mensageria/checklist.md#sec-msg-03--limite-por-número-de-destino) | L2 | A06 | V2.4.1 (L2), V6.6.3 (L2) | BUSL-05 | — |
| [SEC-MSG-04](../base/mensageria/checklist.md#sec-msg-04--países-de-destino-restritos) | L2 | A06 | V2.3.2 (L2) | — | — |
| [SEC-MSG-05](../base/mensageria/checklist.md#sec-msg-05--teto-global-alarme-de-conversão-e-alerta-de-gasto) | L2 | A06 | V2.1.3 (L2), V2.3.2 (L2) | BUSL-07 | API4 |
| [SEC-MSG-06](../base/mensageria/checklist.md#sec-msg-06--captcha-fail-closed-nas-rotas-que-enviam) | L2 | A10 | V2.4.1 (L2), V16.5.3 (L2) | — | — |
| [SEC-MSG-07](../base/mensageria/checklist.md#sec-msg-07--código-só-para-canal-verificado) | L2 | A07 | V6.6.1 (L2) | — | — |
| [SEC-MSG-08](../base/mensageria/checklist.md#sec-msg-08--recusas-registradas-e-rastreáveis-pelo-suporte) | L2 | A09 | V16.3.3 (L2) | — | — |
| [SEC-MSG-09](../base/mensageria/checklist.md#sec-msg-09--gasto-mensurável-finalidade-preço-versionado-entregue--aceito) | L2 | A06 | V2.1.3 (L2) | — | — |
| [SEC-MSG-10](../base/mensageria/checklist.md#sec-msg-10--spf-dkim-e-dmarc-no-domínio-remetente) | — | A02 | — | — | — |
| [SEC-MSG-11](../base/mensageria/checklist.md#sec-msg-11--remetente-de-segurança-separado-do-de-marketing) | — | A06 | — | — | — |

## 11. Rate limit, carga e abuso (`SEC-RL`)

| Item | Nível | Top 10:2025 | ASVS 5.0 | WSTG v4.2 | API:2023 |
|---|---|---|---|---|---|
| [SEC-RL-01](../base/rate-limit/checklist.md#sec-rl-01--limite-na-borda-nginxcdn-e-na-aplicação) | L1 | A06 | V2.4.1 (L2), V6.3.1 (L1) | BUSL-07 | API4 |
| [SEC-RL-02](../base/rate-limit/checklist.md#sec-rl-02--assets-fora-do-limite-de-ações) | L2 | A06 | V2.4.1 (L2) | — | — |
| [SEC-RL-03](../base/rate-limit/checklist.md#sec-rl-03--limite-por-ip-compatível-com-cgnat) | L2 | A06 | V2.4.1 (L2) | — | — |
| [SEC-RL-04](../base/rate-limit/checklist.md#sec-rl-04--ip-real-vindo-só-do-proxy-confiável) | L2 | A02 | V4.1.3 (L2), V15.3.4 (L2) | — | — |
| [SEC-RL-05](../base/rate-limit/checklist.md#sec-rl-05--get-públicos-que-servem-acervo-têm-limite) | L2 | A06 | V2.4.1 (L2) | BUSL-07 | API6 |
| [SEC-RL-06](../base/rate-limit/checklist.md#sec-rl-06--resposta-429-amigável-e-rastreável) | L2 | A10 | V16.5.1 (L2) | — | — |
| [SEC-RL-07](../base/rate-limit/checklist.md#sec-rl-07--teste-de-regressão-navegação-normal-sem-429) | L2 | A06 | V2.4.1 (L2) | — | — |
| [SEC-RL-08](../base/rate-limit/checklist.md#sec-rl-08--teste-de-carga-com-pico-realista) | L2 | A06 | V15.1.3 (L2), V15.2.2 (L2) | — | API4 |
| [SEC-RL-09](../base/rate-limit/checklist.md#sec-rl-09--proteção-l7--waf-avaliada) | L2 | A02 | V2.4.1 (L2) | — | — |
| [SEC-RL-10](../base/rate-limit/checklist.md#sec-rl-10--modo-observar-antes-de-bloquear-limites-novos) | — | A06 | — | — | — |

## 12. Captcha (`SEC-CAP`)

| Item | Nível | Top 10:2025 | ASVS 5.0 | WSTG v4.2 | API:2023 |
|---|---|---|---|---|---|
| [SEC-CAP-01](../base/captcha/checklist.md#sec-cap-01--decisão-sobre-captcha-registrada) | L1 | A06 | V2.4.1 (L2), V6.1.1 (L1) | — | — |
| [SEC-CAP-02](../base/captcha/checklist.md#sec-cap-02--token-validado-no-backend) | L1 | A06 | V2.2.2 (L1), V2.4.1 (L2) | BUSL-07 | — |
| [SEC-CAP-03](../base/captcha/checklist.md#sec-cap-03--produção-recusa-chave-de-teste) | L2 | A02 | V13.2.3 (L2) | — | — |
| [SEC-CAP-04](../base/captcha/checklist.md#sec-cap-04--http-400-hostname-e-action-tratados) | L2 | A06 | V2.4.1 (L2) | — | — |
| [SEC-CAP-05](../base/captcha/checklist.md#sec-cap-05--token-renovado-após-toda-tentativa) | L2 | A06 | V2.4.1 (L2) | — | — |
| [SEC-CAP-06](../base/captcha/checklist.md#sec-cap-06--comportamento-na-falha-do-provedor-decidido-por-rota) | L2 | A10 | V16.5.2 (L2), V16.5.3 (L2) | — | — |
| [SEC-CAP-07](../base/captcha/checklist.md#sec-cap-07--widget-por-ambiente-e-secret-só-no-servidor) | L2 | A02 | V13.3.1 (L2), V13.3.2 (L2) | — | — |
| [SEC-CAP-08](../base/captcha/checklist.md#sec-cap-08--captcha-não-substitui-rate-limit) | L1 | A06 | V2.4.1 (L2), V6.3.1 (L1) | BUSL-07 | API6 |

## 13. Infraestrutura de VPS (`SEC-VPS`)

| Item | Nível | Top 10:2025 | ASVS 5.0 | WSTG v4.2 | API:2023 |
|---|---|---|---|---|---|
| [SEC-VPS-01](../base/infra-vps/checklist.md#sec-vps-01--ssh-só-por-chave-sem-root) | — | A07, A02 | — | CONF-01 | — |
| [SEC-VPS-02](../base/infra-vps/checklist.md#sec-vps-02--algoritmos-ssh-modernos) | — | A04 | — | CONF-01 | — |
| [SEC-VPS-03](../base/infra-vps/checklist.md#sec-vps-03--nenhum-login-suspeito) | — | A09 | — | — | — |
| [SEC-VPS-04](../base/infra-vps/checklist.md#sec-vps-04--contas-de-serviço-sem-sudo-e-sudo-do-deploy-restrito) | — | A01, A02 | — | CONF-09 | — |
| [SEC-VPS-05](../base/infra-vps/checklist.md#sec-vps-05--firewall-default-deny-com-só-2280443) | — | A02 | — | CONF-01 | — |
| [SEC-VPS-06](../base/infra-vps/checklist.md#sec-vps-06--fail2ban-ativo-com-jails-validadas) | — | A09 | — | — | — |
| [SEC-VPS-07](../base/infra-vps/checklist.md#sec-vps-07--dotfiles-bloqueados-e-honeypot-recomendado) | L1 | A02 | V13.4.1 (L1), V13.4.7 (L3) | CONF-04 | — |
| [SEC-VPS-08](../base/infra-vps/checklist.md#sec-vps-08--atualizações-automáticas-e-reboot-de-kernel) | L1 | A03, A02 | V15.2.1 (L1) | — | — |
| [SEC-VPS-09](../base/infra-vps/checklist.md#sec-vps-09--sysctl-de-rede-e-kernel-endurecidos) | — | A02 | — | CONF-01 | — |
| [SEC-VPS-10](../base/infra-vps/checklist.md#sec-vps-10--auditd-journald-persistente-apparmor-e-baseline) | L2 | A09, A02 | V16.4.2 (L2) | — | — |
| [SEC-VPS-11](../base/infra-vps/checklist.md#sec-vps-11--serviços-da-aplicação-isolados-no-systemd) | L2 | A02 | V13.2.2 (L2) | CONF-09 | — |
| [SEC-VPS-12](../base/infra-vps/checklist.md#sec-vps-12--backend-e-banco-só-em-loopback) | — | A02 | — | CONF-01 | — |
| [SEC-VPS-13](../base/infra-vps/checklist.md#sec-vps-13--healthcheck-funcional-com-alerta-externo) | L2 | A09 | V16.4.3 (L2) | — | — |
| [SEC-VPS-14](../base/infra-vps/checklist.md#sec-vps-14--smoke-test-de-resiliência-no-procedimento-de-deploy) | L2 | A10 | V16.5.2 (L2) | — | — |
| [SEC-VPS-15](../base/infra-vps/checklist.md#sec-vps-15--validação-externa-feita-ssh-audit-testssl-portas-lynis) | L1 | A02 | V12.1.1 (L1) | CONF-01, CRYP-01 | — |
| [SEC-VPS-16](../base/infra-vps/checklist.md#sec-vps-16--deploy-com-gate-e-build-fora-da-produção-recomendado) | L2 | A08, A03 | V15.2.3 (L2) | — | — |

## 14. Nginx e TLS (`SEC-WEB`)

| Item | Nível | Top 10:2025 | ASVS 5.0 | WSTG v4.2 | API:2023 |
|---|---|---|---|---|---|
| [SEC-WEB-01](../base/nginx-tls/checklist.md#sec-web-01--só-tls-12-e-13) | L1 | A04 | V12.1.1 (L1), V12.1.2 (L2) | CRYP-01 | — |
| [SEC-WEB-02](../base/nginx-tls/checklist.md#sec-web-02--certificado-válido-e-renovação-automática) | L1 | A04 | V12.2.2 (L1) | CRYP-01 | — |
| [SEC-WEB-03](../base/nginx-tls/checklist.md#sec-web-03--httphttps-e-host-canônico) | L1 | A04 | V12.2.1 (L1), V4.1.2 (L2) | CRYP-03, ATHN-01 | — |
| [SEC-WEB-04](../base/nginx-tls/checklist.md#sec-web-04--nota-de-tls-externa) | L2 | A04 | V12.1.2 (L2) | CRYP-01 | — |
| [SEC-WEB-05](../base/nginx-tls/checklist.md#sec-web-05--server_tokens-off) | L3 | A02 | V13.4.6 (L3) | INFO-02 | — |
| [SEC-WEB-06](../base/nginx-tls/checklist.md#sec-web-06--proxy-só-para-loopback-e-ip-real-confiável) | L2 | A02 | V4.1.3 (L2), V15.3.4 (L2) | — | — |
| [SEC-WEB-07](../base/nginx-tls/checklist.md#sec-web-07--raiz-privada-nunca-servida) | L1 | A02 | V13.4.1 (L1), V13.4.7 (L3) | CONF-04 | — |
| [SEC-WEB-08](../base/nginx-tls/checklist.md#sec-web-08--zonas-de-rate-limit-dedicadas-api-e-login) | L2 | A06 | V2.4.1 (L2) | ATHN-03 | API4 |
| [SEC-WEB-09](../base/nginx-tls/checklist.md#sec-web-09--config-válida-e-versionada) | — | A02 | — | CONF-02 | — |

## 15. Cópias de segurança (`SEC-BKP`)

| Item | Nível | Top 10:2025 | ASVS 5.0 | WSTG v4.2 | API:2023 |
|---|---|---|---|---|---|
| [SEC-BKP-01](../base/copias-de-seguranca/checklist.md#sec-bkp-01--backup-automático-do-banco-e-dos-arquivos) | — | — | — | — | — |
| [SEC-BKP-02](../base/copias-de-seguranca/checklist.md#sec-bkp-02--backup-cifrado-com-chave-pública-servidor-não-decifra) | L2 | A04 | V14.2.4 (L2) | — | — |
| [SEC-BKP-03](../base/copias-de-seguranca/checklist.md#sec-bkp-03--diretório-de-backup-restrito) | L2 | A01, A02 | V14.2.4 (L2) | — | — |
| [SEC-BKP-04](../base/copias-de-seguranca/checklist.md#sec-bkp-04--cópia-fora-do-host) | — | — | — | — | — |
| [SEC-BKP-05](../base/copias-de-seguranca/checklist.md#sec-bkp-05--chave-do-backup-e-pepper-guardados-à-parte-com-redundância) | L2 | A04 | V11.1.1 (L2), V13.3.1 (L2) | — | — |
| [SEC-BKP-06](../base/copias-de-seguranca/checklist.md#sec-bkp-06--restauração-testada-recentemente) | — | — | — | — | — |
| [SEC-BKP-07](../base/copias-de-seguranca/checklist.md#sec-bkp-07--retenção-do-backup-alinhada-à-lgpd) | L3 | — | V14.2.7 (L3) | — | — |

## 16. Logs, auditoria, monitoramento (`SEC-LOG`)

| Item | Nível | Top 10:2025 | ASVS 5.0 | WSTG v4.2 | API:2023 |
|---|---|---|---|---|---|
| [SEC-LOG-01](../base/logs/checklist.md#sec-log-01--eventos-de-autenticação-auditados) | L2 | A09 | V16.3.1 (L2) | — | — |
| [SEC-LOG-02](../base/logs/checklist.md#sec-log-02--ações-sobre-dado-sensível-auditadas-inclusive-leitura-e-delete) | L2 | A09 | V16.3.2 (L2), V16.3.3 (L2) | — | — |
| [SEC-LOG-03](../base/logs/checklist.md#sec-log-03--mudança-de-configuração-com-antesdepois) | L2 | A09 | V16.2.1 (L2), V16.3.3 (L2) | — | — |
| [SEC-LOG-04](../base/logs/checklist.md#sec-log-04--auditoria-gravada-na-mesma-transação) | L2 | A09 | V16.2.1 (L2) | — | — |
| [SEC-LOG-05](../base/logs/checklist.md#sec-log-05--nada-de-segredo-ou-vínculo-sensível-em-log) | L2 | A09 | V16.2.5 (L2) | — | — |
| [SEC-LOG-06](../base/logs/checklist.md#sec-log-06--alertas-saem-do-servidor-e-têm-dono) | L2 | A09 | V16.4.3 (L2) | — | — |
| [SEC-LOG-07](../base/logs/checklist.md#sec-log-07--logs-copiados-para-fora-do-servidor) | L2 | A09 | V16.4.3 (L2) | — | — |
| [SEC-LOG-08](../base/logs/checklist.md#sec-log-08--detecção-de-volume-anômalo) | L2 | A09 | V16.3.3 (L2) | — | — |
| [SEC-LOG-09](../base/logs/checklist.md#sec-log-09--trilha-protegida-e-com-retenção) | L2 | A09 | V16.4.2 (L2) | — | — |

## 17. Privacidade, LGPD, cookies (`SEC-LGPD`)

| Item | Nível | Top 10:2025 | ASVS 5.0 | WSTG v4.2 | API:2023 |
|---|---|---|---|---|---|
| [SEC-LGPD-01](../base/privacidade/checklist.md#sec-lgpd-01--classificação-de-dados-por-campo) | L2 | A04 | V14.1.1 (L2), V14.1.2 (L2) | — | — |
| [SEC-LGPD-02](../base/privacidade/checklist.md#sec-lgpd-02--política-de-retenção-com-expurgo-agendado) | L3 | — | V14.2.7 (L3) | — | — |
| [SEC-LGPD-03](../base/privacidade/checklist.md#sec-lgpd-03--dado-sensível-fora-de-url-log-e-storage-do-navegador) | L1 | A01 | V14.2.1 (L1), V14.3.3 (L2), V16.2.5 (L2) | CLNT-12 | — |
| [SEC-LGPD-04](../base/privacidade/checklist.md#sec-lgpd-04--analyticsads-só-após-consentimento) | L2 | — | V14.2.3 (L2) | — | — |
| [SEC-LGPD-05](../base/privacidade/checklist.md#sec-lgpd-05--política-de-privacidade-lista-os-terceiros-reais) | L2 | — | V14.2.3 (L2) | — | — |
| [SEC-LGPD-06](../base/privacidade/checklist.md#sec-lgpd-06--conteúdo-sensível-público-com-controles-coerentes-ao-consentimento) | — | A01 | — | — | — |
| [SEC-LGPD-07](../base/privacidade/checklist.md#sec-lgpd-07--fluxo-de-direitos-do-titular) | — | — | — | — | — |

## 18. Operação, incidentes, pessoas (`SEC-OPS`)

| Item | Nível | Top 10:2025 | ASVS 5.0 | WSTG v4.2 | API:2023 |
|---|---|---|---|---|---|
| [SEC-OPS-01](../base/operacao/checklist.md#sec-ops-01--runbook-de-incidente-escrito) | — | A09 | — | — | — |
| [SEC-OPS-02](../base/operacao/checklist.md#sec-ops-02--mfa-nas-contas-externas-do-perímetro) | — | A07 | — | — | — |
| [SEC-OPS-03](../base/operacao/checklist.md#sec-ops-03--revisão-periódica-de-acessos) | — | A01 | — | — | — |
| [SEC-OPS-04](../base/operacao/checklist.md#sec-ops-04--procedimento-contra-phishingbec) | — | — | — | — | — |
| [SEC-OPS-05](../base/operacao/checklist.md#sec-ops-05--riscos-aceitos-e-decisões-registrados) | — | A06 | — | — | — |

## Índice reverso — Top 10:2025 → itens

- **A01 Broken Access Control:** `SEC-AUTH-16`, `SEC-SESS-08`, `SEC-SESS-09`, `SEC-API-01`, `SEC-API-02`, `SEC-API-03`, `SEC-API-04`, `SEC-API-13`, `SEC-API-14`, `SEC-API-15`, `SEC-UPL-04`, `SEC-UPL-06`, `SEC-UPL-08`, `SEC-UPL-10`, `SEC-BD-10`, `SEC-VPS-04`, `SEC-BKP-03`, `SEC-LGPD-03`, `SEC-LGPD-06`, `SEC-OPS-03`.
- **A02 Security Misconfiguration:** `SEC-DEP-05`, `SEC-SEG-01`, `SEC-SEG-02`, `SEC-SEG-03`, `SEC-SEG-04`, `SEC-SEG-05`, `SEC-SEG-06`, `SEC-SEG-07`, `SEC-SEG-09`, `SEC-SEG-11`, `SEC-AUTH-22`, `SEC-API-07`, `SEC-API-08`, `SEC-API-09`, `SEC-API-12`, `SEC-UPL-07`, `SEC-UPL-11`, `SEC-NAV-01`, `SEC-NAV-02`, `SEC-NAV-04`, `SEC-NAV-05`, `SEC-NAV-06`, `SEC-NAV-07`, `SEC-BD-06`, `SEC-BD-07`, `SEC-BD-08`, `SEC-BD-09`, `SEC-MSG-10`, `SEC-RL-04`, `SEC-RL-09`, `SEC-CAP-03`, `SEC-CAP-07`, `SEC-VPS-01`, `SEC-VPS-04`, `SEC-VPS-05`, `SEC-VPS-07`, `SEC-VPS-08`, `SEC-VPS-09`, `SEC-VPS-10`, `SEC-VPS-11`, `SEC-VPS-12`, `SEC-VPS-15`, `SEC-WEB-05`, `SEC-WEB-06`, `SEC-WEB-07`, `SEC-WEB-09`, `SEC-BKP-03`.
- **A03 Software Supply Chain Failures:** `SEC-DEP-01`, `SEC-DEP-02`, `SEC-DEP-03`, `SEC-DEP-04`, `SEC-DEP-05`, `SEC-DEP-06`, `SEC-DEP-07`, `SEC-DEP-08`, `SEC-DEP-09`, `SEC-DEP-11`, `SEC-SEG-08`, `SEC-SEG-11`, `SEC-API-15`, `SEC-NAV-11`, `SEC-VPS-08`, `SEC-VPS-16`.
- **A04 Cryptographic Failures:** `SEC-SEG-01`, `SEC-AUTH-01`, `SEC-AUTH-02`, `SEC-AUTH-03`, `SEC-AUTH-04`, `SEC-AUTH-05`, `SEC-AUTH-06`, `SEC-SESS-10`, `SEC-NAV-01`, `SEC-BD-09`, `SEC-PAG-01`, `SEC-VPS-02`, `SEC-WEB-01`, `SEC-WEB-02`, `SEC-WEB-03`, `SEC-WEB-04`, `SEC-BKP-02`, `SEC-BKP-05`, `SEC-LGPD-01`.
- **A05 Injection:** `SEC-API-05`, `SEC-UPL-02`, `SEC-NAV-02`, `SEC-NAV-03`, `SEC-NAV-08`, `SEC-NAV-09`, `SEC-NAV-10`, `SEC-NAV-12`, `SEC-BD-01`, `SEC-BD-02`, `SEC-BD-11`.
- **A06 Insecure Design:** `SEC-DEP-10`, `SEC-AUTH-20`, `SEC-AUTH-29`, `SEC-API-06`, `SEC-API-10`, `SEC-API-11`, `SEC-UPL-01`, `SEC-UPL-03`, `SEC-UPL-05`, `SEC-UPL-09`, `SEC-BD-03`, `SEC-BD-04`, `SEC-BD-05`, `SEC-PAG-02`, `SEC-PAG-04`, `SEC-PAG-05`, `SEC-PAG-06`, `SEC-PAG-09`, `SEC-PAG-10`, `SEC-MSG-01`, `SEC-MSG-02`, `SEC-MSG-03`, `SEC-MSG-04`, `SEC-MSG-05`, `SEC-MSG-09`, `SEC-MSG-11`, `SEC-RL-01`, `SEC-RL-02`, `SEC-RL-03`, `SEC-RL-05`, `SEC-RL-07`, `SEC-RL-08`, `SEC-RL-10`, `SEC-CAP-01`, `SEC-CAP-02`, `SEC-CAP-04`, `SEC-CAP-05`, `SEC-CAP-08`, `SEC-WEB-08`, `SEC-OPS-05`.
- **A07 Authentication Failures:** `SEC-SEG-10`, `SEC-AUTH-01`, `SEC-AUTH-07`, `SEC-AUTH-08`, `SEC-AUTH-09`, `SEC-AUTH-10`, `SEC-AUTH-11`, `SEC-AUTH-12`, `SEC-AUTH-13`, `SEC-AUTH-14`, `SEC-AUTH-15`, `SEC-AUTH-17`, `SEC-AUTH-18`, `SEC-AUTH-19`, `SEC-AUTH-21`, `SEC-AUTH-22`, `SEC-AUTH-23`, `SEC-AUTH-24`, `SEC-AUTH-25`, `SEC-AUTH-26`, `SEC-AUTH-27`, `SEC-AUTH-28`, `SEC-SESS-01`, `SEC-SESS-02`, `SEC-SESS-03`, `SEC-SESS-04`, `SEC-SESS-05`, `SEC-SESS-06`, `SEC-SESS-07`, `SEC-PAG-08`, `SEC-MSG-07`, `SEC-VPS-01`, `SEC-OPS-02`.
- **A08 Software or Data Integrity Failures:** `SEC-DEP-07`, `SEC-DEP-09`, `SEC-SEG-08`, `SEC-NAV-11`, `SEC-PAG-03`, `SEC-PAG-07`, `SEC-VPS-16`.
- **A09 Security Logging and Alerting Failures:** `SEC-MSG-08`, `SEC-VPS-03`, `SEC-VPS-06`, `SEC-VPS-10`, `SEC-VPS-13`, `SEC-LOG-01`, `SEC-LOG-02`, `SEC-LOG-03`, `SEC-LOG-04`, `SEC-LOG-05`, `SEC-LOG-06`, `SEC-LOG-07`, `SEC-LOG-08`, `SEC-LOG-09`, `SEC-OPS-01`.
- **A10 Mishandling of Exceptional Conditions:** `SEC-API-07`, `SEC-BD-11`, `SEC-MSG-06`, `SEC-RL-06`, `SEC-CAP-06`, `SEC-VPS-14`.

## Índice reverso — WSTG v4.2 → itens

- **[INFO](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/01-Information_Gathering/) Coleta de informação:** `INFO-02` → SEC-DEP-01, SEC-NAV-07, SEC-WEB-05; `INFO-03` → SEC-UPL-11; `INFO-05` → SEC-SEG-03; `INFO-06` → SEC-API-08; `INFO-08` → SEC-DEP-01, SEC-NAV-07.
- **[CONF](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/) Configuração e implantação:** `CONF-01` → SEC-BD-06, SEC-BD-09, SEC-VPS-01, SEC-VPS-02, SEC-VPS-05, SEC-VPS-09, SEC-VPS-12, SEC-VPS-15; `CONF-02` → SEC-BD-08, SEC-WEB-09; `CONF-03` → SEC-UPL-07; `CONF-04` → SEC-SEG-02, SEC-VPS-07, SEC-WEB-07; `CONF-05` → SEC-AUTH-16, SEC-API-08; `CONF-07` → SEC-NAV-01; `CONF-09` → SEC-SEG-06, SEC-VPS-04, SEC-VPS-11.
- **[IDNT](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/03-Identity_Management_Testing/) Gestão de identidade:** `IDNT-02` → SEC-AUTH-18, SEC-AUTH-20, SEC-AUTH-21; `IDNT-04` → SEC-AUTH-07, SEC-AUTH-19.
- **[ATHN](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/04-Authentication_Testing/) Autenticação:** `ATHN-01` → SEC-WEB-03; `ATHN-02` → SEC-AUTH-15, SEC-AUTH-22; `ATHN-03` → SEC-AUTH-08, SEC-AUTH-09, SEC-WEB-08; `ATHN-06` → SEC-NAV-06; `ATHN-07` → SEC-AUTH-14; `ATHN-09` → SEC-AUTH-12, SEC-AUTH-23, SEC-AUTH-24, SEC-AUTH-25, SEC-AUTH-26, SEC-AUTH-27, SEC-AUTH-28.
- **[ATHZ](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/05-Authorization_Testing/) Autorização:** `ATHZ-01` → SEC-UPL-04; `ATHZ-02` → SEC-API-01, SEC-API-15, SEC-UPL-08; `ATHZ-03` → SEC-API-02; `ATHZ-04` → SEC-API-01, SEC-BD-10.
- **[SESS](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/06-Session_Management_Testing/) Sessão:** `SESS-01` → SEC-SESS-03, SEC-SESS-04, SEC-SESS-05; `SESS-02` → SEC-SESS-01; `SESS-05` → SEC-SESS-08, SEC-SESS-09; `SESS-06` → SEC-SESS-06; `SESS-07` → SEC-SESS-07.
- **[INPV](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/) Validação de entrada:** `INPV-01` → SEC-API-05, SEC-NAV-08; `INPV-02` → SEC-NAV-08; `INPV-05` → SEC-API-05, SEC-BD-01, SEC-BD-02; `INPV-18` → SEC-API-05; `INPV-19` → SEC-API-13, SEC-API-14.
- **[ERRH](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/08-Testing_for_Error_Handling/) Tratamento de erro:** `ERRH-01` → SEC-API-07, SEC-BD-11; `ERRH-02` → SEC-API-07.
- **[CRYP](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/09-Testing_for_Weak_Cryptography/) Criptografia fraca:** `CRYP-01` → SEC-VPS-15, SEC-WEB-01, SEC-WEB-02, SEC-WEB-04; `CRYP-03` → SEC-WEB-03.
- **[BUSL](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/10-Business_Logic_Testing/) Lógica de negócio:** `BUSL-01` → SEC-API-11, SEC-PAG-02; `BUSL-02` → SEC-API-11, SEC-PAG-02; `BUSL-03` → SEC-PAG-03; `BUSL-05` → SEC-AUTH-20, SEC-BD-03, SEC-BD-05, SEC-PAG-04, SEC-PAG-05, SEC-MSG-01, SEC-MSG-02, SEC-MSG-03; `BUSL-07` → SEC-UPL-09, SEC-PAG-06, SEC-MSG-05, SEC-RL-01, SEC-RL-05, SEC-CAP-02, SEC-CAP-08; `BUSL-08` → SEC-UPL-01; `BUSL-09` → SEC-UPL-02, SEC-UPL-03, SEC-UPL-05.
- **[CLNT](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/11-Client-side_Testing/) Lado do cliente:** `CLNT-01` → SEC-NAV-08, SEC-NAV-09, SEC-NAV-10; `CLNT-04` → SEC-NAV-10; `CLNT-07` → SEC-API-09; `CLNT-09` → SEC-NAV-04; `CLNT-12` → SEC-SESS-02, SEC-LGPD-03.

Testes do WSTG v4.2 ainda sem item correspondente nesta base (lacunas conhecidas; Flash e a
introdução de `BUSL` foram omitidos). Ver
[pesquisa/repositorios-de-referencia.md](../pesquisa/repositorios-de-referencia.md#conteúdo): `ATHN-04`, `ATHN-05`, `ATHN-08`, `ATHN-10`, `BUSL-04`, `BUSL-06`, `CLNT-02`, `CLNT-03`, `CLNT-05`, `CLNT-06`, `CLNT-10`, `CLNT-11`, `CLNT-13`, `CONF-06`, `CONF-10`, `CONF-11`, `SESS-03`, `SESS-04`, `SESS-08`, `SESS-09`.
