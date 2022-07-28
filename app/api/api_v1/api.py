from app.api.api_v1.routers import auth, roles, \
    users, file, permissions, dashboard,\
    general_information, user_resume , data_import
from fastapi import APIRouter


api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router_admin)
api_router.include_router(users.router_user)
api_router.include_router(roles.router)
api_router.include_router(permissions.router)
api_router.include_router(file.router)
api_router.include_router(general_information.router)
api_router.include_router(user_resume.router)
api_router.include_router(dashboard.router)
api_router.include_router(data_import.router)
