from fastapi import APIRouter

from app.api import bloques, escuelas, grados

router = APIRouter()

router.include_router(escuelas.router)
router.include_router(bloques.router)
router.include_router(grados.router)
