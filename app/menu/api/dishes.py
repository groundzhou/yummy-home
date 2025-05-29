from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select

from app.core.db import SessionDep
from app.core.dependencies import get_token_header
from ..models.dish import Dish, DishCreate, DishUpdate

router = APIRouter(
    prefix="/dishes",
    tags=["dishes"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


# 获取全部
@router.get("/", response_model=list[Dish])
def get_dishes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    dishes = session.exec(select(Dish).offset(offset).limit(limit)).all()
    return dishes


# 获取单个
@router.get("/{dish_id}", response_model=Dish)
def get_dish(dish_id: int, session: SessionDep) -> Dish:
    dish = session.get(Dish, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    return dish


# 新增
@router.post("/", response_model=Dish)
def create_dish(dish: DishCreate, session: SessionDep):
    db_dish = Dish.model_validate(dish)
    session.add(db_dish)
    session.commit()
    session.refresh(db_dish)
    return db_dish


# 删除
@router.delete("/{dish_id}")
def delete_dish(dish_id: int, session: SessionDep):
    dish = session.get(Dish, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    session.delete(dish)
    session.commit()
    return {"ok": True}


# 更新
@router.patch("/{dish_id}", response_model=Dish)
def update_dish(dish_id: int, dish: DishUpdate, session: SessionDep):
    dish_db = session.get(Dish, dish_id)
    if not dish_db:
        raise HTTPException(status_code=404, detail="Dish not found")
    dish_data = dish.model_dump(exclude_unset=True)  # 排除默认值
    dish_db.sqlmodel_update(dish_data)
    session.add(dish_db)
    session.commit()
    session.refresh(dish_db)
    return dish_db
