from fastapi import APIRouter
from fastapi import HTTPException, Query
from fastapi.params import Header
from fastapi.responses import FileResponse
from starlette.templating import Jinja2Templates
templates = Jinja2Templates(directory="pages")
from src.work_with_db import insert_params, Token, find_user_id
from src.pydantics import Params
from src.diet import calculate_daily_calories

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
        result = calculate_daily_calories(params.age, params.height, params.weight_current, params.weight_future, params.sex)
        return {"message": result, "username": Token.check_token(authorization)}