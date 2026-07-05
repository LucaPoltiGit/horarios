def test_crear_docente(cliente, escuela_id, materia_id):
    respuesta = cliente.post(
        f"/escuelas/{escuela_id}/docentes/",
        json=[
            {"nombre": "Juan Musica", "materia_id": materia_id, "cargo_modulos": 12},
        ],
    )
    assert respuesta.status_code == 200
    docentes = respuesta.json()
    assert len(docentes) == 1
    assert docentes[0]["cargo_modulos"] == 12


def test_crear_docente_escuela_inexistente(cliente):
    respuesta = cliente.post(
        "/escuelas/999/docentes/",
        json=[{"nombre": "Juan", "materia_id": 1, "cargo_modulos": 12}],
    )
    assert respuesta.status_code == 404


def test_cargar_disponibilidad(cliente, escuela_id, materia_id):
    bloques = cliente.post(
        f"/escuelas/{escuela_id}/bloques/",
        json=[
            {"orden": 1, "hora_inicio": "08:00", "hora_fin": "08:55", "tipo_bloque": "modulo"},
        ],
    ).json()
    bloque_id = bloques[0]["id"]

    docentes = cliente.post(
        f"/escuelas/{escuela_id}/docentes/",
        json=[
            {"nombre": "Juan Musica", "materia_id": materia_id, "cargo_modulos": 12},
        ],
    ).json()
    docente_id = docentes[0]["id"]

    respuesta = cliente.post(
        f"/escuelas/{escuela_id}/docentes/{docente_id}/disponibilidad",
        json=[
            {"dia_semana": 2, "bloque_id": bloque_id},
            {"dia_semana": 4, "bloque_id": bloque_id},
        ],
    )
    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 2


def test_disponibilidad_docente_inexistente(cliente, escuela_id):
    respuesta = cliente.post(
        f"/escuelas/{escuela_id}/docentes/999/disponibilidad",
        json=[{"dia_semana": 1, "bloque_id": 1}],
    )
    assert respuesta.status_code == 404
