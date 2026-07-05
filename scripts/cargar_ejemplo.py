"""Carga una escuela de ejemplo completa para probar el solver.
Requiere que el servidor este corriendo (uvicorn app.main:app --reload)."""

import httpx

BASE = "http://127.0.0.1:8000"


def main():
    cliente = httpx.Client(base_url=BASE, timeout=10)

    # 1. Escuela
    escuela = cliente.post(
        "/escuelas/",
        json={"nombre": "Escuela Ejemplo", "tipo": "simple", "turno": "manana"},
    ).json()
    escuela_id = escuela["id"]
    print(f"Escuela creada: id={escuela_id}")

    # 2. Bloques (4 modulos + 1 recreo)
    bloques = cliente.post(
        f"/escuelas/{escuela_id}/bloques/",
        json=[
            {"orden": 1, "hora_inicio": "08:00", "hora_fin": "08:45", "tipo_bloque": "modulo"},
            {"orden": 2, "hora_inicio": "08:45", "hora_fin": "09:30", "tipo_bloque": "modulo"},
            {"orden": 3, "hora_inicio": "09:30", "hora_fin": "09:45", "tipo_bloque": "recreo"},
            {"orden": 4, "hora_inicio": "09:45", "hora_fin": "10:30", "tipo_bloque": "modulo"},
            {"orden": 5, "hora_inicio": "10:30", "hora_fin": "11:15", "tipo_bloque": "modulo"},
        ],
    ).json()
    ids_modulo = [b["id"] for b in bloques if b["tipo_bloque"] == "modulo"]
    print(f"Bloques creados. Modulos: {ids_modulo}")

    # 3. Grados
    grados = cliente.post(
        f"/escuelas/{escuela_id}/grados/",
        json=[
            {"nombre": "1ro A", "maestra": "Silvia"},
            {"nombre": "2do A", "maestra": "Laura"},
        ],
    ).json()
    id_1ro = grados[0]["id"]
    id_2do = grados[1]["id"]
    print(f"Grados: 1ro A={id_1ro}, 2do A={id_2do}")

    # 4. Materias
    materias = cliente.post(
        f"/escuelas/{escuela_id}/materias/",
        json=[{"nombre": "Musica"}, {"nombre": "Ingles"}],
    ).json()
    id_musica = materias[0]["id"]
    id_ingles = materias[1]["id"]
    print(f"Materias: Musica={id_musica}, Ingles={id_ingles}")

    # 5. Modulos por grado: cada grado tiene Musica 2 e Ingles 2
    cliente.post(
        f"/escuelas/{escuela_id}/materias/asignaciones",
        json=[
            {"grado_id": id_1ro, "materia_id": id_musica, "modulos_semanales": 2},
            {"grado_id": id_1ro, "materia_id": id_ingles, "modulos_semanales": 2},
            {"grado_id": id_2do, "materia_id": id_musica, "modulos_semanales": 2},
            {"grado_id": id_2do, "materia_id": id_ingles, "modulos_semanales": 2},
        ],
    )
    print("Asignaciones materia-grado creadas.")

    # 6. Docentes
    docentes = cliente.post(
        f"/escuelas/{escuela_id}/docentes/",
        json=[
            {"nombre": "Profe Musica", "materia_id": id_musica, "cargo_modulos": 20},
            {"nombre": "Profe Ingles", "materia_id": id_ingles, "cargo_modulos": 20},
        ],
    ).json()
    id_doc_musica = docentes[0]["id"]
    id_doc_ingles = docentes[1]["id"]
    print(f"Docentes: Musica={id_doc_musica}, Ingles={id_doc_ingles}")

    # 7. Disponibilidad: ambos disponibles lunes(1) y martes(2) en los 4 modulos
    def disponibilidad_amplia(ids_modulo):
        franjas = []
        for dia in [1, 2]:
            for bloque_id in ids_modulo:
                franjas.append({"dia_semana": dia, "bloque_id": bloque_id})
        return franjas

    for doc_id in [id_doc_musica, id_doc_ingles]:
        cliente.post(
            f"/escuelas/{escuela_id}/docentes/{doc_id}/disponibilidad",
            json=disponibilidad_amplia(ids_modulo),
        )
    print("Disponibilidad cargada (lunes y martes, todos los modulos).")

    print(f"\nLISTO. Escuela de ejemplo id={escuela_id} cargada completa.")
    cliente.close()


if __name__ == "__main__":
    main()
