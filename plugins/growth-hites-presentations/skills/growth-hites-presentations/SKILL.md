---
name: growth-hites-presentations
description: >-
  Genera y audita presentaciones/decks on-brand del equipo de Growth de Hites (paleta,
  tipografía Plus Jakarta Sans, componentes, diagramas héroe y animaciones). Descarga sola
  la ÚLTIMA versión vigente de las guidelines antes de trabajar, así que siempre usa material
  actualizado sin descargas manuales. Úsala siempre que el usuario pida armar una presentación,
  deck, láminas, slides o pitch de Growth/Hites, cuando pida algo "en la línea/estilo de Growth"
  o "según las guidelines", cuando quiera revisar/auditar si un deck cumple la marca, o cuando
  mencione la paleta, tipografía o componentes del equipo — aunque no diga explícitamente
  "presentación".
---

# Presentaciones on-brand · Growth Hites

Esta skill hace dos cosas con el sistema de diseño de Growth (Hites): **crea** decks HTML
autocontenidos que cumplen la marca, y **revisa/audita** decks existentes contra las guidelines.
El sistema oficial vive en un documento en línea que se actualiza solo cada vez que el equipo lo
cambia; la skill lo baja fresco antes de trabajar, para que nunca uses una versión vieja.

La skill está pensada para **compartirse en equipo**: el *motor on-brand* (Pasos M0–M2) es común a
todos y no se toca por gusto; los *modos de flujo* (índice-primero, presets) son **opcionales y
personales**, para que cada quien trabaje a su manera sin forzar a los demás.

---

## Preferencias personales (opcional)

Antes de empezar, revisa si existe un archivo de preferencias personales del usuario:
`~/.claude/growth-presentations.prefs.md`. **Es personal y vive fuera de la skill compartida**, así
que cada persona configura sus defaults sin afectar al equipo.

- **Si existe** → léelo y aplica sus defaults (p. ej. `indice_primero: sí`, `audiencia_default:
  ejecutivo`). Trátalo como "esta persona ya decidió su forma de trabajar": respétalo en silencio y
  **no ofrezcas modos proactivamente** (el archivo es el interruptor de "ya decidí, no me preguntes").
- **Si NO existe** → la persona probablemente aún no conoce los modos opcionales. Usa los defaults
  neutros de abajo y, la **primera vez** que armes un deck no trivial en la sesión, **recomiéndale
  una sola vez** (en una línea, sin insistir) los modos de alto valor —sobre todo índice-primero— y
  ofrécele dejarlos como default. No crees el archivo tú salvo que lo pida.
- Una petición explícita en el chat **siempre gana** sobre todo lo anterior (p. ej. "esta vez sin índice").

Defaults neutros si no hay archivo: índice-primero **desactivado**; audiencia sin asumir; largo
según el contenido; guardar en la **carpeta actual de trabajo**; al terminar **solo ofrecer** abrir
(no abrir por tu cuenta).

---

## El motor on-brand (siempre)

### M0 — Refresca las guidelines

Corre el script de refresco. Baja la última versión y solo actualiza el cache si cambió:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/fetch_guidelines.sh"
```

El script imprime dos líneas útiles: `STATUS=...` y `CACHE_PATH=...` (la ruta del HTML que debes
leer/usar). Interpreta el estado:
- `STATUS=UPDATED` — cambió; menciónalo y usa la versión nueva.
- `STATUS=UNCHANGED` — ya tienes la última.
- `STATUS=OFFLINE` — sin conexión; avisa que trabajas con el cache local y sigue.
- `STATUS=NOCREDS` — faltan las credenciales (`GROWTH_GUIDELINES_USER` / `GROWTH_GUIDELINES_PASS`);
  avisa al usuario que las configure (ver "Nota sobre credenciales") y trabaja con el seed incluido.

**Guarda el valor de `CACHE_PATH`**: es el documento vigente que leerás en M1 y del que copiarás
patrones. Si por algo no lo tienes, cae al seed incluido:
`${CLAUDE_PLUGIN_ROOT}/assets/design-guidelines.html`. Ese HTML **es a la vez la plantilla y la
referencia**: contiene el `<style>` y el `<script>` que dan vida al deck y 36 láminas de ejemplo que
demuestran cada patrón.

### M1 — Aprende el sistema

Lee `${CLAUDE_PLUGIN_ROOT}/references/design-system.md` (resumen de tokens y reglas editoriales).
Cuando necesites el **markup exacto** de un componente o diagrama (loop, átomo, matriz, tabla, Gantt,
cards, etc.), abre el HTML de `CACHE_PATH` (o el seed), busca su bloque `/* ===== NOMBRE ===== */` en
el `<style>` o la lámina que lo demuestra, y **copia el patrón real**. No reconstruyas de memoria algo
ya resuelto.

### M2 — Reglas que no se negocian

Valen tanto para crear como para revisar. Son las que más se rompen:

- **Magenta solo como texto/borde de acento, JAMÁS como relleno/fondo.**
- **Flechas dibujadas solo en el "mapa del motor"** (punta redondeada). En bullets y navegación, nunca.
- Si el contenido no cabe en el área útil (`.cbody`), va a **otra lámina**; no comprimas ni encojas.
- **Una sola tipografía** (Plus Jakarta Sans) y **una sola escala** `.fs-*`. Nada de tamaños ad-hoc.
- Los **diagramas estructurantes son el héroe** de su lámina: grandes y centrados, no miniaturas.
- Colores solo desde los tokens `--*`; no hardcodees hex nuevos.

---

## Elige el modo

- El usuario quiere **un deck nuevo** (o editar uno) → **Modo CREAR**.
- El usuario quiere **saber si un deck cumple la marca** / auditar / corregir → **Modo REVISAR**.

---

## Modo CREAR

1. **Entiende el encargo**: tema y mensaje central; contenido/datos (si no los dio, pídeselos o
   propón un esqueleto — no inventes cifras de negocio); cuántas láminas aprox.; frente(s) de Growth
   (adquisición/retención/monetización/social) para sus colores de función.
   - **El contenido puede venir de una fuente, no solo pegado a mano.** Si el usuario apunta a una
     **página de Notion**, una **transcripción de reunión** (p. ej. Granola) o una **planilla** de
     datos, léela tú (con las herramientas/MCP disponibles) y extrae de ahí el material — no le pidas
     que lo copie. Si no hay una fuente y faltan datos, pídeselos; nunca inventes cifras de negocio.

2. **Índice-primero**: si la preferencia `indice_primero` está en `sí`, o el usuario lo pide,
   **primero propón la estructura del deck** (lista de láminas con su propósito) y **espera su OK**
   antes de construir. Si el usuario **no tiene archivo de preferencias** (no conoce el modo) y el
   deck es no trivial, **ofréceselo aquí una vez** antes de arrancar ("¿te propongo la estructura
   primero y la apruebas antes de construir?"). Si está **desactivado** por preferencia, construye
   directo sin ofrecer.

3. **Construye reutilizando el shell oficial** (no reinventes el motor):
   - Copia verbatim, desde el HTML de `CACHE_PATH` (o el seed), el `<head>` completo (fuente +
     `<style>` con todos los tokens y componentes) y el `<script>` del final (escalado del stage
     1280×720, count-up, drawboxes, navegación).
   - Dentro de `#stage`, reemplaza las láminas de ejemplo por las de tu contenido, cada una como
     `<section class="slide">…</section>` (la primera con `.active`), usando componentes documentados.
   - Respeta la anatomía `.chead` → `.cbody` (área útil) → `.cfoot`; envuelve lo animable en `.stagger`.
   - Aplica las **reglas M2** mientras construyes.
   - Para acelerar y no reescribir el `<style>` a mano, puedes ensamblar con un script que lea el
     cache y te inyecte las láminas (ver `${CLAUDE_PLUGIN_ROOT}/scripts/assemble_deck.py`; pásale
     `--cache "$CACHE_PATH"` para usar la versión vigente en vez del seed).

4. **Entrega y verifica**:
   - **Dónde guardar**: por defecto, la **carpeta actual de trabajo** (portable y predecible; no
     asumas Escritorio ni una ruta fija). Si el usuario definió `output_dir` en sus preferencias,
     úsala. Nombre descriptivo: `Growth-<Tema>-<fecha>.html`. Debe abrir sin conexión (salvo la
     fuente de Google Fonts).
   - **Verifica antes de entregar** (en este orden):
     1. **Linter, siempre**: corre `brand_check.py` sobre tu propio output. Es Python puro, funciona
        en cualquier máquina — es la verificación base que no depende de nada.
     2. **Vistazo visual, si se puede**: si hay un MCP de navegador disponible (p. ej. chrome-devtools),
        renderiza y toma screenshot de 2–3 láminas clave (portada, un diagrama héroe, una con datos)
        para confirmar composición y que nada se desborde. Si **no** hay ningún MCP de navegador, no
        es un problema: **sáltalo** y apóyate en el linter + la revisión humana. Nunca lo conviertas
        en un requisito.
   - **No abras el archivo por tu cuenta**: solo **ofrece** abrirlo y **espera el OK** del usuario.
     Cuando lo abras, usa el comando del sistema operativo correcto: `open` (macOS), `xdg-open`
     (Linux) o `start` (Windows).
   - Si piden `.pptx` editable, es un paso secundario; el formato nativo y fiel es el HTML.

---

## Modo REVISAR (revisor de marca)

Audita un deck (o cualquier HTML) contra las guidelines y reporta lo que rompe la marca.

1. **Pasada mecánica** con el linter (rápido y objetivo):
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brand_check.py" <ruta-del-deck.html>
   ```
   Detecta lo automatizable: magenta como relleno, flechas fuera del motor, tamaños de fuente fuera
   de la escala `.fs-*`, `font-family` ad-hoc, y colores hex fuera de la paleta de tokens. Imprime
   cada hallazgo con su línea y un `SUMMARY` final.

2. **Pasada de criterio** (lo que el script no puede juzgar): revisa contra `references/design-system.md`
   y las reglas M2 cosas de composición — diagramas usados como miniatura en vez de héroe, contenido
   que desborda el área útil, jerarquía tipográfica, uso correcto de cards/chips/tablas, navegación
   con flechas decorativas, coherencia de los colores de función.

3. **Reporta** ordenado por severidad: primero lo que **viola** una regla no negociable (con línea y
   corrección concreta), luego **mejoras** recomendadas. Si el usuario lo pide, aplica las correcciones
   y vuelve a correr el linter para confirmar que quedó limpio.

---

## Modos opcionales de flujo (personales)

Actívalos vía el archivo de preferencias o a pedido en el chat. No son obligatorios para el equipo:

- **`indice_primero`** — proponer estructura y esperar OK antes de construir (ver Modo CREAR, paso 2).
- **`audiencia_default`** / **`largo_default`** — sesgar densidad y tono: `ejecutivo` (corto, cifras y
  conclusiones) vs `equipo` (más detalle y método). Sin valor, decide según el contenido.
- **`output_dir`** — carpeta donde guardar los decks. Sin valor, usa la carpeta actual de trabajo.

---

## Nota sobre credenciales

Por seguridad, el plugin **no incluye la contraseña** (este repo se comparte). Cada usuario necesita
las credenciales del sitio de guidelines, vía variables de entorno:
`GROWTH_GUIDELINES_USER` y `GROWTH_GUIDELINES_PASS`. Dos formas:

- **Recomendada (equipo):** un admin las pone en el bloque `env` de la configuración administrada,
  y le llegan a todos sin que cada quien haga nada.
- **Individual:** cada persona las exporta una vez en su shell (`~/.zshrc` / `~/.bashrc`).

Si faltan, el script devuelve `STATUS=NOCREDS` y se trabaja con el seed incluido (puede estar
desactualizado). Si el equipo cambia la contraseña, se actualiza en ese mismo lugar.
