from pydantic import BaseModel


class TokenAuth(BaseModel):
    access_token: str
    token_type: str

class Person(BaseModel):
    name: str
    password: str

class Params(BaseModel):
    weight_current: int
    weight_future: int
    height: int
    sex: str
    age: int

class Trains(BaseModel):
    difficulty: str
    muscle_groupp: str
    equipment: str

class Valid(BaseModel):
    message: str