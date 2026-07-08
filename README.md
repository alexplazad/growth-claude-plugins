# Growth · Hites — Plugins de Claude Code

Marketplace de plugins de Claude Code del equipo de Growth (Hites).

## Plugins

### `growth-hites-presentations`
Genera y audita **presentaciones/decks on-brand** siguiendo el sistema de diseño de Growth.
Descarga sola la última versión vigente de las guidelines antes de trabajar, así que siempre produce
material actualizado. Incluye un revisor de marca (linter) para auditar decks existentes.

## Instalación (una vez por persona)

En una terminal interactiva de Claude Code:

```
/plugin marketplace add alexplazad/growth-claude-plugins
/plugin install growth-hites-presentations@growth-hites-plugins
```

> Reemplaza `alexplazad/growth-claude-plugins` por el slug real del repo si es distinto.

Para que el equipo lo tenga sin pasos manuales, un admin puede fijarlo en la configuración
administrada (`extraKnownMarketplaces` + `enabledPlugins`) con `autoUpdate: true`.

## Credenciales (una sola vez)

Por seguridad, el plugin **no incluye la contraseña** del sitio de guidelines. Cada persona la
configura **una vez** y la skill la usa sola desde ahí (no se vuelve a pedir).

- **Setup guiado (recomendado):** la primera vez, la skill te pedirá correr en tu terminal:
  ```bash
  bash "${CLAUDE_PLUGIN_ROOT}/scripts/setup_credentials.sh"
  ```
  Pregunta usuario y contraseña **en tu terminal** (nunca en el chat) y las guarda en tu equipo con
  permisos `600`. No tocan el repo.
- **Equipo, cero toque:** un admin puede ponerlas en el bloque `env` de la configuración administrada
  (`GROWTH_GUIDELINES_USER` / `GROWTH_GUIDELINES_PASS`) y le llegan a todos.
- **Manual:** exportarlas en `~/.zshrc` / `~/.bashrc`.

Este repo **no incluye** el documento de guidelines (es contenido interno); la skill lo baja en
runtime con las credenciales y lo cachea localmente.

## Actualizaciones

Con `autoUpdate` activado, los cambios que se publiquen aquí llegan solos al arrancar Claude Code.
Si no, cada quien corre `/plugin marketplace update`.

## Estructura

```
.claude-plugin/marketplace.json          # lista de plugins del marketplace
plugins/growth-hites-presentations/
├── .claude-plugin/plugin.json           # manifiesto del plugin
├── skills/growth-hites-presentations/SKILL.md
├── scripts/   (fetch_guidelines.sh · assemble_deck.py · brand_check.py)
├── references/design-system.md          # resumen destilado de tokens y reglas
└── assets/                              # sin copia interna; el documento se baja en runtime
```
