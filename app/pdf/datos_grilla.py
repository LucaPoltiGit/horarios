"""Prepara los datos de las grillas para el PDF: traduce ids a nombres
y organiza las asignaciones en una estructura de tabla (bloque x dia).
Incluye TODOS los bloques (modulos, recreos y comedores)."""

from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.models.asignacion import Asignacion
from app.models.bloque_horario import BloqueHorario
from app.models.docente import Docente
from app.models.grado import Grado
from app.models.materia import Materia

NOMBRES_DIAS = {1: "Lunes", 2: "Martes", 3: "Miercoles", 4: "Jueves", 5: "Viernes"}


@dataclass
class Grilla:
    """Datos listos para dibujar una grilla (de grado o de docente)."""
    titulo: str            # ej. "Horario - 1ro A"  o  "Horario - Profe Musica"
    nombre_escuela: str
    bloques: list[BloqueHorario]  # TODOS los bloques, ordenados
    celdas: dict[tuple[int, int], str]  # (bloque_id, dia) -> texto


def _bloques_escuela(sesion: Session, escuela_id: int) -> list[BloqueHorario]:
    return (
        sesion.query(BloqueHorario)
        .filter(BloqueHorario.escuela_id == escuela_id)
        .order_by(BloqueHorario.orden)
        .all()
    )


def preparar_grilla_grado(sesion: Session, grado_id: int) -> Grilla:
    grado = sesion.get(Grado, grado_id)
    if grado is None:
        raise ValueError("El grado no existe")

    escuela = grado.escuela
    bloques = _bloques_escuela(sesion, escuela.id)

    asignaciones = (
        sesion.query(Asignacion)
        .filter(Asignacion.grado_id == grado_id)
        .all()
    )

    nombres_materia: dict[int, str] = {}
    nombres_docente: dict[int, str] = {}

    celdas: dict[tuple[int, int], str] = {}
    for a in asignaciones:
        if a.materia_id not in nombres_materia:
            materia = sesion.get(Materia, a.materia_id)
            nombres_materia[a.materia_id] = materia.nombre if materia else "?"
        if a.docente_id not in nombres_docente:
            docente = sesion.get(Docente, a.docente_id)
            nombres_docente[a.docente_id] = docente.nombre if docente else "?"

        texto = f"{nombres_materia[a.materia_id]}\n{nombres_docente[a.docente_id]}"
        celdas[(a.bloque_id, a.dia_semana)] = texto

    return Grilla(
        titulo=f"Horario - {grado.nombre}",
        nombre_escuela=escuela.nombre,
        bloques=bloques,
        celdas=celdas,
    )


def preparar_grilla_docente(sesion: Session, docente_id: int) -> Grilla:
    docente = sesion.get(Docente, docente_id)
    if docente is None:
        raise ValueError("El docente no existe")

    escuela = docente.escuela
    bloques = _bloques_escuela(sesion, escuela.id)

    asignaciones = (
        sesion.query(Asignacion)
        .filter(Asignacion.docente_id == docente_id)
        .all()
    )

    nombres_grado: dict[int, str] = {}

    celdas: dict[tuple[int, int], str] = {}
    for a in asignaciones:
        if a.grado_id not in nombres_grado:
            grado = sesion.get(Grado, a.grado_id)
            nombres_grado[a.grado_id] = grado.nombre if grado else "?"
        # En la grilla del docente, la celda muestra el GRADO donde esta
        celdas[(a.bloque_id, a.dia_semana)] = nombres_grado[a.grado_id]

    return Grilla(
        titulo=f"Horario - {docente.nombre}",
        nombre_escuela=escuela.nombre,
        bloques=bloques,
        celdas=celdas,
    )
