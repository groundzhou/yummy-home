from fastapi import Depends, FastAPI

from .core.dependencies import get_query_token
from .core.db import create_db_and_tables
from .menu.api import dishes

app = FastAPI(dependencies=[Depends(get_query_token)])


app.include_router(dishes.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/createdb")
async def create_db():
    create_db_and_tables();

