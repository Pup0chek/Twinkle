from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, Query
from fastapi.params import Depends, Header
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from pydantic.fields import Annotated
from starlette.templating import Jinja2Templates
from starlette.requests import Request
templates = Jinja2Templates(directory="pages")
#from pygments.lexers import templates
from werkzeug.security import generate_password_hash
from src.work_with_db import insert_user, check, insert_params, Token, find_user_id, select_trains
from src.pydantics import Person, Params, TokenAuth, Valid, Trains

params_router = APIRouter(prefix="/params", tags=['Parameters'])


@params_router.get("/")
def get_params(token: str= Query(..., description="JWT token for authentication")):
    user_data = Token.decode_access_token(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Невалидный или просроченный токен")
    return FileResponse('pages/params.html')

@params_router.post("/")
def post_params(params: Params, authorization: str = Header(...)):
    if Token.check_token(authorization):
        insert_params(find_user_id(Token.check_token(authorization)), params.weight_current, params.weight_future, params.height, params.sex,
                      params.age)
        return {"message": "Декодирование токена успешно", "username": Token.check_token(authorization)}