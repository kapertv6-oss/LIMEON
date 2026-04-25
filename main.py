from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI()

# Разрешаем фронтенду подключаться к бэкенду
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Имитация базы данных (в реальности тут будет PostgreSQL или MongoDB)
users_db = {}
videos_db = []

class User(BaseModel):
    login: str
    password: str
    name: Optional[str] = None

class Video(BaseModel):
    title: str
    author: str
    video_url: str
    thumb_url: Optional[str] = None

@app.post("/register")
async def register(user: User):
    if user.login in users_db:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    users_db[user.login] = {"password": user.password, "name": user.login}
    return {"message": "Успешная регистрация"}

@app.post("/login")
async def login(user: User):
    if user.login not in users_db or users_db[user.login]["password"] != user.password:
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")
    return {"message": "Вход выполнен", "name": users_db[user.login]["name"]}

@app.get("/videos")
async def get_videos():
    return videos_db

@app.post("/upload")
async def upload_video(video: Video):
    videos_db.append(video.dict())
    return {"message": "Видео добавлено"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
