from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select

from app.core.db import SessionDep
from app.core.dependencies import get_token_header
from ..models import Ingredient, IngredientCreate, IngredientUpdate

router = APIRouter(
    prefix="/ingredients",
    tags=["ingredients"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


# 获取全部
@router.get("/", response_model=list[Ingredient])
def get_ingredients(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    ingredients = session.exec(select(Ingredient).offset(offset).limit(limit)).all()
    return ingredients


# 获取单个
@router.get("/{ingredient_id}", response_model=Ingredient)
def get_ingredient(ingredient_id: int, session: SessionDep) -> Ingredient:
    ingredient = session.get(Ingredient, ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient


# 新增
@router.post("/", response_model=Ingredient)
def create_ingredient(ingredient: IngredientCreate, session: SessionDep):
    db_ingredient = Ingredient.model_validate(ingredient)
    session.add(db_ingredient)
    session.commit()
    session.refresh(db_ingredient)
    return db_ingredient


# 删除
@router.delete("/{ingredient_id}")
def delete_ingredient(ingredient_id: int, session: SessionDep):
    ingredient = session.get(Ingredient, ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    session.delete(ingredient)
    session.commit()
    return {"ok": True}


# 更新
@router.patch("/{ingredient_id}", response_model=Ingredient)
def update_ingredient(
    ingredient_id: int, ingredient: IngredientUpdate, session: SessionDep
):
    ingredient_db = session.get(Ingredient, ingredient_id)
    if not ingredient_db:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    ingredient_data = ingredient.model_dump(exclude_unset=True)  # 排除默认值
    ingredient_db.sqlmodel_update(ingredient_data)
    session.add(ingredient_db)
    session.commit()
    session.refresh(ingredient_db)
    return ingredient_db
