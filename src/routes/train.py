from fastapi import APIRouter
from fastapi import HTTPException, Query
from fastapi.params import Header
from fastapi.responses import FileResponse
from starlette.templating import Jinja2Templates
from starlette.requests import Request
templates = Jinja2Templates(directory="pages")
from src.work_with_db import Token, find_user_id, select_trains
from src.pydantics import Trains

train_router = APIRouter(prefix="/train", tags=['Train'])


@train_router.get("/")
def get_train(token: str= Query(..., description="JWT token for authentication")):
    user_data = Token.decode_access_token(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Невалидный или просроченный токен")
    return FileResponse('pages/train.html')

@train_router.post("/")
def post_train(request: Request, trains: Trains, authorization: str = Header(...)):
    if Token.check_token(authorization):
        user_id = find_user_id(Token.check_token(authorization))
        result= select_trains(find_user_id(Token.check_token(authorization)), trains.difficulty, trains.muscle_groupp, trains.equipment)
        if result:  # Если результат не пустой
            return templates.TemplateResponse("train.html", {"request": request, "exercises": result})
        else:
            return {"message": "Не удалось найти подходящие упражнения."}
    else:
            return {"message": "Неавторизованный доступ"}