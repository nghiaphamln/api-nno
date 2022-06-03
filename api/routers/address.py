from fastapi import APIRouter, Depends
import socket
from routers.account import validate_token


router = APIRouter(
    prefix='/Information'
)


@router.get('/')
async def root():
    return {'message': 'Root of Address Router.'}


@router.get('/GetIP', dependencies=[Depends(validate_token)])
async def get_id():
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    return {
        'hostName': host_name,
        'internetProtocolAddress': ip_address
    }
