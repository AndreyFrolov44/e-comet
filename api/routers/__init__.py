from fastapi import APIRouter

from routers import cities

router = APIRouter()
router.include_router(cities.router, prefix='/cities')
