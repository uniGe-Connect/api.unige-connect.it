from fastapi import APIRouter
from app.api.routes import group_routes, auth_routes

api_router = APIRouter()
api_router.include_router(auth_routes.router)
api_router.include_router(group_routes.router)
