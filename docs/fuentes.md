# Fuentes de datos

## Boletín diario de la Bolsa de Comercio de Rosario (BCR)

- **Página de descarga:** https://www.bcr.com.ar/es/mercados/boletin-diario/mercado-de-granos
- **Formato:** PDF, un boletín por día hábil.
- **Por qué PDF:** la API oficial de la BCR (GIX) solo da acceso a empresas. El boletín es la única fuente pública y oficial de los precios pizarra.

### Qué extraemos

El cuadro **"Precios de Cámaras Arbitrales del país"** de la página 1: una fila por grano y una columna por cámara. Usamos la columna de **Rosario**.

### Formatos encontrados

| | Formato A | Formato B | Formato C |
|---|---|---|---|
| Ejemplo revisado | 01/12/2008 (N.º 14.924) | 14/11/2014 (N.º 16.372) | 17/11/2026 (N.º 19.189) |
| Título del boletín | Mercado de Granos | Mercado de Productos | Mercado de Granos |
| Fecha de los precios | "Precios fijados el día" (mismo día) + "Precios orientativos del día" (día hábil anterior) | "Precios pizarra del día" = día hábil anterior | "Precios pizarra del día" = día hábil anterior |
| Columna de Rosario | "Cámara Rosario" (una sola columna) | "CAC Rosario", dividida en Pizarra / Estimativos | "CAC Rosario", dividida en Pizarra $ / Estimativo |
| Orden de columnas | Bahía Blanca antes que Quequén | Quequén antes que Bahía Blanca | Quequén antes que Bahía Blanca |
| Nombres de granos | Trigo Duro, Maíz Duro, Girasol, Soja, Sorgo | Trigo Duro, Maíz Duro, Girasol, Soja, Sorgo | Trigo pan, Trigo art. 12, Maíz duro, Girasol, Soja, Sorgo, Cebada |
| Formato de números | `400,00` (coma decimal, sin miles) | `1.110,0` (punto de miles, coma decimal) | `545.000` (punto de miles, sin decimales) |
| Marcas especiales | `*` y `**` con nota al pie ("** Protestado. Se ratifica el mismo precio.") | — | — |
| Monedas | $/Tn | $/Tn | $/Tn, salvo Bahía Blanca que puede venir en U$S |

### Reglas para el parser

1. **La fecha del dato sale del contenido del PDF**, no del nombre del archivo ni de la fecha del boletín.
2. **Las columnas se buscan por nombre**, no por posición: el orden cambia entre formatos.
3. **Normalizar nombres de granos:** "Trigo Duro" y "Trigo pan" → trigo; "Maíz Duro" y "Maíz duro" → maíz.
4. **Normalizar números:** quitar el punto de miles y convertir la coma decimal en punto.
5. **Guardar el tipo de precio:** pizarra, estimativo o protestado.
6. **Guardar la moneda de cada valor:** puede aparecer "U$S" dentro de una tabla en $/Tn.
7. **Una celda vacía no es cero:** significa que ese día no hubo precio para ese grano en esa cámara.

### Alcance

- **v1:** solo el Formato C (los últimos 1 a 2 años).
- **v2:** formatos A y B, para la historia completa desde 2008.

### Otras tablas útiles del boletín (para la v2)

- **"Precios del Mercado Físico de Granos de Rosario"** (en 2008: "Mercado de Disponible de Rosario"): ofertas concretas por comprador, lugar y fecha de entrega, en pesos o en dólares. Sirve para el simulador de vender o retener.
- **Futuros (A3 / ROFEX):** precios de posiciones futuras por grano. Sirve para calcular la base.
- **Cotización U$S BCRA C.3500** (en el boletín de 2008, página 2): permite validar el tipo de cambio contra la API del BCRA.

### Controles de calidad posibles

- En el Formato C, el precio pizarra de soja coincidió con la fila "Fca/Ros C/Desc." del mercado físico (545.000). No es una regla: en 2014 no coincidieron (2.505 vs. 2.350), porque el físico es del día del boletín y la pizarra del día anterior.

### Dudas abiertas

- [ ] ¿En qué año exacto se pasa del Formato A al B (entre 2008 y 2014)?
- [ ] ¿En qué año exacto se pasa del Formato B al C (entre 2014 y 2023)? Coincide con el cambio de URL (`AAMMDDbg.pdf` → `boletin-mercado-granos-N.pdf`).
- [ ] En el Formato A, ¿qué diferencia hay entre "precios fijados" y "precios orientativos"?
- [ ] ¿Qué significa "Trigo art. 12"? (en el Formato A aparece con la nota "Condición de pago diferido de los molinos")
