import psycopg2
from fastapi import HTTPException
from werkzeug.security import check_password_hash
import os
import jwt
from datetime import datetime, timedelta
from src.pydantics import TokenAuth

SECRET_KEY = "liasuperpuperlolhaha923"

class Token():
    def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)) -> TokenAuth:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
        return TokenAuth(access_token=encoded_jwt, token_type="bearer")

    def decode_access_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return {"message": "Добро пожаловать!", "user_data": payload}
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    def check_token(authorization: str):
        token_prefix = "Base "
        if not authorization.startswith(token_prefix):
            raise HTTPException(status_code=401, detail="Неверный формат токена")
        token = authorization[len(token_prefix):]
        user_data = Token.decode_access_token(token)
        if not user_data or "user_data" not in user_data:
            raise HTTPException(status_code=401, detail="Невалидный или просроченный токен")
        username = user_data["user_data"]["username"]
        if not username:
            raise HTTPException(status_code=400, detail="Имя пользователя не найдено в данных токена")
        return username


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Almaty111@db:5432/lol")

def insert_user(username, password_hash):
    try:
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()
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

def find_user_id(user_data: str):
    try:
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()

        query = """
        SELECT id FROM users WHERE username = %s
        """
        cursor.execute(query, (user_data,))
        result = cursor.fetchone()
        connection.commit()

        cursor.close()
        connection.close()
        return result[0] if result else None
    except Exception as e:
        print(f"Ошибка при поиске пользователя: {e}")
        return None


def insert_params(user_id, weight_current, weight_future, height, sex, age):
    try:
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()

        # Вставить или обновить запись
        query = """
            INSERT INTO params (user_id, weight_current, weight_future, height, sex, age)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id) 
            DO UPDATE SET 
                weight_current = EXCLUDED.weight_current,
                weight_future = EXCLUDED.weight_future,
                height = EXCLUDED.height,
                sex = EXCLUDED.sex,
                age = EXCLUDED.age
            """
        cursor.execute(query, (user_id, weight_current, weight_future, height, sex, age))
        connection.commit()

        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(f"Ошибка при добавлении или обновлении значений: {e}")
        return False


def select_trains(id, difficulty, muscle_group, equipment):
    try:
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()
        if difficulty == 'Default' and muscle_group == 'Default':
            if equipment == 'Отсутствует':
                query = """
                    SELECT * FROM exercises WHERE equipment='Отсутствует'
                    """
            else:
                query = """
                    SELECT * FROM exercises WHERE equipment!='Отсутствует'
                    """
        elif difficulty == 'Default' and muscle_group != 'Default':
            if equipment == 'Отсутствует':
                query = f"""
                    SELECT * FROM exercises WHERE equipment='Отсутствует' and muscle_group='{muscle_group}'
                    """
            else:
                query = f"""
                    SELECT * FROM exercises WHERE equipment!='Отсутствует' and muscle_group='{muscle_group}'
                    """
        elif difficulty != 'Default' and muscle_group == 'Default':
            if equipment == 'Отсутствует':
                query = f"""
                    SELECT * FROM exercises WHERE equipment='Отсутствует' and difficulty='{difficulty}'
                    """
            else:
                query = f"""
                    SELECT * FROM exercises WHERE equipment!='Отсутствует'and difficulty='{difficulty}'
                    """
        else:
            if equipment == 'Отсутствует':
                query = f"""
                    SELECT * FROM exercises WHERE equipment='Отсутствует' and difficulty='{difficulty}' and muscle_group='{muscle_group}'
                    """
            else:
                query = f"""
                    SELECT * FROM exercises WHERE equipment!='Отсутствует' and difficulty='{difficulty}' and muscle_group='{muscle_group}'
                    """
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()

        cursor.close()
        connection.close()
        return result

    except Exception as e:
        print(f"Ошибка при выборке значений: {e}")
        return None

def check(username, password):
    try:
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor()

        select_query = """
            SELECT password_hash FROM users WHERE username=%s
            """
        cursor.execute(select_query, (username,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result:
            stored_password_hash = result[0]
            return check_password_hash(stored_password_hash, password)
        else:
            return False
    except Exception as e:
        print(f"Ошибка при проверке пользователя: {e}")
        return False
