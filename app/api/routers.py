from fastapi import APIRouter
from app.api.endpoints import (
    auth_router, profile_router, question_router, page_router, meal_router, workout_router)

main_router = APIRouter()
main_router.include_router(page_router)
main_router.include_router(question_router)
main_router.include_router(auth_router)
main_router.include_router(profile_router)
main_router.include_router(meal_router)
main_router.include_router(workout_router)