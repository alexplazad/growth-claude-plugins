#!/usr/bin/env python3
"""
Linter de marca para decks de Growth (Hites). Pasada MECÁNICA del Modo REVISAR: detecta lo que se
puede verificar objetivamente. La pasada de criterio (composición, jerarquía, diagramas héroe) la
hace Claude leyendo references/design-system.md.

Revisa SOLO el contenido de autor (estilos inline y texto de las láminas). Ignora a propósito los
bloques <style> y <script> del shell oficial, que sí definen tokens/magenta/hex legítimamente.

Uso:  python3 brand_check.py <deck.html>
Salida: una línea por hallazgo (con nº de línea) y un SUMMARY final. Exit 1 si hay VIOLATION.
"""
import re
import sys

# Paleta oficial de tokens (hex en minúscula). Fuera de esto = off-brand.
TOKENS = {
    "#0058ba", "#2559be", "#15137e", "#002492", "#fa8100", "#ffa64d", "#fff1e2",
    "#fa1eb3", "#ffe8f6", "#ea2e3b", "#ffe9ea", "#8490a0", "#ffffff", "#1b47a0",
    "#e85d00", "#eaf2fb", "#f4f8fd", "#dee6f0", "#c8daf0", "#eef1f5", "#22262e",
    "#5c6675", "#5a6472", "#0a1430", "#e6eef8",
}
ALLOW_SHORT = {"#fff", "#000", "#f001"}  # blancos/negros comunes de conveniencia
FS_SCALE = {"124", "88", "58", "46", "24", "20", "17", "14", "13", "66", "50"}
MAGENTA = {"#fa1eb3", "--magenta"}
ARROWS = "→➜➔➙➛➜➝➞➟➠➡⟶⇒⇨▶►▸»↦"  # glifos de flecha direccional


def block_lines(text, tag):
    """Números de línea (1-based) cubiertos por bloques <tag>…</tag>, para ignorarlos."""
    covered = set()
    for m in re.finditer(r"<" + tag + r"[^>]*>.*?</" + tag + r">", text, flags=re.S):
        start = text.count("\n", 0, m.start()) + 1
        end = text.count("\n", 0, m.end()) + 1
        covered.update(range(start, end + 1))
    return covered


def hexes(s):
    return [h.lower() for h in re.findall(r"#[0-9A-Fa-f]{3,8}\b", s)]


def main():
    if len(sys.argv) < 2:
        sys.exit("Uso: brand_check.py <deck.html>")
    path = sys.argv[1]
    text = open(path, encoding="utf-8").read()
    lines = text.split("\n")
    skip = block_lines(text, "style") | block_lines(text, "script")

    violations, warnings = [], []

    for i, line in enumerate(lines, 1):
        if i in skip:
            continue

        # Estilos inline del autor
        for style in re.findall(r'style\s*=\s*"([^"]*)"', line):
            low = style.lower()

            # 1) Magenta como relleno/fondo -> VIOLATION
            for prop in ("background", "background-color", "background-image", "fill"):
                m = re.search(prop + r"\s*:\s*([^;]+)", low)
                if m and any(tok in m.group(1) for tok in MAGENTA):
                    violations.append((i, "MAGENTA_FILL",
                                       f"magenta usado en '{prop}' (jamás de relleno; solo texto/borde)"))

            # 2) font-size inline fuera de la escala .fs-* -> WARNING.
            # El sistema oficial SÍ usa ajustes inline puntuales (p. ej. achicar una cifra héroe
            # dentro de una card), así que no es violación dura; es una señal para verificar que
            # sea un ajuste deliberado y no un ramp tipográfico caótico.
            for fs in re.findall(r"font-size\s*:\s*([^;]+)", low):
                fs = fs.strip()
                if "var(--fs" in fs:
                    continue
                px = re.match(r"(\d+)px$", fs)
                if px and px.group(1) not in FS_SCALE:
                    warnings.append((i, "FONT_SIZE",
                                     f"font-size {fs} fuera de la escala .fs-* — verifica que sea ajuste puntual"))
                elif not px:
                    warnings.append((i, "FONT_SIZE?",
                                     f"font-size inline '{fs}' — prefiere una clase .fs-*"))

            # 3) font-family inline -> VIOLATION (debe heredar Plus Jakarta Sans)
            if "font-family" in low:
                violations.append((i, "FONT_FAMILY",
                                   "font-family inline (una sola tipografía: Plus Jakarta Sans, heredada)"))

            # 4) Hex fuera de la paleta de tokens -> VIOLATION
            for h in hexes(style):
                if h in TOKENS or h in ALLOW_SHORT:
                    continue
                violations.append((i, "OFF_PALETTE",
                                   f"color {h} fuera de la paleta de tokens (usa var(--*))"))

        # 5) Flechas direccionales en texto visible -> WARNING (solo se permiten en el mapa del motor)
        visible = re.sub(r"<[^>]+>", "", line)
        for ch in visible:
            if ch in ARROWS:
                warnings.append((i, "ARROW",
                                 f"glifo de flecha '{ch}' — permitido solo en el mapa del motor; "
                                 "en bullets/navegación, nunca"))
                break

    for ln, code, msg in sorted(violations):
        print(f"VIOLATION  L{ln:<5} [{code}] {msg}")
    for ln, code, msg in sorted(warnings):
        print(f"WARNING    L{ln:<5} [{code}] {msg}")

    print(f"\nSUMMARY: {len(violations)} violaciones, {len(warnings)} advertencias en {path}")
    if not violations and not warnings:
        print("Sin hallazgos mecánicos. Falta la pasada de criterio (composición/diagramas héroe).")
    sys.exit(1 if violations else 0)


if __name__ == "__main__":
    main()
