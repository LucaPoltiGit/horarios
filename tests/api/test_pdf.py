def _escenario_con_horario(cliente):
    """Crea una escuela minima completa y genera su horario.
    Devuelve (escuela_id, grado_id, docente_id)."""
    escuela_id = cliente.post(
        "/escuelas/",
        json={"nombre": "Escuela PDF", "tipo": "simple", "turno": "manana"},
    ).json()["id"]

    bloques = cliente.post(
        f"/escuelas/{escuela_id}/bloques/",
        json=[
            {"orden": 1, "hora_inicio": "08:00", "hora_fin": "08:45", "tipo_bloque": "modulo"},
            {"orden": 2, "hora_inicio": "08:45", "hora_fin": "09:30", "tipo_bloque": "modulo"},
        ],
    ).json()
    ids_modulo = [b["id"] for b in bloques]

    grado_id = cliente.post(
        f"/escuelas/{escuela_id}/grados/",
        json=[{"nombre": "1ro A"}],
    ).json()[0]["id"]

    materia_id = cliente.post(
        f"/escuelas/{escuela_id}/materias/",
        json=[{"nombre": "Musica"}],
    ).json()[0]["id"]

    cliente.post(
        f"/escuelas/{escuela_id}/materias/asignaciones",
        json=[{"grado_id": grado_id, "materia_id": materia_id, "modulos_semanales": 2}],
    )

    docente_id = cliente.post(
        f"/escuelas/{escuela_id}/docentes/",
        json=[{"nombre": "Profe Musica", "materia_id": materia_id, "cargo_modulos": 20}],
    ).json()[0]["id"]

    cliente.post(
        f"/escuelas/{escuela_id}/docentes/{docente_id}/disponibilidad",
        json=[
            {"dia_semana": 1, "bloque_id": ids_modulo[0]},
            {"dia_semana": 1, "bloque_id": ids_modulo[1]},
        ],
    )

    cliente.post(f"/escuelas/{escuela_id}/asignaciones/generar")
    return escuela_id, grado_id, docente_id


def test_pdf_grado_ok(cliente):
    _, grado_id, _ = _escenario_con_horario(cliente)
    respuesta = cliente.get(f"/pdf/grado/{grado_id}")
    assert respuesta.status_code == 200
    assert respuesta.headers["content-type"] == "application/pdf"
    # Un PDF valido empieza con estos bytes
    assert respuesta.content[:4] == b"%PDF"


def test_pdf_grado_inexistente(cliente):
    respuesta = cliente.get("/pdf/grado/999")
    assert respuesta.status_code == 404


def test_pdf_docente_ok(cliente):
    _, _, docente_id = _escenario_con_horario(cliente)
    respuesta = cliente.get(f"/pdf/docente/{docente_id}")
    assert respuesta.status_code == 200
    assert respuesta.headers["content-type"] == "application/pdf"
    assert respuesta.content[:4] == b"%PDF"


def test_pdf_docente_inexistente(cliente):
    respuesta = cliente.get("/pdf/docente/999")
    assert respuesta.status_code == 404
