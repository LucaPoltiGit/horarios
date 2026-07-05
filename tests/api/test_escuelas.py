def test_crear_escuela(cliente):
    respuesta = cliente.post(
        "/escuelas/",
        json={"nombre": "Escuela Test", "tipo": "jornada completa", "turno": "doble"},
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["nombre"] == "Escuela Test"
    assert "id" in datos


def test_listar_escuelas(cliente):
    cliente.post(
        "/escuelas/",
        json={"nombre": "Escuela A", "tipo": "simple", "turno": "manana"},
    )
    respuesta = cliente.get("/escuelas/")
    assert respuesta.status_code == 200
    lista = respuesta.json()
    assert len(lista) == 1
    assert lista[0]["nombre"] == "Escuela A"


def test_listar_escuelas_vacio(cliente):
    respuesta = cliente.get("/escuelas/")
    assert respuesta.status_code == 200
    assert respuesta.json() == []
