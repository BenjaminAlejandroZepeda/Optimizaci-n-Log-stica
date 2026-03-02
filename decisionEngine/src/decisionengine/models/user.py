from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass
class User:
    id: str | None
    email: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime]

    @classmethod
    def create(cls, email: str, hashed_password: str) -> "User":
        now = datetime.now(timezone.utc)
        return cls(
            id=None,
            email=email,
            hashed_password=hashed_password,
            created_at=now,
            updated_at=now,
            last_login_at=None
        )

    def register_login(self):
        self.last_login_at = datetime.now(timezone.utc)

    def change_password(self, new_hashed_password: str):
        self.hashed_password = new_hashed_password
        self.updated_at = datetime.now(timezone.utc)