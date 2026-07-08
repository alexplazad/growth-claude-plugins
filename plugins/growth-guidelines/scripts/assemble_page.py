#!/usr/bin/env python3
"""
Arma una página HTML on-brand de formato LIBRE (web, 16:9, documento, landing, lo que sea),
reutilizando los tokens y la tipografía de la guía de Growth, pero SIN el stage/navegación de deck.

Para decks usa assemble_deck.py. Para cualquier otro HTML, este script te da una base on-brand
mínima (tokens vivos + Plus Jakarta Sans + escala tipográfica) y envuelve el <body> que tú escribas.
Tú construyes el layout con las variables --* (colores, radios, tamaños); las reglas de marca (M2)
siguen aplicando como default recomendado.

Uso:
  python3 assemble_page.py --cache <guidelines.html> --body <cuerpo.html> --out <pagina.html> [--title "..."]

--body: archivo con el contenido interno del <body> (lo que va dentro), en markup normal.
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

BASE_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html{-webkit-font-smoothing:antialiased;text-size-adjust:100%}
body{font-family:'Plus Jakarta Sans',system-ui,-apple-system,sans-serif;color:var(--ink);
  background:var(--white);line-height:1.6;font-size:var(--fs-body)}
a{color:var(--royal);text-decoration:none}
img{max-width:100%;height:auto}
/* escala tipográfica de la guía (los tamaños vienen de los tokens :root) */
.fs-hero{font-size:var(--fs-hero);font-weight:800;letter-spacing:-.025em;line-height:1.02}
.fs-sep{font-size:var(--fs-sep);font-weight:800;letter-spacing:-.02em;line-height:1.05}
.fs-title{font-size:var(--fs-title);font-weight:800;letter-spacing:-.02em;line-height:1.1}
.fs-lead{font-size:var(--fs-lead);font-weight:500}
.fs-sub{font-size:var(--fs-sub)}
.fs-body{font-size:var(--fs-body)}
.fs-small{font-size:var(--fs-small)}
.fs-note{font-size:var(--fs-note)}
""".strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True, help="guidelines.html cacheado (para los tokens)")
    ap.add_argument("--body", required=True, help="archivo con el contenido del <body>")
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default="Growth · Hites")
    args = ap.parse_args()

    if not os.path.exists(args.cache):
        sys.exit(f"No encuentro el cache en {args.cache}. Corre fetch_guidelines.sh primero.")
    src = open(args.cache, encoding="utf-8").read()
    body = open(args.body, encoding="utf-8").read()

    m = re.search(r":root\{.*?\}", src, flags=re.S)
    if not m:
        sys.exit("No encontré el bloque :root (tokens) en el cache.")
    tokens = m.group(0)

    out = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{args.title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
{tokens}
{BASE_CSS}
</style>
</head>
<body>
{body}
</body>
</html>
"""
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"OK: {args.out} ({len(out)} chars)")


if __name__ == "__main__":
    main()
