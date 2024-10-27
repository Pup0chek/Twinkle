from fastapi import FastAPI, HTTPException, Query
from fastapi.params import Depends
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from pydantic.fields import Annotated
from werkzeug.security import generate_password_hash
from work_with_db import insert_user, check, insert_params, Token
from pydantics import Person, Params, TokenAuth, Valid
app = FastAPI()


@app.get("/")
def get_root():
    html_content = "<h2>Hello, that's twinkle's API</h2>"
    return HTMLResponse(content=html_content)

@app.get("/registration")
def get_registration():
    return FileResponse('venv/pages/registration.html')

@app.post("/registration")
def post_registration(person: Annotated[Person, Depends()]) -> TokenAuth:
    hashs=generate_password_hash(person.password)
    if insert_user(person.name, hashs):
        access_token = Token.create_access_token(data={"username": person.name})
        return access_token
    else:
        raise HTTPException(status_code=400, detail="Ошибка при добавлении пользователя")

@app.get("/login")
def get_login():
    return FileResponse("venv/pages/login.html")

@app.post("/login")
def post_login(person: Annotated[Person, Depends()]) -> TokenAuth:
    if check(person.name, person.password):
        # Генерируем JWT-токен для пользователя
        access_token = Token.create_access_token(data={"username": person.name})
        return access_token
    else:
        raise HTTPException(status_code=400, detail="Ошибка при аутентификации")

@app.get("/congrads")
def get_congrads(token: str):
    user_data = Token.decode_access_token(token)
    valid = Valid(message="True")
    if not user_data:
        raise HTTPException(status_code=401, detail="Невалидный или просроченный токен")
        valid.message = "False"
    if valid:
        return FileResponse('venv/pages/congrads.html')

@app.get("/params")
def get_params(token: str= Query(..., description="JWT token for authentication")):
    user_data = Token.decode_access_token(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Невалидный или просроченный токен")
    return FileResponse('venv/pages/params.html')
    #insert_params(**params.dict())

@app.post("/params")
def post_params(params: Annotated[Params, Depends()]):
    pass