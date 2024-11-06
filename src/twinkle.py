from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from starlette.templating import Jinja2Templates
templates = Jinja2Templates(directory="pages")
from src.work_with_db import Token
from src.pydantics import Valid
from src.routes.params import params_router
from src.routes.train import train_router
from src.routes.login import login_router
from src.routes.registration import registration_router

app = FastAPI()
app.include_router(params_router)
app.include_router(train_router)
app.include_router(login_router)
app.include_router(registration_router)


@app.get("/")
def get_root():
    html_content = "<h2>Hello, that's twinkle's API</h2>"
    return HTMLResponse(content=html_content)


@app.get("/congrads")
def get_congrads(token: str):
    user_data = Token.decode_access_token(token)
    valid = Valid(message="True")
    if not user_data:
        raise HTTPException(status_code=401, detail="Невалидный или просроченный токен")
        valid.message = "False"
    if valid:
        return FileResponse('pages/congrads.html')



