from typing import Protocol, runtime_checkable
from decisionengine.models.vehicle import Vehicle


@runtime_checkable
class VehicleRepository(Protocol):

    def list_all(self) -> list[Vehicle]:
        """Return all vehicles."""
        ...

    def list_available(self) -> list[Vehicle]:
        """Return only available vehicles."""
        ...

    def get_by_id(self, vehicle_id: int) -> Vehicle | None:
        """Return vehicle by id or None if not found."""
        ...

    def save(self, vehicle: Vehicle) -> None:
        """Persist a vehicle."""
        ...

    def update(self, vehicle: Vehicle) -> None:
        """Update existing vehicle."""
        ...

    def delete(self, vehicle_id: int) -> None:
        """Delete vehicle by id."""
        ...
