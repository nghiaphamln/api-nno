from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str
    fullname: str


class LoginRequest(BaseModel):
    username: str
    password: str
