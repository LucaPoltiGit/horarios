"""Solver CSP por backtracking. Coloca los modulos curriculares de
cada grado en la grilla (dia x bloque) respetando las restricciones duras."""

from dataclasses import dataclass

from app.solver.datos import DIAS_SEMANA, DatosSolver


@dataclass
class Tarea:
    """Una unidad a colocar: un modulo de una materia para un grado."""
    grado_id: int
    materia_id: int


@dataclass
class AsignacionResultado:
    """Una colocacion concreta que decidio el solver."""
    grado_id: int
    materia_id: int
    docente_id: int
    dia_semana: int
    bloque_id: int


class SolverError(Exception):
    """Se lanza cuando no se puede resolver, con un mensaje claro."""


def _construir_tareas(datos: DatosSolver) -> list[Tarea]:
    """Descompone cada requerimiento en tareas individuales."""
    tareas = []
    for req in datos.requerimientos:
        for _ in range(req.modulos_semanales):
            tareas.append(Tarea(grado_id=req.grado_id, materia_id=req.materia_id))
    return tareas


def _ultimo_bloque_id(bloques_ids: list[int]) -> int | None:
    """El bloque-modulo de mayor orden (bloques_ids ya viene ordenado por
    orden ascendente, ver preparar_datos)."""
    return bloques_ids[-1] if bloques_ids else None


def _ordenar_casilleros(
    bloques_ids: list[int], preferido: tuple[int, int] | None
) -> list[tuple[int, int]]:
    """Lista de casilleros (dia, bloque) a probar para una tarea. Si hay un
    casillero preferido (cobertura de salida del grado), se prueba primero;
    el resto sigue en el orden habitual. Es solo un orden de busqueda, no
    una restriccion: si el preferido no sirve, se sigue con los demas."""
    casilleros = [(dia, bloque_id) for dia in DIAS_SEMANA for bloque_id in bloques_ids]
    if preferido is not None and preferido in casilleros:
        casilleros.remove(preferido)
        casilleros.insert(0, preferido)
    return casilleros


def resolver(datos: DatosSolver) -> list[AsignacionResultado]:
    tareas = _construir_tareas(datos)
    bloques_ids = [b.id for b in datos.bloques_modulo]
    ultimo_bloque_id = _ultimo_bloque_id(bloques_ids)

    # Estructuras de control que se van actualizando durante la busqueda:
    resultado: list[AsignacionResultado] = []
    ocupacion_grado: set[tuple[int, int, int]] = set()   # (grado, dia, bloque)
    ocupacion_docente: set[tuple[int, int, int]] = set()  # (docente, dia, bloque)
    carga_docente: dict[int, int] = {}                    # docente_id -> modulos usados

    def casillero_valido(tarea, docente, dia, bloque_id) -> bool:
        # R2: el docente debe estar disponible ese (dia, bloque)
        if (dia, bloque_id) not in datos.disponibilidad.get(docente.id, set()):
            return False
        # R4: el grado no puede tener otra materia en ese (dia, bloque)
        if (tarea.grado_id, dia, bloque_id) in ocupacion_grado:
            return False
        # R1: el docente no puede estar en otro lugar en ese (dia, bloque)
        if (docente.id, dia, bloque_id) in ocupacion_docente:
            return False
        # R5: el docente no puede superar su cargo
        if carga_docente.get(docente.id, 0) >= docente.cargo_modulos:
            return False
        return True

    def backtrack(indice: int) -> bool:
        # Caso base: coloque todas las tareas
        if indice == len(tareas):
            return True

        tarea = tareas[indice]
        # R3 (implicita): solo docentes que dictan esta materia
        docentes = datos.docentes_por_materia.get(tarea.materia_id, [])

        # Enfoque A (preferencia de orden, no restriccion dura): si el grado
        # tiene cobertura de salida, se intenta primero el ultimo bloque del
        # dia elegido, para que tienda naturalmente a quedar cubierto.
        dia_preferido = datos.dia_cobertura.get(tarea.grado_id)
        preferido = (
            (dia_preferido, ultimo_bloque_id)
            if dia_preferido is not None and ultimo_bloque_id is not None
            else None
        )
        casilleros = _ordenar_casilleros(bloques_ids, preferido)

        for docente in docentes:
            for dia, bloque_id in casilleros:
                if not casillero_valido(tarea, docente, dia, bloque_id):
                    continue

                # Coloco (aplico la decision)
                ocupacion_grado.add((tarea.grado_id, dia, bloque_id))
                ocupacion_docente.add((docente.id, dia, bloque_id))
                carga_docente[docente.id] = carga_docente.get(docente.id, 0) + 1
                resultado.append(
                    AsignacionResultado(
                        grado_id=tarea.grado_id,
                        materia_id=tarea.materia_id,
                        docente_id=docente.id,
                        dia_semana=dia,
                        bloque_id=bloque_id,
                    )
                )

                # Sigo con la siguiente tarea
                if backtrack(indice + 1):
                    return True

                # Si no funciono, deshago (backtrack)
                ocupacion_grado.discard((tarea.grado_id, dia, bloque_id))
                ocupacion_docente.discard((docente.id, dia, bloque_id))
                carga_docente[docente.id] -= 1
                resultado.pop()

        # Ningun casillero funciono para esta tarea
        return False

    if not backtrack(0):
        raise SolverError(
            "No se pudo generar el horario con los datos cargados. "
            "Revisa la disponibilidad y los cargos de los docentes."
        )

    return resultado
