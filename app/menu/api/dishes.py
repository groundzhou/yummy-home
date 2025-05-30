from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select

from app.core.db import SessionDep
from app.core.dependencies import get_token_header
from ..models import Dish, DishCreate, DishUpdate, DishRead, DishIngredient, Ingredient

router = APIRouter(
    prefix="/dishes",
    tags=["dishes"],
    # dependencies=[Depends(get_token_header)],
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
@router.get("/{dish_id}", response_model=DishRead)
def get_dish(dish_id: int, session: SessionDep) -> DishRead:
    # 查询 Dish
    dish = session.get(Dish, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    # 查询关联的 DishIngredient
    dish.ingredients = session.exec(
        select(DishIngredient).where(DishIngredient.dish_id == dish_id)
    ).all()

    # 如果需要加载 DishIngredient 的 Ingredient 信息，可以进一步查询
    for ingredient_relation in dish.ingredients:
        ingredient_relation.ingredient = session.get(
            Ingredient, ingredient_relation.ingredient_id
        )

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
    session.delete(dish.ingredients)  # 删除关联的 DishIngredient
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


# 新增菜品食材
@router.post("/{dish_id}/ingredients", response_model=Dish)
def create_dish_ingredient(
    dish_id: int, dish_ingredient: DishIngredient, session: SessionDep
):
    # 检查菜品是否存在
    dish = session.get(Dish, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    # 检查食材是否存在
    ingredient = session.get(Ingredient, dish_ingredient.ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    new_dish_ingredient = DishIngredient.model_validate(dish_ingredient)
    new_dish_ingredient.ingredient = ingredient
    new_dish_ingredient.dish = dish

    session.add(new_dish_ingredient)
    session.commit()
    session.refresh(dish)
    return dish


# 删除菜品食材
@router.delete("/{dish_id}/ingredients/{ingredient_id}", response_model=Dish)
def delete_dish_ingredient(dish_id: int, ingredient_id: int, session: SessionDep):
    # 检查菜品是否存在
    dish = session.get(Dish, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    # 查询 DishIngredient
    dish_ingredient = session.exec(
        select(DishIngredient).where(
            DishIngredient.dish_id == dish_id,
            DishIngredient.ingredient_id == ingredient_id,
        )
    ).first()

    if not dish_ingredient:
        raise HTTPException(status_code=404, detail="DishIngredient not found")

    session.delete(dish_ingredient)
    session.commit()
    session.refresh(dish)
    return dish


# 更新菜品食材
@router.patch("/{dish_id}/ingredients/{ingredient_id}", response_model=DishIngredient)
def update_dish_ingredients(
    dish_id: int, ingredients_id: int, session: SessionDep
):
    # 检查菜品是否存在
    dish = session.get(Dish, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    # 查询 DishIngredient
    dish_ingredient = session.exec(
        select(DishIngredient).where(
            DishIngredient.dish_id == dish_id,
            DishIngredient.ingredient_id == ingredients_id,
        )
    ).first()

    if not dish_ingredient:
        raise HTTPException(status_code=404, detail="DishIngredient not found")

    # 更新 DishIngredient
    dish_ingredient_data = dish_ingredient.model_dump(exclude_unset=True)
    dish_ingredient.sqlmodel_update(dish_ingredient_data)

    session.add(dish_ingredient)
    session.commit()
    session.refresh(dish_ingredient)
    return dish_ingredient