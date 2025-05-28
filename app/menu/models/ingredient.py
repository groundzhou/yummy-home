from datetime import datetime

from sqlmodel import SQLModel, Field

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


class IngredientCreate(IngredientBase):
    create_date: datetime  = Field(default_factory=datetime.now)


class IngredientUpdate(IngredientBase):
    name: str | None = None # type: ignore
    type: str | None = None  # type: ignore
    unit: str | None = None  # type: ignore
    process: str | None = None # type: ignore
    duration: int | None = None # type: ignore
    update_date: datetime | None = Field(default_factory=datetime.now)
