from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI()

# НАСТРОЙКА CORS: Это решит проблему "не работает" при запросах с ПК
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы со всех адресов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

# Имитация базы данных (данные сбросятся при перезагрузке сервера)
users_db = {}
videos_db = []

# Модели данных
class UserData(BaseModel):
    login: str
    password: str

class VideoData(BaseModel):
    title: str
    author: str
    video_url: str
    thumb_url: Optional[str] = None

# Главная страница (чтобы не было Not Found)
@app.get("/")
async def root():
    return {"status": "online", "message": "LIMEON Server is Live!"}

# РЕГИСТРАЦИЯ
@app.post("/register")
async def register(user: UserData):
    if user.login in users_db:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    users_db[user.login] = {"password": user.password, "name": user.login}
    return {"message": "Успешная регистрация"}

# ВХОД
@app.post("/login")
async def login(user: UserData):
    if user.login not in users_db:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if users_db[user.login]["password"] != user.password:
        raise HTTPException(status_code=401, detail="Неверный пароль")
    return {"message": "Вход выполнен", "name": users_db[user.login]["name"]}

# ПОЛУЧЕНИЕ ВСЕХ ВИДЕО
@app.get("/videos")
async def get_videos():
    return videos_db

# ЗАГРУЗКА ВИДЕО
@app.post("/upload")
async def upload_video(video: VideoData):
    videos_db.append(video.dict())
    return {"message": "Видео успешно добавлено на сервер"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
