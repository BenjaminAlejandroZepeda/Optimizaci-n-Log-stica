from fastapi import APIRouter

from .decisions import router as decisions_router
from .orders import router as orders_router
from .vehicles import router as vehicles_router
from .health import router as health_router
from .graph import router as graph_router
from .auth import router as auth_router
from .scoring import router as scoring_router

router = APIRouter()

router.include_router(decisions_router)
router.include_router(orders_router)
router.include_router(vehicles_router)
router.include_router(health_router)
router.include_router(graph_router)
router.include_router(auth_router)
router.include_router(scoring_router)