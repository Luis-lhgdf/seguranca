# Checklist — Cópias de segurança (BKP)

> **Revisado em:** 2026-10-07. Variáveis e regras em [`AGENTS.md`](../../AGENTS.md). **Nunca** decifrar nem abrir backup de produção; só listar nomes, tamanhos, permissões e datas.

### SEC-BKP-01 — Backup automático do banco e dos arquivos
- **Aplica-se quando:** há dado persistente.
- **Risco se faltar:** perda definitiva em falha ou ataque.
- **Como verificar:** `ssh $VPS 'sudo crontab -l; systemctl list-timers --all | grep -i backup; ls -la --time-style=long-iso <dir-de-backup> | tail'`.
- **OK quando:** diário, cobrindo banco **e** uploads (inclusive privados), último arquivo de hoje/ontem.
- **Referência:** [estrategia.md#1-o-que-entra](estrategia.md#1-o-que-entra).
- **Mapeamento:** Top 10 — · sem requisito ASVS direto.

### SEC-BKP-02 — Backup cifrado com chave pública (servidor não decifra)
- **Aplica-se quando:** o backup contém dado pessoal ou sensível.
- **Risco se faltar:** um arquivo de backup vazado entrega todos os dados.
- **Como verificar:** `ssh $VPS 'ls <dir-de-backup> | grep -vc "\.gpg$"'` (deve ser 0); `ssh $VPS 'sudo -u <usuario-backup> gpg --list-secret-keys 2>/dev/null | grep -c ^sec'` (deve ser 0).
- **OK quando:** 100% cifrados e sem chave privada no servidor.
- **Referência:** [estrategia.md#2--o-backup-é-a-maior-concentração-de-dado-sensível](estrategia.md#2--o-backup-é-a-maior-concentração-de-dado-sensível).
- **Mapeamento:** nível L2 · Top 10 A04:2025 · ASVS V14.2.4 (L2).

### SEC-BKP-03 — Diretório de backup restrito
- **Aplica-se quando:** backup local.
- **Risco se faltar:** qualquer conta do servidor copia o backup.
- **Como verificar:** `ssh $VPS 'stat -c "%a %U %n" <dir-de-backup>'`.
- **OK quando:** `700` com dono do backup.
- **Referência:** [estrategia.md#2--o-backup-é-a-maior-concentração-de-dado-sensível](estrategia.md#2--o-backup-é-a-maior-concentração-de-dado-sensível).
- **Mapeamento:** nível L2 · Top 10 A01:2025, A02:2025 · ASVS V14.2.4 (L2).

### SEC-BKP-04 — Cópia fora do host
- **Aplica-se quando:** produção.
- **Risco se faltar:** perder o disco/a VPS = perder tudo, inclusive o backup.
- **Como verificar:** procurar envio off-site no script; perguntar destino e se a credencial é só de escrita.
- **OK quando:** cópia em outro provedor/local com versionamento — ou risco aceito por escrito com data de reavaliação (PARCIAL).
- **Referência:** [estrategia.md#3-fora-do-host](estrategia.md#3-fora-do-host).
- **Mapeamento:** Top 10 — · sem requisito ASVS direto.

### SEC-BKP-05 — Chave do backup e pepper guardados à parte, com redundância
- **Aplica-se quando:** backup cifrado ou pepper em uso.
- **Risco se faltar:** perder a chave = nenhum backup recuperável; pepper junto do dump = pepper inútil.
- **Como verificar:** perguntar onde estão a chave privada (2 cópias?) e o backup do pepper.
- **OK quando:** locais documentados, separados do dump e redundantes.
- **Referência:** [estrategia.md#4-pepper-e-segredos](estrategia.md#4-pepper-e-segredos).
- **Mapeamento:** nível L2 · Top 10 A04:2025 · ASVS V11.1.1 (L2), V13.3.1 (L2).

### SEC-BKP-06 — Restauração testada recentemente
- **Aplica-se quando:** há backup.
- **Risco se faltar:** descobrir no dia do desastre que o backup não restaura.
- **Como verificar:** procurar registro do último teste (data, ambiente, contagens).
- **OK quando:** teste completo há < 6 meses, procedimento escrito.
- **Referência:** [estrategia.md#6-restauração-testada](estrategia.md#6-restauração-testada).
- **Mapeamento:** Top 10 — · sem requisito ASVS direto.

### SEC-BKP-07 — Retenção do backup alinhada à LGPD
- **Aplica-se quando:** backup com dado pessoal.
- **Risco se faltar:** dado que deveria ter sido apagado continua no backup sem prazo.
- **Como verificar:** ler a rotação dos scripts e a política de retenção.
- **OK quando:** prazo definido e documentado.
- **Referência:** [estrategia.md#5-retenção](estrategia.md#5-retenção).
- **Mapeamento:** nível L3 · Top 10 — · ASVS V14.2.7 (L3).
