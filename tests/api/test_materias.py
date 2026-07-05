def test_crear_materias(cliente, escuela_id):
    respuesta = cliente.post(
        f"/escuelas/{escuela_id}/materias/",
        json=[{"nombre": "Musica"}, {"nombre": "Ingles"}],
    )
    assert respuesta.status_code == 200
    materias = respuesta.json()
    assert len(materias) == 2
    assert materias[0]["nombre"] == "Musica"


def test_crear_materias_escuela_inexistente(cliente):
    respuesta = cliente.post(
        "/escuelas/999/materias/",
        json=[{"nombre": "Musica"}],
    )
    assert respuesta.status_code == 404


def test_asignar_materia_a_grado(cliente, escuela_id, grado_id, materia_id):
    respuesta = cliente.post(
        f"/escuelas/{escuela_id}/materias/asignaciones",
        json=[
            {"grado_id": grado_id, "materia_id": materia_id, "modulos_semanales": 2},
        ],
    )
    assert respuesta.status_code == 200
    asignaciones = respuesta.json()
    assert len(asignaciones) == 1
    assert asignaciones[0]["modulos_semanales"] == 2


def test_listar_asignaciones(cliente, escuela_id, grado_id, materia_id):
    cliente.post(
        f"/escuelas/{escuela_id}/materias/asignaciones",
        json=[
            {"grado_id": grado_id, "materia_id": materia_id, "modulos_semanales": 3},
        ],
    )
    respuesta = cliente.get(f"/escuelas/{escuela_id}/materias/asignaciones")
    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 1
