from fastapi import APIRouter, Depends

from decisionengine.api.v1.schemas.vehicle import VehicleSchema
from decisionengine.dependencies import get_vehicles
from decisionengine.api.v1.mappers.vehicle_mapper import VehicleMapper

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("/", response_model=list[VehicleSchema])
def list_vehicles(vehicles=Depends(get_vehicles)):
    return [
        VehicleMapper.to_schema(v)
        for v in vehicles
    ]
