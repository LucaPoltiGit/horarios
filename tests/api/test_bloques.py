def test_crear_bloques(cliente, escuela_id):
    respuesta = cliente.post(
        f"/escuelas/{escuela_id}/bloques/",
        json=[
            {"orden": 1, "hora_inicio": "08:00", "hora_fin": "08:55", "tipo_bloque": "modulo"},
            {"orden": 2, "hora_inicio": "08:55", "hora_fin": "09:50", "tipo_bloque": "recreo"},
        ],
    )
    assert respuesta.status_code == 200
    bloques = respuesta.json()
    assert len(bloques) == 2
    assert bloques[0]["tipo_bloque"] == "modulo"


def test_crear_bloques_escuela_inexistente(cliente):
    respuesta = cliente.post(
        "/escuelas/999/bloques/",
        json=[
            {"orden": 1, "hora_inicio": "08:00", "hora_fin": "08:55", "tipo_bloque": "modulo"},
        ],
    )
    assert respuesta.status_code == 404


def test_listar_bloques_ordenados(cliente, escuela_id):
    cliente.post(
        f"/escuelas/{escuela_id}/bloques/",
        json=[
            {"orden": 2, "hora_inicio": "08:55", "hora_fin": "09:50", "tipo_bloque": "modulo"},
            {"orden": 1, "hora_inicio": "08:00", "hora_fin": "08:55", "tipo_bloque": "modulo"},
        ],
    )
    respuesta = cliente.get(f"/escuelas/{escuela_id}/bloques/")
    bloques = respuesta.json()
    assert bloques[0]["orden"] == 1
    assert bloques[1]["orden"] == 2
