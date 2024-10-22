from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from pydantic import BaseModel
import psycopg2
from fastapi.staticfiles import StaticFiles
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Almaty111@db:5432/lol")
print(DATABASE_URL)
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

class Person(BaseModel):
    name: str
    password: str



@app.get("/")
def read_root():
    html_content = "<h2>Hello, that's twinkle's API</h2>"
    return HTMLResponse(content=html_content)


@app.get("/registration")
def get_hello():
    return FileResponse('registration.html')

@app.post("/registration")
def hello(person: Person):
    hashs=generate_password_hash(person.password)
    insert_user(person.name, hashs)
    return True

@app.get("/login")
def get_login():
    return FileResponse("login.html")

@app.post("/login")
def post_login(person: Person):
    if check(person.name, person.password):
        return {"message": "Успешный вход"}
    else:
        raise BaseException()

@app.get("/congrads")
def get_lol_html():
    return FileResponse('congrads.html')


