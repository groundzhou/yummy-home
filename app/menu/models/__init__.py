from .ingredient import *
from .dish_ingredient import *
from .dish import *


__all__ = [
    "Dish",
    "DishCreate",
    "DishUpdate",
    "DishRead",
    "Ingredient",
    "IngredientCreate",
    "IngredientUpdate",
    "IngredientRead",
    "DishIngredient",
    "DishIngredientRead",
]


# 调用 model_rebuild() 确保模型解析完成
IngredientRead.model_rebuild()
DishIngredientRead.model_rebuild()
DishRead.model_rebuild()