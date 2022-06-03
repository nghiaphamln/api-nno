from fastapi import FastAPI
from routers import address, account
from sql_app import models
from sql_app.database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(address.router)
app.include_router(account.router)


@app.get('/')
async def root():
    return {'detail': 'API Code By NghiaPH.'}
