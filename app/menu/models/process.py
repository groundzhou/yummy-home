from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlmodel import Relationship, SQLModel, Field
from pydantic import BaseModel

# 仅用于类型检查
if TYPE_CHECKING:
    from .dish_ingredient import DishIngredient


# 流程类
class ProcessBase(SQLModel):
    name: str = Field(index=True)
    duration: int  # 处理时间
    person_duration: int = 0  # 人工处理时间
    kitcherware_id: int | None
    order: int  # 处理顺序


class Process(ProcessBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    process_type: int  # 处理类型(1:食材处理, 2:菜品处理)
    reference_id: int  # 食材id或菜品id


class ProcessCreate(ProcessBase):
    process_type: int  # 处理类型(1:食材处理, 2:菜品处理)
    reference_id: int  # 食材id或菜品id


class ProcessUpdate(ProcessBase):
    name: str | None = None
    duration: int | None = None
    person_duration: int | None = None
    kitcherware_id: int | None = None
    order: int | None = None


class ProcessRead(BaseModel):
    name: str
    duration: int
    person_duration: int
    kitcherware_id: int | None
    order: int
