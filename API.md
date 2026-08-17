# Contrato de la API — Generador de Horarios Escolares

API REST (FastAPI + PostgreSQL) para armar las grillas de horarios de los
grados de una escuela, asignando docentes curriculares mediante un solver
CSP por backtracking.

Este documento describe **todos** los endpoints disponibles para que el
frontend los consuma sin necesidad de leer el código del backend.

## Cómo levantar el servidor

```bash
# 1. Activar el entorno virtual (ya incluido en el repo)
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

# 2. Variables de entorno (copiar .env.example a .env y completar)
#    DATABASE_URL=postgresql+psycopg://usuario:password@localhost:5432/horarios

# 3. Migraciones
alembic upgrade head

# 4. Levantar el servidor
uvicorn app.main:app --reload
```

El servidor corre por defecto en `http://127.0.0.1:8000`.

**Documentación interactiva (Swagger UI):** `http://127.0.0.1:8000/docs`
(autogenerada por FastAPI a partir de los mismos schemas que se describen
acá — sirve para probar los endpoints a mano).

## Notas generales

- Todos los bodies y respuestas son JSON.
- Los endpoints de creación que reciben una **lista** (`crear_bloques`,
  `crear_grados`, `crear_materias`, `crear_docentes`,
  `asignar_materias_a_grados`, `cargar_disponibilidad`) esperan un array
  JSON en el body, aunque sea de un solo elemento, y devuelven un array con
  los objetos creados (incluyendo su `id`).
- `dia_semana` y `dia_cobertura` son enteros **1 = lunes ... 5 = viernes**.
- Si el body no cumple los tipos/campos requeridos por el schema, FastAPI
  devuelve automáticamente **422 Unprocessable Entity** con el detalle de
  validación (no se documenta caso por caso, es el comportamiento estándar
  de FastAPI/Pydantic en todos los endpoints).
- Los recursos anidados bajo `/escuelas/{escuela_id}/...` devuelven
  **404** con `{"detail": "La escuela no existe"}` si `escuela_id` no
  corresponde a ninguna escuela cargada.

---

## Salud

### `GET /salud`

Chequeo simple de que el servidor está levantado.

**Respuesta 200:**
```json
{ "estado": "ok" }
```

---

## Escuelas

### `POST /escuelas/`

Crea una escuela.

**Body** (`EscuelaCrear`):
```json
{
  "nombre": "Escuela Ejemplo",
  "tipo": "simple",
  "turno": "manana"
}
```
| Campo | Tipo | Requerido |
|---|---|---|
| nombre | string | sí |
| tipo | string | sí |
| turno | string | sí |

**Respuesta 201/200** (`EscuelaLeer`):
```json
{
  "id": 1,
  "nombre": "Escuela Ejemplo",
  "tipo": "simple",
  "turno": "manana"
}
```

### `GET /escuelas/`

Lista todas las escuelas.

**Respuesta 200:** `EscuelaLeer[]`
```json
[
  { "id": 1, "nombre": "Escuela Ejemplo", "tipo": "simple", "turno": "manana" }
]
```

---

## Bloques horarios

Un bloque es una franja de tiempo del día (un módulo de clase o un recreo).

### `POST /escuelas/{escuela_id}/bloques/`

Crea uno o más bloques horarios para una escuela.

**Body** (`BloqueCrear[]`):
```json
[
  { "orden": 1, "hora_inicio": "08:00", "hora_fin": "08:45", "tipo_bloque": "modulo" },
  { "orden": 3, "hora_inicio": "09:30", "hora_fin": "09:45", "tipo_bloque": "recreo" }
]
```
| Campo | Tipo | Requerido |
|---|---|---|
| orden | int | sí |
| hora_inicio | string `"HH:MM"` (time) | sí |
| hora_fin | string `"HH:MM"` (time) | sí |
| tipo_bloque | string (ej. `"modulo"`, `"recreo"`) | sí |

**Respuesta 200** (`BloqueLeer[]`):
```json
[
  {
    "id": 10,
    "escuela_id": 1,
    "orden": 1,
    "hora_inicio": "08:00:00",
    "hora_fin": "08:45:00",
    "tipo_bloque": "modulo"
  }
]
```

**Errores:** `404` si la escuela no existe.

### `GET /escuelas/{escuela_id}/bloques/`

Lista los bloques de la escuela, ordenados por `orden` ascendente.

**Respuesta 200:** `BloqueLeer[]` (mismo formato que arriba).

**Errores:** `404` si la escuela no existe.

---

## Grados

### `POST /escuelas/{escuela_id}/grados/`

Crea uno o más grados para una escuela.

**Body** (`GradoCrear[]`):
```json
[
  { "nombre": "1ro A", "maestra": "Silvia", "dia_cobertura": 3 }
]
```
| Campo | Tipo | Requerido |
|---|---|---|
| nombre | string | sí |
| maestra | string \| null | no |
| dia_cobertura | int (1=lunes...5=viernes) \| null | no |

`dia_cobertura` es el día en que la maestra del grado necesita cubrir la
salida: el solver intenta (como preferencia, no como restricción dura)
ubicar un módulo curricular en el último bloque de ese día para ese grado.

**Respuesta 200** (`GradoLeer[]`):
```json
[
  {
    "id": 5,
    "escuela_id": 1,
    "nombre": "1ro A",
    "maestra": "Silvia",
    "dia_cobertura": 3
  }
]
```

**Errores:** `404` si la escuela no existe.

### `GET /escuelas/{escuela_id}/grados/`

Lista los grados de la escuela.

**Respuesta 200:** `GradoLeer[]` (mismo formato que arriba).

**Errores:** `404` si la escuela no existe.

---

## Materias

### `POST /escuelas/{escuela_id}/materias/`

Crea una o más materias curriculares para una escuela (ej. Música, Inglés).

**Body** (`MateriaCrear[]`):
```json
[{ "nombre": "Musica" }, { "nombre": "Ingles" }]
```
| Campo | Tipo | Requerido |
|---|---|---|
| nombre | string | sí |

**Respuesta 200** (`MateriaLeer[]`):
```json
[
  { "id": 2, "escuela_id": 1, "nombre": "Musica" }
]
```

**Errores:** `404` si la escuela no existe.

### `GET /escuelas/{escuela_id}/materias/`

Lista las materias de la escuela.

**Respuesta 200:** `MateriaLeer[]` (mismo formato que arriba).

**Errores:** `404` si la escuela no existe.

### `POST /escuelas/{escuela_id}/materias/asignaciones`

Asigna materias a grados, indicando cuántos módulos semanales corresponden
(esto es lo que el solver usa como demanda a cubrir).

**Body** (`MateriaGradoCrear[]`):
```json
[
  { "grado_id": 5, "materia_id": 2, "modulos_semanales": 2 }
]
```
| Campo | Tipo | Requerido |
|---|---|---|
| grado_id | int | sí |
| materia_id | int | sí |
| modulos_semanales | int | sí |

**Respuesta 200** (`MateriaGradoLeer[]`):
```json
[
  { "id": 8, "grado_id": 5, "materia_id": 2, "modulos_semanales": 2 }
]
```

**Errores:** `404` si la escuela no existe. (No valida que `grado_id`/`materia_id`
pertenezcan a la escuela ni que existan — atención al integrar el frontend.)

### `GET /escuelas/{escuela_id}/materias/asignaciones`

Lista las asignaciones materia-grado de la escuela (join contra `materias`
por `escuela_id`).

**Respuesta 200:** `MateriaGradoLeer[]` (mismo formato que arriba).

**Errores:** `404` si la escuela no existe.

---

## Docentes

### `POST /escuelas/{escuela_id}/docentes/`

Crea uno o más docentes. Cada docente dicta una única materia curricular.

**Body** (`DocenteCrear[]`):
```json
[
  { "nombre": "Profe Musica", "materia_id": 2, "cargo_modulos": 20 }
]
```
| Campo | Tipo | Requerido |
|---|---|---|
| nombre | string | sí |
| materia_id | int | sí |
| cargo_modulos | int (máximo de módulos semanales que puede dictar) | sí |

**Respuesta 200** (`DocenteLeer[]`):
```json
[
  {
    "id": 3,
    "escuela_id": 1,
    "materia_id": 2,
    "nombre": "Profe Musica",
    "cargo_modulos": 20
  }
]
```

**Errores:** `404` si la escuela no existe.

### `GET /escuelas/{escuela_id}/docentes/`

Lista los docentes de la escuela.

**Respuesta 200:** `DocenteLeer[]` (mismo formato que arriba).

**Errores:** `404` si la escuela no existe.

### `POST /escuelas/{escuela_id}/docentes/{docente_id}/disponibilidad`

Carga una o más franjas horarias en las que el docente está disponible
para dictar clases.

**Body** (`DisponibilidadCrear[]`):
```json
[
  { "dia_semana": 1, "bloque_id": 10 },
  { "dia_semana": 2, "bloque_id": 10 }
]
```
| Campo | Tipo | Requerido |
|---|---|---|
| dia_semana | int (1=lunes...5=viernes) | sí |
| bloque_id | int (id de un bloque tipo `modulo`) | sí |

**Respuesta 200** (`DisponibilidadLeer[]`):
```json
[
  { "id": 15, "docente_id": 3, "dia_semana": 1, "bloque_id": 10 }
]
```

**Errores:** `404` con `{"detail": "El docente no existe"}` si `docente_id`
no existe o no pertenece a `escuela_id`.

### `GET /escuelas/{escuela_id}/docentes/{docente_id}/disponibilidad`

Lista la disponibilidad cargada de un docente.

**Respuesta 200:** `DisponibilidadLeer[]` (mismo formato que arriba).

**Errores:** `404` con `{"detail": "El docente no existe"}` si `docente_id`
no existe o no pertenece a `escuela_id`.

---

## Asignaciones (horario generado)

Una `Asignacion` es una celda concreta de la grilla: un grado, en un día y
bloque, con una materia y un docente.

### `GET /escuelas/{escuela_id}/asignaciones/`

Lista las asignaciones ya generadas y guardadas para la escuela.

**Respuesta 200** (`AsignacionLeer[]`):
```json
[
  {
    "id": 100,
    "escuela_id": 1,
    "grado_id": 5,
    "dia_semana": 1,
    "bloque_id": 10,
    "materia_id": 2,
    "docente_id": 3
  }
]
```

**Errores:** `404` si la escuela no existe.

### `POST /escuelas/{escuela_id}/asignaciones/generar`

Corre el solver CSP (backtracking con MRV + forward checking) sobre los
datos cargados de la escuela (bloques, grados, materias asignadas,
docentes y su disponibilidad) y **persiste** el resultado, reemplazando
lo que hubiera. Devuelve la grilla completa generada.

Restricciones duras que respeta el solver:
- Un docente no puede estar en dos lugares a la vez.
- El docente debe estar disponible en ese día/bloque.
- Un grado no puede tener dos materias en el mismo día/bloque.
- Solo dictan docentes que efectivamente dan esa materia.
- Un docente no puede superar su `cargo_modulos`.

Si el grado tiene `dia_cobertura`, el solver intenta (preferencia de
búsqueda, no restricción dura) ubicar un módulo en el último bloque de
ese día.

**Body:** ninguno.

**Respuesta 200:** `AsignacionLeer[]` (mismo formato que el GET de arriba).

**Errores:**
- `404` si la escuela no existe.
- `400` si el solver no pudo encontrar una solución con los datos
  cargados, con el detalle:
  ```json
  { "detail": "No se pudo generar el horario con los datos cargados. Revisa la disponibilidad y los cargos de los docentes." }
  ```

---

## PDF

Descarga de la grilla de horario en formato PDF, ya generada (requiere
haber corrido antes `POST /escuelas/{escuela_id}/asignaciones/generar`).
La respuesta no es JSON: es el binario del PDF con
`Content-Type: application/pdf` y
`Content-Disposition: attachment; filename=<titulo>.pdf`.

### `GET /pdf/grado/{grado_id}`

Descarga la grilla semanal de un grado (filas = bloques, columnas = días,
con materia y docente en cada celda).

**Respuesta 200:** binario `application/pdf`.

**Errores:** `404` con `{"detail": "El grado no existe"}` si `grado_id` no existe.

### `GET /pdf/docente/{docente_id}`

Descarga la grilla semanal de un docente.

**Respuesta 200:** binario `application/pdf`.

**Errores:** `404` con `{"detail": "El docente no existe"}` si `docente_id` no existe.
