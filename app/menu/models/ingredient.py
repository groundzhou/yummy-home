import datetime

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Ingredient(SQLModel, table=True):
    """食材"""

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    type: str
    process: str
    duration: datetime.timedelta
