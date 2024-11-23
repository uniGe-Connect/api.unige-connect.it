from fastapi import APIRouter

from app.api.routes import groups, items, login, users, utils, saml

api_router = APIRouter()
api_router.include_router(groups.router)
api_router.include_router(saml.router, tags=["saml"])


# example
# api_router.include_router(login.router, tags=["login"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
