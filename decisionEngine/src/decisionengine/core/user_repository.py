from abc import ABC, abstractmethod
from decisionengine.models.user import User


class UserRepository(ABC):

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def update(self, user: User) -> None:
        pass

    @abstractmethod
    def delete(self, email: str) -> None:
        pass

    @abstractmethod
    def list_all(self) -> list[User]:
        pass