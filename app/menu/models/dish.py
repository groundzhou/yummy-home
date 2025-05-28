from datetime import datetime
from ingredient import Ingredient
from sqlmodel import SQLModel, Field, Relationship
from typing import List

"""菜品类"""
class DishBase(SQLModel):
    name: str = Field(index=True)
    type: str
    ingredients: List[Ingredient] = Relationship(back_populates="ingredient")
    process: str
    duration: int


class Dish(DishBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    create_date: datetime
    update_date: datetime


class DishCreate(DishBase):
    create_date: datetime  = Field(default_factory=datetime.now)


class DishUpdate(DishBase):
    name: str | None = None # type: ignore
    type: str | None = None  # type: ignore
    ingredients: List[Ingredient] | None = None # type: ignore
    process: str | None = None # type: ignore
    duration: int | None = None # type: ignore
    update_date: datetime | None = Field(default_factory=datetime.now)


# DishIngredient 表：关系表，包含顺序字段
class DishIngredient(SQLModel, table=True):  # 定义为数据库表
    id: int = Field(default=None, primary_key=True)
    dish_id: int = Field(foreign_key="dish.id")
    ingredient_id: int = Field(foreign_key="ingredient.id")
    order: int  # 配料在菜品中的顺序
    quantity: int # 所需要的量

    # 关系：关联 Dish 和 Ingredient
    dish: Dish = Relationship(back_populates="ingredients")
    ingredient: Ingredient = Relationship(back_populates="dishes")
  
