from fastapi import Header, HTTPException


async def get_token_header(x_token: str = Header()):
    if x_token != "zhou":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "ground":
        raise HTTPException(status_code=400, detail="No Ground token provided")