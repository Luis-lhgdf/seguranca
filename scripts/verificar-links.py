"""Confere links relativos e âncoras (#seção) entre os .md do repositório.

Uso: python scripts/verificar-links.py
Sai com código 1 se algum link apontar para arquivo ou seção inexistente.
A âncora segue a regra do GitHub: minúsculas, remove pontuação, espaço vira hífen.
"""

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
LINK = re.compile(r"\]\(([^)\s]+)\)")
TITULO = re.compile(r"^#{1,6}\s+(.*)$")


def slug(titulo: str) -> str:
    titulo = re.sub(r"[`*]", "", titulo.strip().lower())
    titulo = re.sub(r"[^\w\- ]", "", titulo)
    return titulo.replace(" ", "-")


def ancoras(arquivo: Path) -> set[str]:
    vistas: dict[str, int] = {}
    saida = set()
    dentro_de_codigo = False
    for linha in arquivo.read_text(encoding="utf-8").splitlines():
        if linha.startswith("```"):
            dentro_de_codigo = not dentro_de_codigo
            continue
        m = None if dentro_de_codigo else TITULO.match(linha)
        if m:
            base = slug(m.group(1))
            n = vistas.get(base, 0)
            saida.add(base if n == 0 else f"{base}-{n}")
            vistas[base] = n + 1
    return saida


def main() -> int:
    erros = []
    for md in sorted(RAIZ.rglob("*.md")):
        if ".git" in md.parts:
            continue
        for alvo in LINK.findall(md.read_text(encoding="utf-8")):
            if alvo.startswith(("http://", "https://", "mailto:")):
                continue
            caminho, _, ancora = alvo.partition("#")
            destino = (md.parent / caminho).resolve() if caminho else md
            if not destino.exists():
                erros.append(f"{md.relative_to(RAIZ)}: arquivo não existe -> {alvo}")
                continue
            if ancora and destino.suffix == ".md" and ancora not in ancoras(destino):
                erros.append(f"{md.relative_to(RAIZ)}: seção não existe -> {alvo}")
    for e in erros:
        print(e)
    print(f"{len(erros)} problema(s).")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
