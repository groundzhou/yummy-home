from sqlmodel import SQLModel, Field
from pydantic import BaseModel


# 厨具类
class KitchenwareBase(SQLModel):
    name: str
    number: int = 0  # 数量


class Kitchenware(KitchenwareBase, table=True):
    __tablename__ = "kitchenware"  # 指定表名

    id: int | None = Field(default=None, primary_key=True)


class KitchenwareCreate(KitchenwareBase):
    pass


class KitchenwareUpdate(KitchenwareBase):
    name: str | None = None
    number: int | None = None


# 嵌套模型：Kitchenware
class KitchenwareRead(BaseModel):
    id: int
    name: str
    number: int

    class Config:
        from_attributes = True
