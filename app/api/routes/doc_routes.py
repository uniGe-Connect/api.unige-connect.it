from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from app.api.deps import SessionDep
from app.api.routes.utils import router
from app.controllers.user_controller import user_controller
from app.core import security
from app.core.config import settings
from app.models.user_model import UserModel


@router.post("/docs/login", include_in_schema=False)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    query = select(UserModel).where(UserModel.email == form_data.username)
    users = user_controller.get_multi(query=query, session=session)
    user = users[0] if users else None
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")

    expiration = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return {"access_token": security.create_access_token(user.id, expires_delta=expiration), "token_type": "bearer"}