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

## Credenciales (requeridas)

Por seguridad, el plugin **no incluye la contraseña** del sitio de guidelines. Cada usuario define:

```bash
export GROWTH_GUIDELINES_USER="growth.hites"
export GROWTH_GUIDELINES_PASS="•••"   # pídela al equipo; no la escribas en el repo
```

- **Recomendado (equipo):** distribuirlas por el bloque `env` de la configuración administrada.
- **Individual:** exportarlas en `~/.zshrc` / `~/.bashrc`.

Sin credenciales, la skill trabaja con la copia semilla incluida (puede estar desactualizada).

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
├── references/design-system.md
└── assets/design-guidelines.html        # copia semilla (se refresca en runtime)
```
