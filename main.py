import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routes.book import book_router
from api.routes.user import user_router

load_dotenv()

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Только для React-приложения
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
    expose_headers=["Content-Type"]
)

app.include_router(book_router, prefix="/book")
app.include_router(user_router, prefix="/user")

if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=8000)#95.163.85.129