from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.responses import FileResponse
from pydantic.fields import Annotated
from starlette.templating import Jinja2Templates
templates = Jinja2Templates(directory="pages")
from werkzeug.security import generate_password_hash
from src.work_with_db import insert_user, Token
from src.pydantics import Person, TokenAuth

registration_router = APIRouter(prefix="/registration", tags=['Registration'])


@registration_router.get("/")
def get_registration():
    return FileResponse('pages/registration.html')

@registration_router.post("/")
def post_registration(person: Annotated[Person, Depends()]) -> TokenAuth:
    hashs=generate_password_hash(person.password)
    if insert_user(person.name, hashs):
        access_token = Token.create_access_token(data={"username": person.name})
        return access_token
    else:
        raise HTTPException(status_code=400, detail="Ошибка при добавлении пользователя")