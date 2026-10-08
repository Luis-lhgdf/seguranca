# Cópias de segurança (backup): cifradas, fora do host e restauráveis

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses), confirme na fonte oficial.

## 1. O que entra

- Dump do banco diário (`mysqldump --single-transaction --no-tablespaces | gzip`, ou `pg_dump -Fc`), conferindo o fim íntegro (`-- Dump completed`).
- Arquivos: `uploads` **e** `private_uploads`.
- Config necessária para reerguer (Nginx, systemd, scripts) — versionada no repositório.
- **Não** junto: o `.env`/pepper (ver §4).

## 2. 🔴 O backup é a maior concentração de dado sensível

Um `tar` com fotos e termos **deixa para trás todo o controle de acesso da aplicação**
(`is_private`, rota autenticada, permissão dedicada não valem nada dentro do arquivo). Snapshot de
VPS que vaze, ou leitura de arquivo no servidor, entrega tudo.

**Cifrar na geração, com chave pública** (padrão recomendado):
- GPG **assimétrico**: só a **chave pública** fica na VPS — o servidor cifra mas **não decifra** (`gpg --decrypt` → `No secret key`).
- Chave privada **fora** da VPS, com o responsável, em **2 cópias** separadas. Sem ela, **nenhum** backup é recuperável — registrar onde estão.
- Ao ligar a cifra, cifrar também os arquivos **antigos** (senão a correção é decorativa) e conferir: N cifrados / 0 em claro.
- Diretório de backup `700`, dono do processo de backup.

## 3. Fora do host

- Backup só no mesmo disco não cobre perda do disco/VPS nem comprometimento do host. Alternativa usada na prática em VPS pequena: manter no disco + snapshot de 24 h por custo zero, **reavaliar com o volume de dados** — registrar como risco aceito, não como esquecimento.
- Alvo: destino off-site (outro provedor/bucket com versionamento e bloqueio de deleção; credencial só de escrita a partir da VPS). Regra 3-2-1.
- Snapshot do provedor ≠ backup (expira, fica no mesmo provedor).

## 4. Pepper e segredos

Backup do pepper/segredos **separado** do backup do banco (guardar junto anula o pepper). Perder o
pepper = ninguém loga.

## 5. Retenção

Exemplo de política: banco 14 dias, uploads 7 dias. Alinhar com a política de retenção LGPD — dado
expurgado continua vivo no backup até ele expirar (documentar esse prazo).

## 6. Restauração testada

- Teste periódico num ambiente limpo (chaveiro limpo, banco vazio): decifrar, restaurar, subir a app e conferir contagens (ex.: 82 arquivos, dump com 22 tabelas).
- Registrar data e resultado; sem teste, backup é hipótese.
- Procedimento escrito (runbook), inclusive onde estão as chaves.

## 7. Descarte de mídia

Disco/pendrive com backup descartado: sobrescrever (zero-fill) antes — formatação rápida deixa os
dados recuperáveis por *file carving*.
