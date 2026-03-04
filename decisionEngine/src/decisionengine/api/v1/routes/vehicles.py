from fastapi import APIRouter, Depends

from decisionengine.api.v1.schemas.vehicle import VehicleSchema
from decisionengine.dependencies import get_vehicle_repository
from decisionengine.api.v1.mappers.vehicle_mapper import VehicleMapper
from decisionengine.core.vehicle_repository import VehicleRepository

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("/", response_model=list[VehicleSchema])
def list_vehicles(
    vehicle_repository: VehicleRepository = Depends(get_vehicle_repository),
):
    vehicles = vehicle_repository.get_available_vehicles()

    return [
        VehicleMapper.to_schema(v)
        for v in vehicles
    ]
