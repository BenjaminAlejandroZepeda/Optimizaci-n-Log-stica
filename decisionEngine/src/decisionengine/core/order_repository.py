from typing import Protocol
from decisionengine.models.order import Order


class OrderRepository(Protocol):
    """
    Command repository abstraction.
    The core layer does NOT know if this is MongoDB, memory, etc.
    """

    def save(self, order: Order) -> str:
        """
        An order persists and returns its generated ID.
        """
        ...

    def get_by_id(self, order_id: str) -> Order | None:
        """
        You get an order by your ID.
        """
        ...

    def list_all(self) -> list[Order]:
        """
        List all stored orders.
        """
        ...

    def delete(self, order_id: str) -> None:
        """

        Delete an order by ID.
        """
        ...