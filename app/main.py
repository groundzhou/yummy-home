from fastapi import Depends, FastAPI

from core.dependencies import get_query_token, get_token_header
from core.db import create_db_and_tables
from app.menu.api import dishes

app = FastAPI(dependencies=[Depends(get_query_token)])


app.include_router(dishes.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
