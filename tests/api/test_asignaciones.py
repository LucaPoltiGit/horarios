def test_listar_asignaciones_vacio(cliente, escuela_id):
    respuesta = cliente.get(f"/escuelas/{escuela_id}/asignaciones/")
    assert respuesta.status_code == 200
    assert respuesta.json() == []


def test_listar_asignaciones_escuela_inexistente(cliente):
    respuesta = cliente.get("/escuelas/999/asignaciones/")
    assert respuesta.status_code == 404
