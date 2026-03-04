import os

import uuid

os.environ["MONGO_URI"] = "mongodb://fake:27017/testdb"
os.environ["SECRET_KEY"] = "test_secret_key"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "60"

import pytest
from fastapi.testclient import TestClient
from decisionengine.models.location import Location
from decisionengine.main import create_app
from decisionengine.dependencies import (
    get_user_repository,
    get_vehicle_repository
)

from decisionengine.models.user import User
from decisionengine.models.vehicle import Vehicle
from decisionengine.models.enums import VehicleType


class FakeUserRepository:
    def __init__(self):
        self.users = {}

    def save(self, user: User):
        if not getattr(user, "id", None):
            user.id = str(uuid.uuid4())  

        self.users[user.email] = user
        return user

    def create(self, user: User):
        return self.save(user)

    def get_by_email(self, email: str):
        return self.users.get(email)

    def get_by_id(self, user_id: int):
        for user in self.users.values():
            if user.id == user_id:
                return user
        return None

    def list_all(self):
        return list(self.users.values())

    def delete(self, user_id: int):
        for email, user in list(self.users.items()):
            if user.id == user_id:
                del self.users[email]
                return True
        return False


class FakeVehicleRepository:

    def __init__(self):
        self.vehicles = [
            Vehicle(
                id="1",
                vehicle_type=VehicleType.BIKE,
                capacity_kg=20,
                current_location=Location(latitude=0, longitude=0),
                is_available=True,
            ),
            Vehicle(
                id="2",
                vehicle_type=VehicleType.CAR,
                capacity_kg=100,
                current_location=Location(latitude=0, longitude=0),
                is_available=True,
            ),
        ]

    def get_available_vehicles(self):
        return [v for v in self.vehicles if v.is_available]

    def save(self, vehicle):
        self.vehicles.append(vehicle)

    def update(self, vehicle):
        for i, v in enumerate(self.vehicles):
            if v.id == vehicle.id:
                self.vehicles[i] = vehicle
                return vehicle
        return None




@pytest.fixture
def client():
    app = create_app()

    fake_user_repo = FakeUserRepository()
    fake_vehicle_repo = FakeVehicleRepository()

    app.dependency_overrides[get_user_repository] = lambda: fake_user_repo
    app.dependency_overrides[get_vehicle_repository] = lambda: fake_vehicle_repo

    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()