"""Lee de la base los datos que el solver necesita y los deja
en estructuras simples de Python, faciles de recorrer."""

from dataclasses import dataclass, field

from sqlalchemy.orm import Session

from app.models.bloque_horario import BloqueHorario
from app.models.docente import DisponibilidadDocente, Docente
from app.models.grado import Grado
from app.models.materia import MateriaGrado

DIAS_SEMANA = [1, 2, 3, 4, 5]  # lunes a viernes: constantes del sistema


@dataclass
class RequerimientoMateria:
    """Una materia que un grado necesita, con cuantos modulos."""
    grado_id: int
    materia_id: int
    modulos_semanales: int


@dataclass
class DatosSolver:
    """Todo lo que el solver necesita para resolver una escuela."""
    escuela_id: int
    # bloques de tipo modulo (los casilleros de tiempo disponibles)
    bloques_modulo: list[BloqueHorario] = field(default_factory=list)
    # que necesita cada grado
    requerimientos: list[RequerimientoMateria] = field(default_factory=list)
    # docentes por materia: materia_id -> lista de docentes que la dictan
    docentes_por_materia: dict[int, list[Docente]] = field(default_factory=dict)
    # disponibilidad: docente_id -> set de (dia, bloque_id) donde puede dar
    disponibilidad: dict[int, set[tuple[int, int]]] = field(default_factory=dict)


def preparar_datos(sesion: Session, escuela_id: int) -> DatosSolver:
    datos = DatosSolver(escuela_id=escuela_id)

    # 1. Bloques de tipo modulo (recreo y comedor quedan afuera)
    datos.bloques_modulo = (
        sesion.query(BloqueHorario)
        .filter(
            BloqueHorario.escuela_id == escuela_id,
            BloqueHorario.tipo_bloque == "modulo",
        )
        .order_by(BloqueHorario.orden)
        .all()
    )

    # 2. Requerimientos: que materia y cuantos modulos necesita cada grado
    grados = sesion.query(Grado).filter(Grado.escuela_id == escuela_id).all()
    ids_grados = [g.id for g in grados]
    asignaciones_materia = (
        sesion.query(MateriaGrado)
        .filter(MateriaGrado.grado_id.in_(ids_grados))
        .all()
    )
    for am in asignaciones_materia:
        datos.requerimientos.append(
            RequerimientoMateria(
                grado_id=am.grado_id,
                materia_id=am.materia_id,
                modulos_semanales=am.modulos_semanales,
            )
        )

    # 3. Docentes agrupados por materia
    docentes = sesion.query(Docente).filter(Docente.escuela_id == escuela_id).all()
    for docente in docentes:
        datos.docentes_por_materia.setdefault(docente.materia_id, []).append(docente)

    # 4. Disponibilidad de cada docente como set de (dia, bloque_id)
    ids_docentes = [d.id for d in docentes]
    franjas = (
        sesion.query(DisponibilidadDocente)
        .filter(DisponibilidadDocente.docente_id.in_(ids_docentes))
        .all()
    )
    for franja in franjas:
        datos.disponibilidad.setdefault(franja.docente_id, set()).add(
            (franja.dia_semana, franja.bloque_id)
        )

    return datos
