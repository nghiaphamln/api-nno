from fastapi import FastAPI
from routers import address

app = FastAPI()

app.include_router(address.router)


@app.get("/")
async def root():
    return {'message': 'API Code By NghiaPH!'}
