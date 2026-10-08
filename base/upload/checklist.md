# Checklist — Upload e mídia (UPL)

> **Revisado em:** 2026-10-07. Variáveis e regras em [`AGENTS.md`](../../AGENTS.md). Uploads de teste **só em ambiente local/de teste**.

### SEC-UPL-01 — Tipo real por magic bytes, com whitelist
- **Aplica-se quando:** há upload.
- **Risco se faltar:** um arquivo executável disfarçado de imagem entra no servidor.
- **Como verificar:** ler o serviço de upload (sniff dos primeiros bytes, lista permitida); em teste, subir `.php` e `.html` renomeados → recusados.
- **OK quando:** extensão/`Content-Type` ignorados; só tipos da whitelist.
- **Referência:** [validacao-de-arquivo.md#1-as-defesas](validacao-de-arquivo.md#1-as-defesas) · ASVS V5.2.2.

### SEC-UPL-02 — SVG recusado
- **Aplica-se quando:** há upload de imagem.
- **Risco se faltar:** SVG com script executa no domínio do site (XSS armazenado).
- **Como verificar:** em teste, subir SVG com `<script>` → recusado; conferir allowlist.
- **OK quando:** SVG fora (ou sanitizado e servido de domínio separado, decisão escrita).
- **Referência:** [validacao-de-arquivo.md#3-serviço-de-arquivo-e-xss](validacao-de-arquivo.md#3-serviço-de-arquivo-e-xss).

### SEC-UPL-03 — Proteção contra bomba de descompressão
- **Aplica-se quando:** o servidor decodifica imagem.
- **Risco se faltar:** uma imagem pequena consome GB de memória e CPU.
- **Como verificar:** procurar checagem de dimensão antes do decode e `MAX_IMAGE_PIXELS`.
- **OK quando:** teto de dimensão antes de decodificar (ou nenhum decode).
- **Referência:** [validacao-de-arquivo.md#1-as-defesas](validacao-de-arquivo.md#1-as-defesas).

### SEC-UPL-04 — Nome gerado pelo servidor e sem path traversal
- **Aplica-se quando:** há upload.
- **Risco se faltar:** sobrescrever arquivo do sistema ou gravar fora da pasta.
- **Como verificar:** ler a geração do nome (UUID) e a checagem `commonpath`; em teste, nome `../../etc/passwd` → gravado como `<uuid>.ext` no diretório.
- **OK quando:** nome enviado descartado; destino validado.
- **Referência:** [validacao-de-arquivo.md#2-testes-que-provam](validacao-de-arquivo.md#2-testes-que-provam) · ASVS V5.3.2.

### SEC-UPL-05 — Limite de tamanho no app e na borda
- **Aplica-se quando:** há upload.
- **Risco se faltar:** arquivos enormes enchem o disco ou derrubam o serviço.
- **Como verificar:** teto no código; `ssh $VPS 'sudo nginx -T | grep -n client_max_body_size'`.
- **OK quando:** os dois tetos existem e são coerentes.
- **Referência:** [validacao-de-arquivo.md#1-as-defesas](validacao-de-arquivo.md#1-as-defesas).

### SEC-UPL-06 — Metadados removidos (EXIF, GPS, miniatura, texto)
- **Aplica-se quando:** há upload de imagem — **crítico** se for foto de pessoa.
- **Risco se faltar:** a foto publicada revela onde e quando foi tirada, quem tirou, e até o rosto cortado.
- **Como verificar:** baixar uma imagem publicada pela URL pública e rodar `exiftool -a -G1 <arquivo>`; em teste, subir foto com GPS e conferir o servido.
- **OK quando:** nenhum GPS, autor, serial, texto ou miniatura nos arquivos servidos.
- **Referência:** [metadados-de-imagem.md#3-como-verificar](metadados-de-imagem.md#3-como-verificar).

### SEC-UPL-07 — Diretório de upload sem listagem e com `nosniff`
- **Aplica-se quando:** arquivos servidos pelo servidor web.
- **Risco se faltar:** qualquer um lista todos os arquivos; navegador "adivinha" tipo executável.
- **Como verificar:** `curl -s -o /dev/null -w '%{http_code}' $SITE/uploads/` → 403/404; `curl -sI $SITE/uploads/<arquivo> | grep -i nosniff`.
- **OK quando:** sem listagem e com `nosniff`.
- **Referência:** [validacao-de-arquivo.md#1-as-defesas](validacao-de-arquivo.md#1-as-defesas).

### SEC-UPL-08 — Mídia privada fora do alcance público
- **Aplica-se quando:** há arquivos privados (documentos, termos).
- **Risco se faltar:** documento com nome de pessoa acessível por URL.
- **Como verificar:** confirmar que o root privado não aparece em `nginx -T` nem em montagem de estáticos; tentar a URL direta → 404; rota autenticada com permissão própria e `Cache-Control: no-store`.
- **OK quando:** só rota autenticada e auditada serve o privado.
- **Referência:** [midia-publica-e-privada.md#1-dois-roots](midia-publica-e-privada.md#1-dois-roots).

### SEC-UPL-09 — Acervo sensível não raspável sem controle
- **Aplica-se quando:** há galeria/listagem pública de mídia sensível.
- **Risco se faltar:** um script baixa todas as fotos de pacientes/clientes.
- **Como verificar:** de fora, `curl` na listagem e na rota de mídia sem sessão e sem aceite; checar rate limit dos GET públicos; checar alerta de volume no log.
- **OK quando:** gate com contrapartida no servidor + rate limit + alerta — ou desvio aceito por escrito pelo responsável.
- **Referência:** [midia-publica-e-privada.md#3-galeria-sensível-e-raspagem](midia-publica-e-privada.md#3-galeria-sensível-e-raspagem).

### SEC-UPL-10 — Cache de mídia sensível permite recolher
- **Aplica-se quando:** mídia sensível pública.
- **Risco se faltar:** foto publicada por engano continua em cache por semanas.
- **Como verificar:** `curl -sI $SITE/uploads/<arquivo sensível> | grep -i cache-control`.
- **OK quando:** cache curto (ou decisão escrita) para mídia sensível.
- **Referência:** [midia-publica-e-privada.md#2-arquivo-público-é-público-por-natureza](midia-publica-e-privada.md#2-arquivo-público-é-público-por-natureza).

### SEC-UPL-11 — Crawlers fora das pastas de mídia
- **Aplica-se quando:** mídia sensível pública.
- **Risco se faltar:** fotos indexadas por buscadores e datasets de IA.
- **Como verificar:** `curl -s $SITE/robots.txt` — `Disallow: /uploads/` para `*` e crawlers de IA; sitemap sem slugs sensíveis.
- **OK quando:** os dois atendidos (lembrando que robots não é controle de acesso).
- **Referência:** [midia-publica-e-privada.md#3-galeria-sensível-e-raspagem](midia-publica-e-privada.md#3-galeria-sensível-e-raspagem).
