#!/usr/bin/env bash
# Setup de credenciales de UNA SOLA VEZ para el sistema de guidelines de Growth.
# Se corre manualmente en TU terminal. La contraseña se lee directo aquí (no pasa por el chat/IA)
# y se guarda solo en tu equipo, con permisos restringidos. Después, la skill la usa sola y no
# vuelve a pedirla. Estas credenciales NUNCA se guardan en el repo del plugin.
set -euo pipefail

CREDS_DIR="${GROWTH_GUIDELINES_CREDS_DIR:-${CLAUDE_PLUGIN_DATA:-$HOME/.config/growth-hites-guidelines}}"
CREDS_FILE="$CREDS_DIR/credentials"
mkdir -p "$CREDS_DIR"
chmod 700 "$CREDS_DIR" 2>/dev/null || true

echo "Credenciales del sistema de guidelines de Growth (Hites)."
echo "Se guardan solo en este equipo: $CREDS_FILE"
echo

# -r: no interpretar barras · -s: no mostrar la contraseña en pantalla
read -r  -p "Usuario: " GG_USER
read -rs -p "Contraseña: " GG_PASS
echo

if [ -z "${GG_USER:-}" ] || [ -z "${GG_PASS:-}" ]; then
  echo "Usuario o contraseña vacíos. No se guardó nada." >&2
  exit 1
fi

umask 177  # el archivo nace 600 (solo tú lo lees)
# %q escapa para que el archivo sea sourceable aunque la contraseña tenga caracteres especiales.
{ printf 'GROWTH_GUIDELINES_USER=%q\n' "$GG_USER"
  printf 'GROWTH_GUIDELINES_PASS=%q\n' "$GG_PASS"; } > "$CREDS_FILE"
chmod 600 "$CREDS_FILE"

echo "✅ Listo. Guardado en $CREDS_FILE (solo lectura para ti)."
echo "   La skill lo usará sola de ahora en adelante; no se te volverá a pedir."
