#!/usr/bin/env bash
# Descarga la última versión del sistema de diseño de Growth (Hites) y la deja en un cache
# EDITABLE, actualizando solo si el contenido cambió. Reporta el estado y la ruta del cache.
#
# Estados (penúltima línea de stdout):
#   STATUS=UPDATED    -> el documento cambió; el cache se actualizó
#   STATUS=UNCHANGED  -> el documento es idéntico al cache
#   STATUS=OFFLINE    -> no se pudo descargar; se conserva el cache existente (o el seed)
#   STATUS=NOCREDS    -> faltan credenciales; no se intentó descargar (se usa el seed)
# Última línea siempre: CACHE_PATH=<ruta al HTML que debe leerse>
#
# CREDENCIALES (obligatorias, NO vienen incluidas por seguridad — este archivo se comparte por git):
#   export GROWTH_GUIDELINES_USER="growth.hites"
#   export GROWTH_GUIDELINES_PASS="•••"
# Distribúyelas por el bloque `env` de la configuración administrada del equipo, o cada quien las
# exporta una vez en su shell. Nunca las escribas aquí.
set -euo pipefail

URL="https://growth-guidelines.pages.dev/design-guidelines"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SEED="$SCRIPT_DIR/../assets/design-guidelines.html"   # copia semilla que viene con el plugin (solo lectura)

# Cache editable y persistente entre updates del plugin.
CACHE_DIR="${CLAUDE_PLUGIN_DATA:-$HOME/.cache/growth-hites-guidelines}"
mkdir -p "$CACHE_DIR" 2>/dev/null || CACHE_DIR="$(mktemp -d)"
CACHE="$CACHE_DIR/design-guidelines.html"

# Si no hay cache aún, siémbralo con la copia del plugin para tener siempre algo utilizable.
if [ ! -f "$CACHE" ] && [ -f "$SEED" ]; then cp "$SEED" "$CACHE" 2>/dev/null || true; fi

report() { echo "$1"; echo "CACHE_PATH=$CACHE"; }

# Credenciales, en orden: 1) variables de entorno; 2) archivo local que creó setup_credentials.sh.
# Nunca vienen en el repo. Si no hay ninguna, se reporta NOCREDS y la skill guiará el setup.
CREDS_FILE="${GROWTH_GUIDELINES_CREDS:-${CLAUDE_PLUGIN_DATA:-$HOME/.config/growth-hites-guidelines}/credentials}"
USER="${GROWTH_GUIDELINES_USER:-}"
PASS="${GROWTH_GUIDELINES_PASS:-}"
if { [ -z "$USER" ] || [ -z "$PASS" ]; } && [ -f "$CREDS_FILE" ]; then
  # shellcheck disable=SC1090
  . "$CREDS_FILE"
  USER="${GROWTH_GUIDELINES_USER:-}"
  PASS="${GROWTH_GUIDELINES_PASS:-}"
fi
if [ -z "$USER" ] || [ -z "$PASS" ]; then
  echo "Sin credenciales. Corre una vez setup_credentials.sh (o exporta GROWTH_GUIDELINES_USER/PASS)." >&2
  report "STATUS=NOCREDS"; exit 0
fi

TMP="$(mktemp)"; trap 'rm -f "$TMP"' EXIT
if ! curl -fsSL -u "$USER:$PASS" "$URL" -o "$TMP" 2>/dev/null; then
  echo "No se pudo descargar; se usa el cache existente." >&2
  report "STATUS=OFFLINE"; exit 0
fi
if [ ! -s "$TMP" ] || [ "$(wc -c < "$TMP")" -lt 10000 ]; then
  echo "Descarga inválida (muy pequeña); se conserva el cache." >&2
  report "STATUS=OFFLINE"; exit 0
fi

new_sum="$(shasum -a 256 "$TMP" | awk '{print $1}')"
old_sum="none"; [ -f "$CACHE" ] && old_sum="$(shasum -a 256 "$CACHE" | awk '{print $1}')"
if [ "$new_sum" = "$old_sum" ]; then
  report "STATUS=UNCHANGED"
else
  mv "$TMP" "$CACHE"; trap - EXIT
  report "STATUS=UPDATED"
fi
