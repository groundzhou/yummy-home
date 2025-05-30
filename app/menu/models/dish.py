from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel

# 仅用于类型检查
if TYPE_CHECKING:
    from .dish_ingredient import DishIngredient, DishIngredientRead


# 菜品实体
class DishBase(SQLModel):
    name: str = Field(index=True)
    type: int
    process: str
    duration: int


class Dish(DishBase, table=True):
    __tablename__ = "dish"  # 指定表名

    id: int | None = Field(default=None, primary_key=True)
    create_date: datetime | None
    update_date: datetime | None = None
    ingredients: List["DishIngredient"] = Relationship(back_populates="dish")


class DishCreate(DishBase):
    create_date: datetime | None = Field(default_factory=datetime.now)


class DishUpdate(DishBase):
    name: str | None = None
    type: str | None = None
    process: str | None = None
    duration: int | None = None
    update_date: datetime | None = Field(default_factory=datetime.now)


# 修改 Dish 模型
class DishRead(BaseModel):
    id: int
    name: str
    type: int
    process: str
    duration: int
    ingredients: List["DishIngredientRead"]  # 嵌套 DishIngredient 信息
    create_date: datetime | None
    update_date: datetime | None

    class Config:
        from_attributes = True
