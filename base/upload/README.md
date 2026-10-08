# Upload e mídia

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md).

**Cobre:** validação de arquivo (magic bytes, SVG, bomba, nome, tamanho), metadados de imagem
(EXIF/GPS/miniatura), mídia pública × privada, cache e raspagem de galeria.
**Aplica-se quando:** o sistema aceita arquivo de usuário ou admin. Sem upload → N/A.

| Arquivo | Conteúdo |
|---|---|
| [validacao-de-arquivo.md](validacao-de-arquivo.md) | defesas e testes |
| [metadados-de-imagem.md](metadados-de-imagem.md) | o que vaza, limpeza estrutural × reencode, como verificar |
| [midia-publica-e-privada.md](midia-publica-e-privada.md) | dois roots, cache, gate de conteúdo, raspagem |
| [referencias.md](referencias.md) | fontes oficiais e mapeamento Top 10 / ASVS / WSTG |
| [checklist.md](checklist.md) | itens `SEC-UPL-*` (com nível ASVS e mapeamento) |
