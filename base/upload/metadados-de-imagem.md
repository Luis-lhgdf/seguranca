# Upload: metadados de imagem (EXIF, GPS, miniatura) — LGPD

> **Revisado em:** 2026-10-07 · **Origem:** conteúdo compilado de fontes públicas (OWASP, ASVS, NIST, CWE, documentação oficial, avisos de CVE e artigos técnicos) — ver [referências](referencias.md). Se a data estiver antiga (> 6 meses) ou o tema envolver versão/CVE, confirme na fonte oficial antes de aplicar.

## 1. O problema (achado típico em auditoria)

Seis arquivos subidos e baixados pela URL pública voltaram com `sha256` **idêntico** — nada era limpo:

| Formato | O que sobrevivia |
|---|---|
| JPEG | GPS, `DateTimeOriginal`, `CameraOwnerName`, `BodySerialNumber`, `Artist` |
| JPEG | 🔴 **a miniatura embutida (IFD1)** — publica o enquadramento que alguém **decidiu cortar** (numa foto de antes/depois, o corte costuma ser o rosto) |
| PNG | `tEXt`/`iTXt`: nome da fotógrafa, software + nome da máquina da recepção, texto digitado pelo operador |
| WebP | chunk `EXIF` completo — **WebP não é sinônimo de limpo**, é contêiner RIFF |

GPS numa foto de paciente é o endereço onde ela estava; foto de perfil de celular carrega a casa
da pessoa. As travas "nada sensível em URL, log ou erro" **não cobrem isto**: o vazamento está
dentro do arquivo.

## 2. Duas formas de limpar

| | Limpeza estrutural | Reencode a partir dos pixels |
|---|---|---|
| Como | reescreve o contêiner **sem decodificar pixel**: JPEG perde `APPn` e `COM`; PNG mantém só **whitelist** de chunks; WebP perde `EXIF`/`XMP` e a flag correspondente no `VP8X` | `Image.frombytes` dos pixels crus (`.info` vazio) e salva com `exif=b""`, `icc_profile=None`, `pnginfo=None`, `xmp=b""` explícitos (o default varia entre versões do Pillow) |
| Foto 4032×3024 | **0,69 ms** | 1.158 ms |
| Dependência | nenhuma | Pillow (+26 MB na imagem de produção) |
| Bomba de descompressão | não expõe (não decodifica) | exige checar dimensão antes |
| Payload embutido / esteganografia nos pixels | não alcança | destrói |
| Propriedade | **o backend nunca interpreta bytes hostis** | arquivo final é 100% gerado pelo servidor |

Ambas zeram EXIF/GPS/XMP/IPTC/ICC/texto/miniatura. Escolher conscientemente; reencode passa a
fazer sentido quando houver corte/redimensionamento (aí vem junto).

## 3. Como verificar

- Subir foto com GPS e texto conhecido, **baixar pela URL pública** e rodar `exiftool -a -G1 arquivo` — sem GPS, autor, serial, miniatura.
- Varredura bruta pelo texto secreto: `grep -c "<texto>" arquivo` → 0.
- Comparar `sha256` do enviado × baixado: devem diferir.
- Validar também as **imagens estáticas do repositório** (fotos versionadas também carregam metadado).
- Passar o mesmo strip em **todo** upload (catálogo, perfil, documento), não só no primeiro.
