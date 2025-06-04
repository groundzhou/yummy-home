from .ingredient import *
from .dish_ingredient import *
from .dish import *
from .kitchenware import *
from .process import *


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
    "KitchenWare",
    "KitchenwareCreate",
    "KitchenwareUpdate",
    "KitchenWareRead",
    "Process",
    "ProcessCreate",
    "ProcessUpdate",
    "ProcessRead"
]


# 调用 model_rebuild() 确保模型解析完成
KitchenwareRead.model_rebuild()
IngredientRead.model_rebuild()
DishIngredientRead.model_rebuild()
DishRead.model_rebuild()
