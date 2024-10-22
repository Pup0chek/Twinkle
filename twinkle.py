from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from werkzeug.security import generate_password_hash
from work_with_db import Person, insert_user, check, Params, insert_params
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
        raise HTTPException(status_code=401, detail="Неверные имя пользователя или пароль")

@app.get("/congrads")
def get_congrads():
    return FileResponse('congrads.html')

@app.get("/params")
def get_params(params: Params):
    insert_params(**params.dict().values())
