#!/usr/bin/env python3
"""
Extrae piezas puntuales del documento de guidelines SIN que Claude tenga que leer los ~226 KB.
Es la clave de rendimiento: en vez de ingerir todo el archivo, se pide solo lo necesario.

Uso:
  python3 extract.py --cache <guidelines.html> --list
      -> índice compacto: una línea por lámina (índice · etiqueta · componentes detectados).
  python3 extract.py --cache <guidelines.html> --slide N
      -> imprime el markup completo de la lámina N (para copiar su patrón).
  python3 extract.py --cache <guidelines.html> --find PALABRA
      -> imprime la primera lámina que contiene PALABRA (con su índice).
  python3 extract.py --cache <guidelines.html> --tokens
      -> imprime solo el bloque :root (tokens) — útil para HTML libre.
"""
import argparse
import re
import sys
import html as _html

COMPONENTS = [
    "cup", "loop-ring", "atom", "oatom", "matriz", "quad", "gantt", "flow-arrow",
    "tree", "okr", "table", "th", "card-soft", "ccard", "bul", "toc", "sep",
    "hmark", "grid-bg", "drawbox", "sparkline", "stat", "chip",
]


def get_slides(src):
    return re.findall(r'<section class="slide.*?</section>', src, flags=re.S)


def label(slide):
    for cls in ("dtitle", "covertitle", "septitle", "fs-title"):
        m = re.search(r'class="[^"]*' + cls + r'[^"]*"[^>]*>(.*?)<', slide)
        if m:
            t = _html.unescape(re.sub(r"\s+", " ", m.group(1))).strip()
            if t:
                return t[:52]
    return "(sin título)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--list", action="store_true")
    g.add_argument("--slide", type=int)
    g.add_argument("--find")
    g.add_argument("--tokens", action="store_true")
    args = ap.parse_args()

    src = open(args.cache, encoding="utf-8").read()

    if args.tokens:
        m = re.search(r":root\{.*?\}", src, flags=re.S)
        print(m.group(0) if m else "(:root no encontrado)")
        return

    slides = get_slides(src)

    if args.list:
        print(f"# {len(slides)} láminas en la guía")
        for i, s in enumerate(slides):
            comps = [c for c in COMPONENTS if c in s]
            print(f"{i:>2} | {label(s):<52} | {','.join(sorted(set(comps)))}")
        return

    if args.slide is not None:
        if 0 <= args.slide < len(slides):
            print(slides[args.slide])
        else:
            sys.exit(f"Índice fuera de rango (0..{len(slides)-1})")
        return

    if args.find:
        kw = args.find.lower()
        for i, s in enumerate(slides):
            if kw in s.lower():
                print(f"<!-- lámina {i} -->")
                print(s)
                return
        sys.exit(f"Ninguna lámina contiene '{args.find}'")


if __name__ == "__main__":
    main()
