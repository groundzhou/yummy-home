from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlmodel import Relationship, SQLModel, Field
from pydantic import BaseModel

# 仅用于类型检查
if TYPE_CHECKING:
    from .dish_ingredient import DishIngredient
    from .process import Process


# 原材料类
class IngredientBase(SQLModel):
    name: str = Field(index=True)
    type: int
    unit: str
    duration: int


class Ingredient(IngredientBase, table=True):
    __tablename__ = "ingredient"  # 指定表名

    id: int | None = Field(default=None, primary_key=True)
    create_date: datetime | None
    update_date: datetime | None = None
    dishes: List["DishIngredient"] = Relationship(back_populates="ingredient")


class IngredientCreate(IngredientBase):
    create_date: datetime | None = Field(default_factory=datetime.now)


class IngredientUpdate(IngredientBase):
    name: str | None = None
    type: str | None = None
    unit: str | None = None
    process: str | None = None
    duration: int | None = None
    update_date: datetime | None = Field(default_factory=datetime.now)


# 嵌套模型：Ingredient
class IngredientRead(BaseModel):
    id: int
    name: str
    type: int
    unit: str
    process: str
    duration: int
    process: List["Process"] = []  # 关联的处理过程列表

    class Config:
        from_attributes = True
