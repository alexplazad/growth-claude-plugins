# Sistema de diseño — Growth · Hites (referencia destilada)

Este archivo resume las reglas del sistema. La **fuente de verdad completa** (CSS, JS y
todos los componentes con su markup real) es `assets/design-guidelines.html`. Cuando
necesites el markup exacto de un componente, ábrelo y copia la sección correspondiente:
está organizado en 36 láminas, cada una demostrando un patrón, con bloques
`/* ===== NOMBRE ===== */` en el `<style>` que puedes buscar por nombre.

## Principio rector

Diseño de **precisión**: científico, dato-céntrico, con sello matemático. Movimiento
audaz pero con propósito ("nunca circo"). Minimalismo: lo que explica va al anexo.
La navegación es el clic, **nunca una flecha decorativa**.

## Tokens (única fuente de verdad — no inventes valores)

**Stage**: todo el deck vive en un escenario fijo de **1280×720** que se escala al viewport
(`#stage` + función `fit()` en el `<script>`). No cambies estas dimensiones.

**Radios**: `--r-pill:999px` `--r-card:20px` `--r-box:16px` `--r-sm:12px` `--r-xs:4px`

**Paleta base**:
- Azules: `--blue:#0058BA` `--royal:#2559BE` `--navy:#15137E` `--deep:#002492`
- Naranjo (acento primario): `--orange:#FA8100` `--orange-hi:#FFA64D` `--orange-soft:#FFF1E2` `--orange-deep:#E85D00`
- Magenta (SOLO destacador de texto/borde, **jamás relleno**): `--magenta:#FA1EB3` `--magenta-soft:#FFE8F6`
- Rojo (identidad de Analytics): `--red:#EA2E3B` `--red-soft:#FFE9EA`
- Neutros: `--gray:#8490A0` `--white:#FFFFFF` `--ink:#22262E` `--muted:#5C6675` `--line:#DEE6F0` `--blue-soft:#EAF2FB` `--grid:#E6EEF8` `--backdrop:#0A1430`

**Tipografía**: una sola familia, **Plus Jakarta Sans** (400–800). Escala única por clases
`.fs-*`: `--fs-hero:124px` `--fs-sep:88px` `--fs-q:58px` `--fs-title:46px` `--fs-lead:24px`
`--fs-sub:20px` `--fs-body:17px` `--fs-small:14px` `--fs-note:13px`. No uses tamaños fuera de esta escala.

**Colores de función** (los 4 frentes de Growth): adquisición `.adq`, retención `.ret`,
monetización `.mon`, social/`.so`. Se usan en chips y acentos.

## Estructura de una lámina

- `.slide` — lienzo absoluto; una activa a la vez (`.active`). `.slide.dark` = texto blanco.
- Láminas de contenido: `.chead` (encabezado: `.pill` + `.dtitle`) → `.cbody` (**área útil**) → `.cfoot` (pie).
- **Regla de oro del área útil**: `.cbody` tiene `overflow:hidden` como red de seguridad. Si el
  contenido llena el área, va a **OTRA lámina** — no comprimas ni encojas para que quepa.
- Transiciones (portada, separatas, cierre): comparten un área útil con 84px a los lados,
  contenido centrado vertical, pie reservado. El título de portada **baja de escalón** según
  su largo (`--fs-sep-l`, `--fs-sep-xl`) para no desbordar ni verse grotesco.
- Ayudas de construcción (quitar antes de publicar): `class="safe-guide"` y `class="cover-guide"`
  dibujan el recuadro de zona segura.

## Inventario de componentes (busca su bloque en el HTML por nombre)

**Texto y datos**
- Destacador magenta: solo texto, jamás fondo.
- Cifra héroe: gran número con gradiente y glow. Puede usar `.cup` (count-up animado desde 0).
- Bullets: marcador **cuadrado** de precisión, nunca flechas.
- Firmas matemáticas / signatures: `Σ μ σ Δ % ρ`.

**Bloques**
- Cards de color (`.card-soft` y variantes vibrantes con gradiente y sombra), chips de función,
  pills, barras, numeración circular, tabla (header `deep`/`royal`, **nunca magenta**, zebra sutil).

**Diagramas héroe** (el corazón del impacto — grandes, centrados, nunca adornos diminutos):
- **Loop/ciclo**: circular; nodo con número centrado dentro y label radial afuera (`.loop-ring`).
- **Mapa del motor / engranajes**: funciones como bloques en circuito, flechas de flujo de
  **punta redondeada** (`marker #motorArrow`) — único lugar del deck con flechas dibujadas.
- **Journey**: línea de vida con hitos luminosos.
- **Árbol de decisión**: ramificación con nodos; salidas como cards.
- **Matriz 2×2**: cuadrantes con profundidad; el ganador con glow.
- **Átomo** (`.atom`): núcleo + órbitas elípticas + electrones que orbitan — héroe de método/ciencia/analítica.
- **Organigrama**: canon átomo (núcleo=líder anillo naranjo, órbita interior royal, reportes soft, vacantes borde magenta punteado).
- Gantt/roadmap, flujos lineales, OKR (objetivo + resultados clave), Do/Don't (panel doble).

**Capa de datos (sello matemático)**: retícula blueprint, sparkline, stat radial (% en anillo),
"cálculo a la vista" (operandos con × + = hasta el resultado — los operadores matemáticos SÍ se
permiten porque no son flechas direccionales).

**Marca**: la "h" en contorno + círculo naranjo de acento, solo en transiciones, sangra fuera del
borde, siempre SVG. Logos Hites en base64 (`.lgb` azul para fondos claros, `.lgw` blanco para oscuros)
— única excepción raster. Logo del equipo: `∫` monolínea sobre squircle.

**Navegación**: índice clickeable (`.toc` / `.tocitem` con `data-goto`), botón global `#toindex`,
anexos (`.aref` link, `.term` subrayado, `.aback` volver). Ningún elemento de navegación es una flecha.

## Animaciones (una sola batería, con propósito)

- Entrada escalonada: contenido en `.stagger`, los hijos entran en secuencia (máx ~.7s, hasta 10 hijos).
- Contorno que se dibuja (`.drawbox`): el borde se traza una vez al activar la lámina (no loop) y el
  interior entra escalonado. El JS dimensiona el rect al tamaño real del box.
- Count-up (`.cup`): el valor final vive en el HTML; el JS anima desde 0.
- Loop: el anillo se dibuja y una luz recorre los nodos.
- Todas respetan `prefers-reduced-motion`: si está activo, se muestran los estados finales sin animar.

## Reglas que más se rompen (revísalas siempre)

1. **Magenta jamás de relleno** — solo texto o borde de acento.
2. **Flechas**: solo las del mapa del motor (punta redondeada). En bullets y navegación, nunca.
3. **Área útil**: si no cabe, nueva lámina. No encoger.
4. **Una sola tipografía y una sola escala** `.fs-*`. Sin tamaños ad-hoc.
5. Diagramas estructurantes son el **héroe** de su lámina: grandes y centrados, no miniaturas.
