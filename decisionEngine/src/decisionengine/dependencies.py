# src/decisionengine/dependencies.py
from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from decisionengine.core.graph import Graph
from decisionengine.core.decision import DecisionService
from decisionengine.models.location import Location
from decisionengine.core.vehicle_repository import VehicleRepository
from decisionengine.db.in_memory_vehicle_repository import InMemoryVehicleRepository

from decisionengine.db.mongo_user_repository import MongoUserRepository
from decisionengine.config.settings import settings

from decisionengine.core.auth_service import AuthService
from decisionengine.core.user_repository import UserRepository

from decisionengine.db.MongoOrderRepository import MongoOrderRepository
_graph: Graph | None = None


def get_graph() -> Graph:
    global _graph
    if _graph is None:
        graph = Graph()
        a = Location(0, 0)
        b = Location(0, 1)
        c = Location(0, 2)
        d = Location(1, 1)

        graph.add_edge(a, b, 5)
        graph.add_edge(b, c, 3)
        graph.add_edge(a, d, 7)
        graph.add_edge(d, a, 7)
        _graph = graph
    return _graph


def zero_heuristic(a, b) -> float:
    return 0.0


def get_heuristic():
    return zero_heuristic


def get_vehicle_repository() -> VehicleRepository:
    return InMemoryVehicleRepository()


def get_decision_service(
    heuristic=Depends(get_heuristic),
    vehicle_repository: VehicleRepository = Depends(get_vehicle_repository),
) -> DecisionService:
    return DecisionService(
        heuristic=heuristic,
        vehicle_repository=vehicle_repository,
    )


def get_decision_context(
    service: DecisionService = Depends(get_decision_service),
    graph: Graph = Depends(get_graph),
    vehicle_repository: VehicleRepository = Depends(get_vehicle_repository),
):
    return service, graph, vehicle_repository


def get_user_repository() -> UserRepository:
    return MongoUserRepository(settings.MONGO_URI, settings.MONGO_DB)

def get_order_repository() -> MongoOrderRepository:
    return MongoOrderRepository(settings.MONGO_URI)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"  
)


def get_auth_service() -> AuthService:
    return AuthService()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service),
):
    email = auth_service.decode_token(token)

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = user_repository.get_by_email(email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user