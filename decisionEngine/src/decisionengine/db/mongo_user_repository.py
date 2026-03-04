from pymongo import MongoClient
from decisionengine.core.user_repository import UserRepository
from decisionengine.models.user import User
from datetime import datetime


class MongoUserRepository(UserRepository):

    def __init__(self, mongo_uri: str):
        self.client = MongoClient(mongo_uri)
        self.db = self.client["decision_engine"]
        self.collection = self.db["users"]
        self.collection.create_index("email", unique=True)

    def get_by_email(self, email: str) -> User | None:
        doc = self.collection.find_one({"email": email})
        return self._map_to_domain(doc) if doc else None

    def save(self, user: User) -> None:
        result = self.collection.insert_one(self._map_to_document(user))
        user.id = str(result.inserted_id) 

    def update(self, user: User) -> None:
        self.collection.update_one(
            {"email": user.email},
            {"$set": self._map_to_document(user)}
        )

    def delete(self, email: str) -> None:
        self.collection.delete_one({"email": email})

    def list_all(self) -> list[User]:
        documents = self.collection.find()
        return [self._map_to_domain(doc) for doc in documents]

    def _map_to_document(self, user: User) -> dict:
        return {
            "email": user.email,
            "hashed_password": user.hashed_password,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "last_login_at": user.last_login_at,
        }

    def _map_to_domain(self, doc: dict) -> User:
        return User(
            id=str(doc.get("_id")),
            email=doc["email"],
            hashed_password=doc["hashed_password"],
            created_at=doc["created_at"],
            updated_at=doc["updated_at"],
            last_login_at=doc.get("last_login_at"),
        )