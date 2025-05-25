from fastapi import APIRouter
from .auth_router import router as auth_router
from .roles_router import router as roles_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(roles_router)
