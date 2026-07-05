"""Orquesta el proceso completo: preparar datos, resolver y guardar.
El endpoint solo llama a esta funcion."""

from sqlalchemy.orm import Session

from app.models.asignacion import Asignacion
from app.solver.backtracking import resolver
from app.solver.datos import preparar_datos


def generar_y_guardar(sesion: Session, escuela_id: int) -> list[Asignacion]:
    """Genera el horario de una escuela y reemplaza el anterior.
    Puede lanzar SolverError si no hay solucion posible."""

    # 1. Preparar datos y resolver (puede lanzar SolverError)
    datos = preparar_datos(sesion, escuela_id)
    resultado = resolver(datos)

    # 2. Borrar asignaciones anteriores de esta escuela (Opcion A: reemplazar)
    sesion.query(Asignacion).filter(
        Asignacion.escuela_id == escuela_id
    ).delete()

    # 3. Guardar las nuevas
    nuevas = []
    for r in resultado:
        asignacion = Asignacion(
            escuela_id=escuela_id,
            grado_id=r.grado_id,
            dia_semana=r.dia_semana,
            bloque_id=r.bloque_id,
            materia_id=r.materia_id,
            docente_id=r.docente_id,
        )
        sesion.add(asignacion)
        nuevas.append(asignacion)

    sesion.commit()
    for asignacion in nuevas:
        sesion.refresh(asignacion)

    return nuevas
