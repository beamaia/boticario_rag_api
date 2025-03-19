from fastapi import APIRouter

from app.app.endpoints import upload_file, retrieve_query

api_router = APIRouter()

api_router.include_router(upload_file.router)
api_router.include_router(retrieve_query.router)