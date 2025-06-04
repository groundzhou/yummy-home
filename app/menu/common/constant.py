from enum import Enum


# 食材类型
class IngredientType(Enum):
    SPICES = 1  # 调料
    SRAPLE = 2  # 主食
    VEGETABLE = 3  # 蔬菜
    MEAT = 4  # 肉类


# 菜品类型
class DishType(Enum):
    MAIN = 1  # 主食
    STIRFRY = 2  # 炒菜
    FRIED = 3  # 炸物
    STEAMED = 4  # 蒸菜
    BOILED = 5  # 水煮
    BARBECUE = 6  # 烧烤
    SOUP = 7  # 汤类


# 菜品状态
class DishStatus(Enum):
    DRAFT = 1  # 草稿
    PUBLISHED = 2  # 已发布
    DELETED = 3  # 已删除


# 流程类型
class ProcessType(Enum):
    DISH = 1
    INGREDIENT = 2