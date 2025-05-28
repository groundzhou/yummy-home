from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

from core.db import SessionDep
from core.dependencies import get_token_header
from menu.models.dish import Dish

router = APIRouter(
    prefix="/dishes",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


# 获取全部
@router.get("/")
async def get_dishes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Dish]:
    dishes = session.exec(select(Dish).offset(offset).limit(limit)).all()
    return list(dishes)


# 获取单个
@router.get("/{dish_id}")
async def get_dish(dish_id: str, session: SessionDep) -> Dish:
    dish = session.get(Dish, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    return dish


# 新增
@router.post("/")
def create_dish(dish: Dish, session: SessionDep):
    session.add(dish)
    session.commit()
    session.refresh(dish)
    return dish


# 删除
@router.delete("/{dish_id}")
async def delete_dish(dish_id: str, session: SessionDep):
    dish = session.get(Dish, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    session.delete(dish)
    session.commit()
    return {"ok": True}


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
