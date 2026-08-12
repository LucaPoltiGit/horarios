def test_crear_grados(cliente, escuela_id):
    respuesta = cliente.post(
        f"/escuelas/{escuela_id}/grados/",
        json=[
            {"nombre": "1ro A", "maestra": "Silvia Gomez"},
            {"nombre": "2do A"},
        ],
    )
    assert respuesta.status_code == 200
    grados = respuesta.json()
    assert len(grados) == 2
    assert grados[0]["nombre"] == "1ro A"
    assert grados[1]["maestra"] is None


def test_crear_grados_escuela_inexistente(cliente):
    respuesta = cliente.post(
        "/escuelas/999/grados/",
        json=[{"nombre": "1ro A"}],
    )
    assert respuesta.status_code == 404


def test_listar_grados(cliente, escuela_id):
    cliente.post(
        f"/escuelas/{escuela_id}/grados/",
        json=[{"nombre": "1ro A"}],
    )
    respuesta = cliente.get(f"/escuelas/{escuela_id}/grados/")
    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 1


def test_crear_grado_con_dia_cobertura(cliente, escuela_id):
    respuesta = cliente.post(
        f"/escuelas/{escuela_id}/grados/",
        json=[{"nombre": "1ro A", "dia_cobertura": 5}],
    )
    assert respuesta.status_code == 200
    grados = respuesta.json()
    assert grados[0]["dia_cobertura"] == 5


def test_crear_grado_sin_dia_cobertura(cliente, escuela_id):
    respuesta = cliente.post(
        f"/escuelas/{escuela_id}/grados/",
        json=[{"nombre": "1ro A"}],
    )
    assert respuesta.status_code == 200
    grados = respuesta.json()
    assert grados[0]["dia_cobertura"] is None
