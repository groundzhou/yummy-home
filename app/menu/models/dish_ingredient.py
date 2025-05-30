from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, List
from pydantic import BaseModel

# 仅用于类型检查
if TYPE_CHECKING:
    from .dish import Dish
    from .ingredient import Ingredient, IngredientRead
    from .process import Process


# DishIngredient关系表
class DishIngredient(SQLModel, table=True):  # 定义为数据库表
    __tablename__ = "dish_ingredient"  # 指定表名

    id: int | None = Field(default=None, primary_key=True)
    dish_id: int = Field(foreign_key="dish.id")
    ingredient_id: int = Field(foreign_key="ingredient.id")
    order: int  # 配料在菜品中的顺序
    quantity: int  # 所需要的量

    # 关系：关联 Dish 和 Ingredient
    dish: "Dish" = Relationship(back_populates="ingredients")
    ingredient: "Ingredient" = Relationship(back_populates="dishes")



# 嵌套模型：DishIngredient
class DishIngredientRead(BaseModel):
    id: int
    order: int
    quantity: int
    ingredient: "IngredientRead"  # 嵌套 Ingredient 信息
    
    class Config:
        from_attributes = True


