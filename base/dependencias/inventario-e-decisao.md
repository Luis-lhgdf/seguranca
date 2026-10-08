# Versões: inventário, checagem na fonte e decisão de subir ou voltar

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Este tema **envelhece rápido**: o agente deve sempre consultar a web na hora da auditoria.

## 1. Inventário (o que levantar em todo projeto)

| Camada | Onde achar a versão em uso |
|---|---|
| SO | `ssh $VPS 'cat /etc/os-release; uname -r'` |
| Linguagens/runtimes | `python3 --version`, `node --version`, `.python-version`, `.nvmrc`, `engines` no `package.json`, `requires-python` |
| Frameworks e libs diretas | `package.json` + lockfile (`package-lock.json`/`pnpm-lock.yaml`), `pyproject.toml` + `uv.lock`/`poetry.lock`/`requirements*.txt` |
| Banco | `mysql --version` / `SELECT VERSION();` / `psql -V`; Redis `redis-server --version` |
| Servidor web | `nginx -v` |
| Ferramentas de deploy | Certbot, Docker (`docker version`), imagens base (`FROM ...` nos Dockerfiles; `docker images`) |
| Serviços externos com SDK | versão do SDK no lockfile |
| GitHub Actions | `uses: owner/action@vX` nos workflows |

Registrar no relatório em "Versões verificadas em AAAA-MM-DD" (ver [`relatorios/MODELO.md`](../../relatorios/MODELO.md)).
**Versão em uso é a do lockfile/servidor, não o piso do manifesto** (`>=23.1` diz pouco; o lock diz `25.1.0`).

## 2. Checar na fonte oficial — sempre na web, na data da auditoria

Para cada item relevante (prioridade: o que recebe entrada externa — framework web, parser de
imagem, driver de banco, lib de crypto/JWT, servidor web, SO):

1. **Versão atual estável** e **fim de suporte**: página de releases oficial; https://endoflife.date/<produto>.
2. **CVE/advisory para a versão em uso**: GitHub Advisory Database, OSV (https://osv.dev), NVD, PyPI Advisory DB (PYSEC), npm advisories, Ubuntu Security Notices (USN) para pacotes do SO, página de segurança do produto (ex.: nginx security advisories).
3. **Changelog** entre a versão em uso e a atual: breaking changes, correções de segurança, regressões conhecidas.
4. **Issues abertas de regressão** na versão nova (GitHub issues do projeto) — atualização recém-lançada pode trazer bug ou, raramente, CVE nova.

Nunca concluir "está atualizado" só pela memória do modelo ou por esta base: citar link e data.

## 3. Decidir: manter, subir ou voltar

| Situação | Recomendação |
|---|---|
| CVE explorável no seu uso, com correção | **subir** (patch/minor) com prioridade pela severidade |
| CVE sem correção upstream | manter, documentar **por que não é explorável** no seu uso (ex.: `asyncmy` PYSEC-2026-286: chaves geradas pelo ORM), monitorar, avaliar alternativa |
| Versão fora de suporte (EOL) | planejar subida de major |
| Versão nova com regressão/CVE própria | **voltar/pinar** na última boa, com issue de acompanhamento |
| Transitiva com alerta sem impacto prático (ex.: `nanoid` em ferramenta de build) | registrar e usar `overrides`/`resolutions` se houver versão corrigida |
| Major disponível sem CVE na atual | não urgente; agendar |

Toda recomendação traz: versão atual → alvo, motivo (CVE/EOL/regressão com link), risco da
mudança (breaking changes) e como validar (testes, smoke test, staging).

## 4. Prazos de remediação (ASVS V15.1.1)

Documentar e cumprir, por exemplo: crítica 7 dias · alta 30 dias · média 90 dias · baixa no ciclo
normal. Sem prazo escrito, "vamos atualizar" não é controle.
