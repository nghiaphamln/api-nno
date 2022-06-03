from fastapi import APIRouter, Depends
import socket
from routers.account import validate_token
import urllib.request


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
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    return {
        'hostName': host_name,
        'localInternetProtocol': ip_address,
        'externalnternetProtocol': external_ip
    }
