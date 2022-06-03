from fastapi import APIRouter, Depends, Response, status
from sql_app.database import get_database
from sqlalchemy.orm import Session
from crud import account_crud
from schemas import account_schema

router = APIRouter(
    prefix='/Account'
)


@router.get('/')
async def root():
    return {'message': 'Root of Account Router.'}


@router.post('/Register')
async def register(account: account_schema.UserSchema, response: Response, database: Session = Depends(get_database)):
    if account_crud.create_account(database, account):
        return {'message': 'Đã đăng ký tài khoản thành công.'}
    else:
        response.status_code = status.HTTP_409_CONFLICT
        return {'message': 'Tài khoản đã tồn tại, vui lòng sử dụng tài khoản khác.'}
