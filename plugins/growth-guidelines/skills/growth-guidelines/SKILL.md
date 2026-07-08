---
name: growth-guidelines
description: >-
  Crea y audita HTML on-brand del equipo de Growth de Hites usando su sistema de diseño (paleta,
  tipografía Plus Jakarta Sans, componentes, diagramas). Sirve para CUALQUIER HTML: presentaciones y
  decks, páginas web, formatos 16:9, landings, documentos. Descarga sola la ÚLTIMA versión vigente de
  las guidelines antes de trabajar, así que siempre produce material actualizado sin descargas
  manuales. Úsala siempre que el usuario pida armar una presentación, deck, láminas, slides, pitch,
  una página web, un HTML, algo "en la línea/estilo de Growth" o "según las guidelines", cuando quiera
  revisar/auditar si un HTML cumple la marca, o cuando mencione la paleta, tipografía o componentes del
  equipo — aunque no diga explícitamente "presentación".
---

# HTML on-brand · Growth Hites

Esta skill es un **creador (y auditor) de HTML on-brand** con el sistema de diseño de Growth (Hites).
Aunque la guía nació para presentaciones, el sistema (tokens, paleta, tipografía, componentes) sirve
para **cualquier HTML**: decks, páginas web, formatos 16:9, landings, documentos. La skill **crea**
ese HTML y también **revisa/audita** HTML existente contra la guía. El sistema oficial vive en un
documento en línea que se actualiza solo cada vez que el equipo lo cambia; la skill lo baja fresco
antes de trabajar, para que nunca uses una versión vieja.

La skill está pensada para **compartirse en equipo**: el *motor on-brand* (Pasos M0–M2) es común a
todos; los *modos de flujo* (índice-primero, presets) son **opcionales y personales**, para que cada
quien trabaje a su manera sin forzar a los demás.

## Principio: el usuario manda

La guía es el **default recomendado**, no una camisa de fuerza. Si el usuario pide algo que no es
on-brand (un color fuera de paleta, otra tipografía, romper una regla), **adviérteselo una vez**, breve
y sin dramatizar, explicando por qué. Pero si insiste o lo confirma, **aplícalo tal como lo pidió** —
su decisión gana. Nunca ignores ni "corrijas por tu cuenta" una instrucción explícita en nombre de la
marca. Las reglas M2 y el linter son **guía**, no un veto sobre el usuario.

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
según el contenido; guardar en la **carpeta actual de trabajo**; al terminar, **cierre sobrio**
(entrega en una línea y deja seguir la conversación; no ofrezcas abrir ni ajustes).

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
- `STATUS=NOCREDS` — primera vez / sin credenciales guardadas. Para que sea **cero fricción real**:
  1. **Resuelve la ruta concreta** del script: corre en tu entorno
     `echo "${CLAUDE_PLUGIN_ROOT}/scripts/setup_credentials.sh"` y toma esa ruta absoluta. (En tu
     entorno `${CLAUDE_PLUGIN_ROOT}` está definido; en la terminal del usuario **NO**, por eso debes
     resolverla tú antes de dársela.)
  2. Entrégale un comando **copy-paste con la ruta ya resuelta** (ej.:
     `bash "/Users/<user>/.claude/plugins/cache/.../scripts/setup_credentials.sh"`) y explícale en una
     línea: es de **una sola vez**, le preguntará usuario y contraseña **en su terminal**, se guarda en
     su equipo y **no se le vuelve a pedir**.
  3. **No le pidas la contraseña en el chat ni la escribas tú** — el setup la toma directo en su
     terminal para que nunca pase por aquí. Cuando confirme que lo corrió, re-corre M0.
  Nunca le pases el comando con `${CLAUDE_PLUGIN_ROOT}` sin resolver: en su terminal esa variable está
  vacía y el comando fallaría.

**Guarda el valor de `CACHE_PATH`**: es el documento vigente (descargado y cacheado) sobre el que
trabajan los scripts. **No lo abras entero** — son ~226 KB, y leerlo completo es justo lo que hace
lento el proceso. Para todo lo que necesites usa los helpers: `extract.py` (ver índice o sacar una
lámina/tokens puntuales) y `assemble_deck.py` (inyectar el shell). Este plugin **no incluye una copia
interna** del documento; si el estado es `NOCREDS`, u `OFFLINE` sin cache previo, pide al usuario las
credenciales antes de seguir. Ese HTML contiene el `<style>` y el `<script>` que dan vida al deck y 36
láminas de ejemplo que demuestran cada patrón.

### M1 — Aprende el sistema

Lee `${CLAUDE_PLUGIN_ROOT}/references/design-system.md` (resumen de tokens y reglas editoriales). Es tu
"entendimiento" ya destilado y **estático**: con esto basta para el 90% de los casos y no necesitas
re-leer la guía en cada uso (a menos que `STATUS=UPDATED`).

Cuando necesites el **markup exacto** de un componente o diagrama, **no leas el documento completo** —
sácalo puntualmente con `extract.py` (esto es lo que mantiene rápido el proceso):

```bash
# índice de las 36 láminas (etiqueta + componentes que usa), en ~36 líneas:
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/extract.py" --cache "$CACHE_PATH" --list
# el markup de una lámina concreta (≈1% del archivo), por índice o por palabra:
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/extract.py" --cache "$CACHE_PATH" --slide 10
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/extract.py" --cache "$CACHE_PATH" --find atom
# solo los tokens (:root), útil para HTML libre:
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/extract.py" --cache "$CACHE_PATH" --tokens
```

Copia el patrón real del snippet; no reconstruyas de memoria algo ya resuelto.

### M2 — Reglas de marca (default on-brand)

Así se ve on-brand; son las que más se rompen. Aplícalas **por defecto** al crear y revisar. Pero
recuerda el principio *el usuario manda*: si pide explícitamente lo contrario, adviértele una vez y
respeta su decisión.

- **Magenta como texto/borde de acento, no de relleno/fondo.**
- **Flechas dibujadas solo en el "mapa del motor"** (punta redondeada); en bullets y navegación, no.
- Si el contenido no cabe en el área útil (`.cbody`), va a **otra lámina**; no comprimas ni encojas.
- **Una sola tipografía** (Plus Jakarta Sans) y **una sola escala** `.fs-*`; evita tamaños ad-hoc.
- Los **diagramas estructurantes son el héroe** de su lámina: grandes y centrados, no miniaturas.
- Colores desde los tokens `--*`; evita hex nuevos.

---

## Elige el modo y el formato

- **CREAR** — el usuario quiere un HTML nuevo (o editar uno). Determina el **formato**:
  - **Deck** — presentación, láminas, slides, pitch, o el usuario lo pide → sistema de láminas 1280×720.
  - **HTML libre** — página web, 16:9, landing, documento, "un HTML de…" → formato abierto, sin stage.
  - Si el pedido es ambiguo sobre el formato, **pregúntale** cuál quiere.
- **REVISAR** — el usuario quiere saber si un HTML cumple la marca / auditar / corregir → **Modo REVISAR**.

---

## Modo CREAR

1. **Entiende el encargo**: formato (deck / HTML libre); tema y mensaje central; contenido/datos (si
   no los dio, pídeselos o propón un esqueleto — no inventes cifras de negocio); cuántas láminas o
   secciones aprox.; frente(s) de Growth (adquisición/retención/monetización/social) para sus colores
   de función.
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

3. **Construye** — según el formato elegido (3a deck / 3b HTML libre). En ambos, el shell/base lo
   inyecta un script: **nunca leas ni reescribas el `<style>`/`<script>` completos** (130+ KB; ese es
   el costo que evitamos).

**3a · Deck** — tú solo escribes las láminas; el script pega el motor del deck.
   - Escribe **solo** tus láminas de contenido en un archivo-fragmento, cada una como
     `<section class="slide">…</section>`. Para el patrón de cada componente, copia el snippet que te
     dio `extract.py` en M1.
   - Respeta la anatomía `.chead` → `.cbody` (área útil) → `.cfoot`; envuelve lo animable en `.stagger`;
     aplica las **reglas M2**.
   - Ensambla el deck final con el script, que pega el shell oficial (fuente + `<style>` con todos los
     tokens/componentes + `<script>` del stage 1280×720/count-up/drawboxes/navegación) y marca activa
     la primera lámina:
     ```bash
     python3 "${CLAUDE_PLUGIN_ROOT}/scripts/assemble_deck.py" \
       --slides <tus-laminas.html> --cache "$CACHE_PATH" --out "<deck>.html"
     ```

**3b · HTML libre** (web, 16:9, landing, documento, cualquier formato) — mismo sistema de diseño, sin
el stage/navegación de deck. Tú tienes libertad total de layout; solo mantén la marca (M2).
   - Consulta los tokens con `extract.py --tokens` (colores, radios, escala tipográfica) y úsalos como
     variables `var(--*)`. Para inspiración de un componente puntual, `extract.py --find <algo>`.
   - Escribe **solo el contenido del `<body>`** en un archivo, con tu layout (usa `var(--deep)`,
     `var(--orange)`, `var(--r-card)`, clases `.fs-*`, etc.). Para 16:9 usa un contenedor
     `aspect-ratio:16/9`; para web, secciones normales.
   - Ensambla con el script, que pega la base on-brand (fuente Plus Jakarta Sans + tokens vivos + escala):
     ```bash
     python3 "${CLAUDE_PLUGIN_ROOT}/scripts/assemble_page.py" \
       --body <tu-cuerpo.html> --cache "$CACHE_PATH" --out "<pagina>.html" --title "…"
     ```

4. **Entrega y verifica**:
   - **Dónde guardar**: por defecto, la **carpeta actual de trabajo** (portable y predecible; no
     asumas Escritorio ni una ruta fija). Si el usuario definió `output_dir` en sus preferencias,
     úsala. Nombre descriptivo: `Growth-<Tema>-<fecha>.html`. Debe abrir sin conexión (salvo la
     fuente de Google Fonts).
   - **Verifica antes de entregar** (verificación **interna**: no la narres al usuario salvo que
     encuentres un problema real que valga la pena avisar):
     1. **Linter, siempre**: corre `brand_check.py` sobre tu propio output. Es Python puro, funciona
        en cualquier máquina — es la verificación base que no depende de nada.
     2. **Vistazo visual, si se puede**: si hay un MCP de navegador disponible (p. ej. chrome-devtools),
        renderiza y toma screenshot de 2–3 vistas clave (en deck: portada + un diagrama + una con datos;
        en HTML libre: las secciones principales) para confirmar composición y que nada se desborde. Si
        **no** hay ningún MCP de navegador, no es un problema: **sáltalo** y apóyate en el linter + la
        revisión humana. Nunca lo conviertas en un requisito.
   - **Cierre sobrio — la skill es una herramienta, no el centro de la conversación.** Termina con
     **una sola línea** diciendo qué generaste y dónde (p. ej. `Generé Growth-Q3.html en esta
     carpeta.`) y **detente ahí**. El HTML es el *producto*: la skill hizo su trabajo y se aparta;
     deja que el usuario siga su conversación por donde quiera.
     - **No** ofrezcas abrirlo, **no** propongas ajustes, **no** des un menú de opciones, **no** hagas
       preguntas de seguimiento, **no** conviertas el archivo en el tema de la conversación.
     - Solo **si el usuario lo pide**: ábrelo (`open` macOS · `xdg-open` Linux · `start` Windows),
       hazle ajustes o expórtalo a otro formato. Nunca lo abras por tu cuenta.

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

3. **Reporta** ordenado por severidad: primero lo que **rompe** una regla de marca (con línea y
   corrección concreta), luego **mejoras** recomendadas. Recuerda *el usuario manda*: reportas y
   sugieres, no impones — si una desviación fue una decisión deliberada del usuario, márcala como
   intencional y respétala. Si te pide aplicar correcciones, hazlas y vuelve a correr el linter.

---

## Modos opcionales de flujo (personales)

Actívalos vía el archivo de preferencias o a pedido en el chat. No son obligatorios para el equipo:

- **`indice_primero`** — proponer estructura y esperar OK antes de construir (ver Modo CREAR, paso 2).
- **`audiencia_default`** / **`largo_default`** — sesgar densidad y tono: `ejecutivo` (corto, cifras y
  conclusiones) vs `equipo` (más detalle y método). Sin valor, decide según el contenido.
- **`output_dir`** — carpeta donde guardar los decks. Sin valor, usa la carpeta actual de trabajo.

---

## Nota sobre credenciales

Por seguridad, el plugin **no incluye la contraseña** (este repo es público). Cada usuario la
configura **una sola vez**; después la skill la usa sola y no vuelve a pedirla. En orden de comodidad:

- **Setup de una vez (recomendado):** ante `NOCREDS`, la skill guía a correr en la terminal
  `bash "${CLAUDE_PLUGIN_ROOT}/scripts/setup_credentials.sh"`, que pide usuario y contraseña **en la
  propia terminal** (nunca en el chat) y las guarda en el equipo con permisos 600. No tocan el repo
  ni pasan por la IA.
- **Equipo, cero toque:** un admin puede poner `GROWTH_GUIDELINES_USER/PASS` en el bloque `env` de la
  configuración administrada y le llegan a todos automáticamente.
- **Manual:** exportarlas en `~/.zshrc` / `~/.bashrc`.

La skill resuelve credenciales en ese orden: variables de entorno → archivo guardado por el setup. Si
no hay ninguna, reporta `STATUS=NOCREDS`. Si el equipo cambia la contraseña, se vuelve a correr el
setup.
