from datetime import datetime
from typing import List

from sqlmodel import Relationship, SQLModel, Field


"""原材料类"""
class IngredientBase(SQLModel):
    name: str = Field(index=True)
    type: int
    unit: str 
    process: str
    duration: int


class Ingredient(IngredientBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    create_date: datetime
    update_date: datetime

    dishes: List["DishIngredient"] = Relationship(back_populates="ingredient")


class IngredientCreate(IngredientBase):
    create_date: datetime  = Field(default_factory=datetime.now)


class IngredientUpdate(IngredientBase):
    name: str | None = None
    type: str | None = None 
    unit: str | None = None 
    process: str | None = None
    duration: int | None = None
    update_date: datetime | None = Field(default_factory=datetime.now)
