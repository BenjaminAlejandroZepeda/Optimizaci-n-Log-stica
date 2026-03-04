# src/decisionengine/db/mongo_user_repository.py
from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import OperationFailure, ConfigurationError, PyMongoError

from decisionengine.core.user_repository import UserRepository
from decisionengine.models.user import User


class MongoUserRepository(UserRepository):
    def __init__(self, mongo_uri: str, db_name: str = "decision_engine"):

        self.client = MongoClient(mongo_uri, server_api=ServerApi('1'))
        try:
            
            self.client.admin.command("ping")
        except OperationFailure as e:
         
            raise RuntimeError(f"[Mongo] OperationFailure durante ping: {e}") from e
        except ConfigurationError as e:
           
            raise RuntimeError(f"[Mongo] ConfigurationError: {e}") from e
        except PyMongoError as e:
            raise RuntimeError(f"[Mongo] PyMongoError: {e}") from e

        # DB y colección
        self.db = self.client[db_name]
        self.collection = self.db["users"]

        
        self.collection.create_index("email", unique=True)



    def get_by_email(self, email: str) -> Optional[User]:
        doc = self.collection.find_one({"email": email})
        return self._map_to_domain(doc) if doc else None

    def save(self, user: User) -> None:
        
        now = datetime.utcnow()
        if getattr(user, "created_at", None) is None:
            user.created_at = now
        user.updated_at = now

        result = self.collection.insert_one(self._map_to_document(user))
      
        user.id = str(result.inserted_id)

    def update(self, user: User) -> None:
        user.updated_at = datetime.utcnow()
        self.collection.update_one(
            {"email": user.email},
            {"$set": self._map_to_document(user)}
        )

    def delete(self, email: str) -> None:
        self.collection.delete_one({"email": email})

    def list_all(self) -> List[User]:
        documents = self.collection.find()
        return [self._map_to_domain(doc) for doc in documents]

 

    def _map_to_document(self, user: User) -> dict:
        return {
            "email": user.email,
            "hashed_password": user.hashed_password,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "last_login_at": getattr(user, "last_login_at", None),
        }

    def _map_to_domain(self, doc: dict) -> User:
        return User(
            id=str(doc.get("_id")),
            email=doc["email"],
            hashed_password=doc["hashed_password"],
            created_at=doc["created_at"],
            updated_at=doc.get("updated_at"),
            last_login_at=doc.get("last_login_at"),
        )