from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, equipment, orders, reviews, chat, shifts

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(equipment.router, prefix="/equipment", tags=["equipment"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(shifts.router, prefix="/shifts", tags=["shifts"]) 