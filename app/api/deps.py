import uuid
from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session
from app.core import security
from app.core.config import settings
from app.core.db import engine
from app.models.token_model import TokenPayload
from app.models.user_model import UserModel, UserTypes

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
            detail="Expired session, try to login again.",
        )
    user = session.get(UserModel, token_data.sub)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to complete the authentication.")

    return user

def is_prof(session: SessionDep, current_user: UserModel = Depends(auth_user)) -> UserModel:
    if current_user.type is UserTypes.student:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions.")
    return current_user


CurrentUser = Annotated[UserModel, Depends(auth_user)]
