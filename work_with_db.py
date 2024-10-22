from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from pydantic import BaseModel
import psycopg2
from fastapi.staticfiles import StaticFiles
from werkzeug.security import generate_password_hash, check_password_hash
import os
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "liasuperpuperlolhaha923"  # Задайте свой секретный ключ

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    """
    Создает JWT-токен с указанными данными и временем жизни.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def decode_access_token(token: str):
    """
    Декодирует JWT-токен и возвращает его данные.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None












DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Almaty111@db:5432/lol")
print(DATABASE_URL)

class Person(BaseModel):
    name: str
    password: str


class Params(BaseModel):
    user_id: int
    weight_current: int
    weight_future: int
    height: int
    sex: str
    age: int

def insert_user(username, password_hash):
    try:
        # Подключение к базе данных
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()
        # SQL-запрос на вставку данных
        insert_query = """
        INSERT INTO users (username, password_hash)
        VALUES (%s, %s)
        """
        cursor.execute(insert_query, (username, password_hash))
        connection.commit()

        cursor.close()
        connection.close()

        return True
    except Exception as e:
        print(f"Ошибка при добавлении пользователя: {e}")
        return False

def insert_params(user_id, weight_current, weight_future, height, sex, age):
    try:
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()

        query = """
        INSERT INTO params (user_id, weight_current, weight_future, height, sex, age)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, weight_current, weight_future, height, sex, age))
        connection.commit()

        cursor.close()
        connection.close()

        return True
    except Exception as e:
        print(f"Ошибка при добавлении значений: {e}")
        return False

def check(username, password):
    try:
        # Подключение к базе данных
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()

        # SQL-запрос для получения хеша пароля
        select_query = """
            SELECT password_hash FROM users WHERE username=%s
            """
        cursor.execute(select_query, (username,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        # Если пользователь найден, проверяем пароль
        if result:
            stored_password_hash = result[0]
            # Проверяем введённый пароль с хешем, сохраненным в базе
            return check_password_hash(stored_password_hash, password)
        else:
            # Пользователь не найден
            return False
    except Exception as e:
        print(f"Ошибка при проверке пользователя: {e}")
        return False

