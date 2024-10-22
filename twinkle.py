from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from werkzeug.security import generate_password_hash
from work_with_db import Person, insert_user, check, Params, insert_params, create_access_token, decode_access_token
import jwt
from datetime import datetime, timedelta
app = FastAPI()


@app.get("/")
def get_root():
    html_content = "<h2>Hello, that's twinkle's API</h2>"
    return HTMLResponse(content=html_content)

@app.get("/registration")
def get_registration():
    return FileResponse('registration.html')

@app.post("/registration")
def post_registration(person: Person):
    hashs=generate_password_hash(person.password)
    if insert_user(person.name, hashs):
        # Генерируем JWT-токен для пользователя
        access_token = create_access_token(data={"username": person.name})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при добавлении пользователя")

@app.get("/login")
def get_login():
    return FileResponse("login.html")

@app.post("/login")
def post_login(person: Person):
    if check(person.name, person.password):
        # Генерируем JWT-токен для пользователя
        access_token = create_access_token(data={"username": person.name})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Ошибка при аутентификации")

@app.get("/congrads")
def get_congrads(token: str):
    user_data = decode_access_token(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Невалидный или просроченный токен")
    return {"message": "Добро пожаловать!", "user_data": user_data}
    #return FileResponse('congrads.html')

@app.get("/params")
def get_params(params: Params):
    insert_params(**params.dict().values())
