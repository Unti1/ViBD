from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.api.v1.api import api_router
from settings.config import settings

app = FastAPI(
    title="ViBD API",
    description="API для системы управления инвентарем спортивного клуба",
    version="1.0.0",
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Добро пожаловать в API системы учета инвентаря спортивного клуба"} 

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)