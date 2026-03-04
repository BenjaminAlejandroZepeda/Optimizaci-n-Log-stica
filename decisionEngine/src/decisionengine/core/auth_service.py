from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from datetime import datetime, timezone
from decisionengine.config.settings import settings


class AuthService:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_expire_days = 7

    def create_access_token(self, email: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.access_expire_minutes
        )

        payload = {
            "sub": email,
            "exp": expire,
            "type": "access",
        }

        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )

    def create_refresh_token(self, email: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            days=self.refresh_expire_days
        )

        payload = {
            "sub": email,
            "exp": expire,
            "type": "refresh",
        }

        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )

    def decode_token(
        self,
        token: str,
        expected_type: str = "access",
    ) -> Optional[str]:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )

            if payload.get("type") != expected_type:
                return None

            return payload.get("sub")

        except JWTError:
            return None