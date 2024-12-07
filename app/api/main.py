from fastapi import APIRouter
from app.api.routes import group_routes, auth_routes, member_routes
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(auth_routes.router, tags=["Authentication"])
api_router.include_router(group_routes.router, tags=["Groups"])
api_router.include_router(member_routes.router, tags=["Member"])

is_local = settings.ENVIRONMENT != "production"

if is_local:
    from app.api.routes import doc_routes
    api_router.include_router(doc_routes.router)