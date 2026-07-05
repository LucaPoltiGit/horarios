from fastapi import APIRouter

from app.api import bloques, escuelas, grados, materias

router = APIRouter()

router.include_router(escuelas.router)
router.include_router(bloques.router)
router.include_router(grados.router)
router.include_router(materias.router)
