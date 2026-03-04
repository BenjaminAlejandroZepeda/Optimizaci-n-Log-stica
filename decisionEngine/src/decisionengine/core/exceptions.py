class DomainError(Exception):
    """Clase base para errores a nivel de dominio."""
    pass


class NoVehicleAvailableError(DomainError):
    """Se genera cuando ningún vehículo puede satisfacer las restricciones del pedido.."""
    pass


class RouteNotFoundError(DomainError):
    """Se genera cuando no se puede calcular una ruta entre dos ubicaciones."""
    pass
