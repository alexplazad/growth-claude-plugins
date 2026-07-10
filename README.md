# Growth · Hites — Plugins de Claude Code

Marketplace de plugins de Claude Code del equipo de Growth (Hites).

## Plugins

### `growth-guidelines`
Crea y audita **HTML on-brand** usando el sistema de diseño de Growth: decks/presentaciones,
páginas web, formatos 16:9, landings y documentos HTML. Descarga sola la última versión vigente de
las guidelines antes de trabajar, así que siempre produce material actualizado. Incluye un revisor de
marca (linter) para auditar HTML existente.

## Instalación (una vez por persona)

En una terminal interactiva de Claude Code:

```
/plugin marketplace add alexplazad/growth-claude-plugins
/plugin install growth-guidelines@growth-hites-plugins
```

Cuando pregunte el scope de instalación, elige **Install for you (user scope)**. Eso deja el plugin
disponible en todos tus chats/proyectos de esta máquina.

> Reemplaza `alexplazad/growth-claude-plugins` por el slug real del repo si es distinto.

Para que el equipo lo tenga sin pasos manuales, un admin puede fijarlo en la configuración
administrada (`extraKnownMarketplaces` + `enabledPlugins`) con `autoUpdate: true`.

## Credenciales (una sola vez)

Por seguridad, el plugin **no incluye la contraseña** del sitio de guidelines. Cada persona la
configura **una vez** y la skill la usa sola desde ahí (no se vuelve a pedir).

- **Setup guiado (una vez):** después de instalar, corre en tu terminal normal:
  ```bash
  bash "$(find ~/.claude/plugins -name setup_credentials.sh -path '*growth-guidelines*' | head -1)"
  ```
  Pregunta usuario y contraseña **en tu terminal** (nunca en el chat) y las guarda en tu equipo con
  permisos `600`. La contraseña muestra un `•` por cada carácter escrito/pegado. No toca el repo ni
  pasa por la IA.
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
plugins/growth-guidelines/
├── .claude-plugin/plugin.json           # manifiesto del plugin
├── skills/growth-guidelines/SKILL.md
├── scripts/   (fetch_guidelines.sh · setup_credentials.sh · extract.py · assemble_deck.py ·
│               assemble_page.py · brand_check.py)
├── references/design-system.md          # resumen destilado de tokens y reglas
└── assets/                              # sin copia interna; el documento se baja en runtime
```
