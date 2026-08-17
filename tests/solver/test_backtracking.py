import pytest

from app.models.bloque_horario import BloqueHorario
from app.models.docente import Docente
from app.solver.backtracking import SolverError, resolver
from app.solver.datos import DIAS_SEMANA, DatosSolver, RequerimientoMateria


def _bloque(id_, orden):
    return BloqueHorario(
        id=id_, escuela_id=1, orden=orden,
        hora_inicio=None, hora_fin=None, tipo_bloque="modulo",
    )


def _docente(id_, materia_id, cargo):
    return Docente(
        id=id_, escuela_id=1, materia_id=materia_id,
        nombre=f"Docente {id_}", cargo_modulos=cargo,
    )


def test_resuelve_caso_simple():
    """Un grado, una materia con 2 modulos, un docente disponible.
    Debe colocar exactamente 2 asignaciones."""
    b1, b2 = _bloque(1, 1), _bloque(2, 2)
    doc = _docente(10, materia_id=100, cargo=20)

    datos = DatosSolver(
        escuela_id=1,
        bloques_modulo=[b1, b2],
        requerimientos=[
            RequerimientoMateria(grado_id=1, materia_id=100, modulos_semanales=2),
        ],
        docentes_por_materia={100: [doc]},
        disponibilidad={10: {(1, 1), (1, 2), (2, 1), (2, 2)}},
    )

    resultado = resolver(datos)
    assert len(resultado) == 2
    # Todas son del grado 1, materia 100, docente 10
    for a in resultado:
        assert a.grado_id == 1
        assert a.materia_id == 100
        assert a.docente_id == 10


def test_no_repite_docente_en_mismo_dia_bloque():
    """Dos grados necesitan al mismo docente. No puede estar en los dos
    a la vez en el mismo (dia, bloque)."""
    b1 = _bloque(1, 1)
    doc = _docente(10, materia_id=100, cargo=20)

    datos = DatosSolver(
        escuela_id=1,
        bloques_modulo=[b1],
        requerimientos=[
            RequerimientoMateria(grado_id=1, materia_id=100, modulos_semanales=1),
            RequerimientoMateria(grado_id=2, materia_id=100, modulos_semanales=1),
        ],
        docentes_por_materia={100: [doc]},
        # Disponible lunes y martes en el bloque 1
        disponibilidad={10: {(1, 1), (2, 1)}},
    )

    resultado = resolver(datos)
    assert len(resultado) == 2
    # Los dos grados no pueden compartir el mismo (dia, bloque)
    casilleros = {(a.dia_semana, a.bloque_id) for a in resultado}
    assert len(casilleros) == 2  # deben ser dias distintos


def test_lanza_error_si_no_hay_solucion():
    """Un grado necesita 2 modulos pero el docente solo tiene
    disponibilidad para 1. Debe lanzar SolverError."""
    b1 = _bloque(1, 1)
    doc = _docente(10, materia_id=100, cargo=20)

    datos = DatosSolver(
        escuela_id=1,
        bloques_modulo=[b1],
        requerimientos=[
            RequerimientoMateria(grado_id=1, materia_id=100, modulos_semanales=2),
        ],
        docentes_por_materia={100: [doc]},
        # Solo un casillero disponible, pero necesita 2
        disponibilidad={10: {(1, 1)}},
    )

    with pytest.raises(SolverError):
        resolver(datos)


def test_cubre_dia_de_cobertura_si_hay_lugar():
    """El grado 1 tiene dia_cobertura=2 (martes). Hay un solo modulo semanal
    y el docente esta disponible toda la semana: el Enfoque A debe hacer que
    el solver lo ubique en (martes, ultimo bloque)."""
    b1, b2 = _bloque(1, 1), _bloque(2, 2)  # b2 es el de mayor orden (ultimo)
    doc = _docente(10, materia_id=100, cargo=20)

    datos = DatosSolver(
        escuela_id=1,
        bloques_modulo=[b1, b2],
        requerimientos=[
            RequerimientoMateria(grado_id=1, materia_id=100, modulos_semanales=1),
        ],
        docentes_por_materia={100: [doc]},
        disponibilidad={
            10: {(dia, bloque.id) for dia in DIAS_SEMANA for bloque in (b1, b2)}
        },
        dia_cobertura={1: 2},
    )

    resultado = resolver(datos)
    assert len(resultado) == 1
    assert resultado[0].dia_semana == 2
    assert resultado[0].bloque_id == b2.id


def test_resuelve_aunque_no_pueda_cubrir_dia_de_cobertura():
    """El grado 1 tiene dia_cobertura=1 (lunes), pero el docente no esta
    disponible ese dia. La cobertura es solo una preferencia de orden de
    busqueda, no una restriccion dura: el solver debe seguir encontrando
    una solucion valida en otro (dia, bloque)."""
    b1 = _bloque(1, 1)
    doc = _docente(10, materia_id=100, cargo=20)

    datos = DatosSolver(
        escuela_id=1,
        bloques_modulo=[b1],
        requerimientos=[
            RequerimientoMateria(grado_id=1, materia_id=100, modulos_semanales=1),
        ],
        docentes_por_materia={100: [doc]},
        # Disponible solo el martes, nunca el lunes (dia de cobertura pedido)
        disponibilidad={10: {(2, 1)}},
        dia_cobertura={1: 1},
    )

    resultado = resolver(datos)
    assert len(resultado) == 1
    assert resultado[0].dia_semana == 2


def test_respeta_cargo_docente():
    """El docente tiene cargo de 1 modulo pero se necesitan 2.
    Debe lanzar SolverError porque no puede superar su cargo."""
    b1, b2 = _bloque(1, 1), _bloque(2, 2)
    doc = _docente(10, materia_id=100, cargo=1)  # cargo de solo 1 modulo

    datos = DatosSolver(
        escuela_id=1,
        bloques_modulo=[b1, b2],
        requerimientos=[
            RequerimientoMateria(grado_id=1, materia_id=100, modulos_semanales=2),
        ],
        docentes_por_materia={100: [doc]},
        disponibilidad={10: {(1, 1), (1, 2)}},
    )

    with pytest.raises(SolverError):
        resolver(datos)
