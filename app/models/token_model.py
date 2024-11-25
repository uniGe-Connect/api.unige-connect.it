from sqlmodel import SQLModel

from app.resources.user_resource import UserPublic


class Token(SQLModel):
    access_token: str
    token_type: str = "Bearer"
    user: UserPublic


class TokenPayload(SQLModel):
    sub: str | None = None
