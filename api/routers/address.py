from fastapi import APIRouter
import socket


router = APIRouter(
    prefix='/Information'
)


@router.get('/')
async def root():
    return {'message': 'Root of Address Router.'}


@router.get('/GetIP')
async def get_id():
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    return {
        'hostName': host_name,
        'internetProtocolAddress': ip_address
    }
