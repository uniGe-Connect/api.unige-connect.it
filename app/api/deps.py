import uuid
from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

from app.controllers.group_controller import group_controller
from app.core import security
from app.core.config import settings
from app.core.db import engine
from app.models.group_model import GroupModel
from app.models.token_model import TokenPayload
from app.models.user_model import UserModel

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="docs/login"
)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def auth_user(session: SessionDep, token: TokenDep) -> UserModel:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(UserModel, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


CurrentUser = Annotated[UserModel, Depends(auth_user)]


def get_current_active_superuser(current_user: CurrentUser) -> UserModel:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user

def group_owner(_id: uuid.UUID, current_user: UserModel = Depends(auth_user)) -> GroupModel:
    group = group_controller.get(id=_id)
    if group.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of this group")
    return group