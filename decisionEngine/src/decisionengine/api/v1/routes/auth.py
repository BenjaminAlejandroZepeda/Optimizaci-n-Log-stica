from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
import bcrypt

from decisionengine.models.user import User
from decisionengine.dependencies import (
    get_current_user,
    get_user_repository,
    get_auth_service,
)
from decisionengine.core.auth_service import AuthService
from decisionengine.core.user_repository import UserRepository
from decisionengine.api.v1.schemas.auth import (
    UserRegisterSchema,
    UserResponseSchema,
    TokenResponseSchema,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    payload: UserRegisterSchema,
    user_repository: UserRepository = Depends(get_user_repository),
):
    email = payload.email.lower().strip()

    existing = user_repository.get_by_email(email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    if len(payload.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters",
        )

    hashed = bcrypt.hashpw(
        payload.password.encode(),
        bcrypt.gensalt(),
    ).decode()

    user = User.create(
        email=email,
        hashed_password=hashed,
    )

    user_repository.save(user)

    return user


@router.post(
    "/login",
    response_model=TokenResponseSchema,
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service),
):
    user = user_repository.get_by_email(form_data.username.lower().strip())

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not bcrypt.checkpw(
        form_data.password.encode(),
        user.hashed_password.encode(),
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = auth_service.create_access_token(user.email)
    refresh_token = auth_service.create_refresh_token(user.email)

    return TokenResponseSchema(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@router.get(
    "/me",
    response_model=UserResponseSchema,
)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


