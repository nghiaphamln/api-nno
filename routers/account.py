import os
from typing import Union, Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sql_app.database import get_database
from sqlalchemy.orm import Session
from crud import account_crud
from schemas import account_schema
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta
from pydantic import ValidationError

load_dotenv()
router = APIRouter(
    prefix='/Account'
)

SECURITY_ALGORITHM = os.getenv('SECURITY_ALGORITHM')
SECRET_KEY = os.getenv('SECRET_KEY')
reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)


def generate_token(username: Union[str, Any]) -> str:
    expire = datetime.utcnow() + timedelta(
        seconds=60 * 60 * 24 * 3  # Expired after 3 days
    )
    to_encode = {
        'exp': expire, 'username': username
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=SECURITY_ALGORITHM)
    return encoded_jwt


def validate_token(http_authorization_credentials=Depends(reusable_oauth2)) -> str:
    try:
        payload = jwt.decode(http_authorization_credentials.credentials, SECRET_KEY, algorithms=[SECURITY_ALGORITHM])
        if payload.get('exp') < datetime.timestamp(datetime.utcnow()):
            raise HTTPException(
                status_code=403,
                detail='Token đã hết hạn.'
            )
        return payload.get('username')
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail='Token không hợp lệ.'
        )


@router.get('/')
async def root():
    return {'detail': 'Root of Account Router.'}


@router.post('/Register')
async def register(account: account_schema.UserSchema, database: Session = Depends(get_database)):
    if account_crud.create_account(database, account):
        return {'detail': 'Đã đăng ký tài khoản thành công.'}
    else:
        raise HTTPException(
            status_code=409,
            detail='Tài khoản đã tồn tại, vui lòng sử dụng tài khoản khác.'
        )


@router.post('/Login')
async def login(accout: account_schema.LoginRequest, database: Session = Depends(get_database)):
    if account_crud.login(database, accout):
        return {'token': generate_token(accout.username)}
    else:
        raise HTTPException(
            status_code=401,
            detail='Tài khoản hoặc mật khẩu không chính xác.'
        )


@router.get('/GetUserInfo', dependencies=[Depends(validate_token)])
async def get_user_info(username: str = Depends(validate_token), database: Session = Depends(get_database)):
    return account_crud.get_user_information(database, username)