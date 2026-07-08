#!/usr/bin/env python3
"""
Ensambla un deck on-brand completo reutilizando el shell del documento oficial de guidelines.

Toma el <head> (fuente + <style> con tokens y componentes) y el <script> (escalado del stage,
count-up, drawboxes, navegación) del cache `assets/design-guidelines.html`, e inserta tus láminas
dentro de #stage. Así NO reescribes el CSS de 132 KB a mano y garantizas fidelidad de marca.

Uso:
  python3 assemble_deck.py --slides laminas.html --out "Growth-Tema-2026.html" [--title "Título"]

--slides: archivo HTML con solo los <section class="slide">…</section> en orden. La primera lámina
          se marca .active automáticamente si ninguna lo está.
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", "assets", "design-guidelines.html")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slides", required=True, help="HTML con las <section class=slide> del deck")
    ap.add_argument("--out", required=True, help="Ruta del deck .html a generar")
    ap.add_argument("--title", default=None, help="Título del <title> (opcional)")
    ap.add_argument("--cache", default=CACHE, help="Ruta al design-guidelines.html cacheado")
    args = ap.parse_args()

    if not os.path.exists(args.cache):
        sys.exit(f"No encuentro el cache de guidelines en {args.cache}. Corre fetch_guidelines.sh primero.")
    src = open(args.cache, encoding="utf-8").read()
    slides = open(args.slides, encoding="utf-8").read().strip()

    head_end = src.find("</head>")
    if head_end == -1:
        sys.exit("El cache no tiene </head>; ¿está corrupto?")
    head = src[: head_end + len("</head>")]

    scripts = re.findall(r"<script[^>]*>.*?</script>", src, flags=re.S)
    if not scripts:
        sys.exit("El cache no tiene <script>; ¿está corrupto?")
    script_block = "\n".join(scripts)

    # Asegura una lámina activa
    if "slide active" not in slides and 'slide"' in slides:
        slides = slides.replace('class="slide', 'class="slide active', 1)
    elif "active" not in slides:
        # variantes como class="slide dark"
        slides = re.sub(r'class="slide(?![^"]*active)', 'class="slide active', slides, count=1)

    if args.title:
        head = re.sub(r"<title>.*?</title>", f"<title>{args.title}</title>", head, flags=re.S)

    out = (
        head
        + '\n<body>\n<div id="viewport"><div id="stage">\n'
        + slides
        + "\n</div></div>\n"
        + script_block
        + "\n</body></html>\n"
    )
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(out)
    n = len(re.findall(r'<section class="slide', slides))
    print(f"OK: {args.out} ({len(out)} chars, {n} láminas)")


if __name__ == "__main__":
    main()
