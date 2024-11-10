from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.responses import FileResponse
from pydantic.fields import Annotated
from starlette.templating import Jinja2Templates
templates = Jinja2Templates(directory="pages")
from src.work_with_db import check, Token
from src.pydantics import Person, TokenAuth

login_router = APIRouter(prefix="/login", tags=['Login'])


@login_router.get("/")
def get_login():
    #return {"massage": "login.get"}
    return FileResponse("pages/login.html")

@login_router.post("/")
def post_login(person: Annotated[Person, Depends()]) -> TokenAuth:
    if check(person.name, person.password):
        # Генерируем JWT-токен для пользователя
        access_token = Token.create_access_token(data={"username": person.name})
        return access_token
    else:
        raise HTTPException(status_code=400, detail="Ошибка при аутентификации")