from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# check_same_thread=False可以让 FastAPI 在不同线程中使用同一个 SQLite 数据库
connect_args = {"check_same_thread": False} 
engine = create_engine(sqlite_url, connect_args=connect_args)


# 创建数据库表
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# 为每个请求提供一个新的Session
def get_session():
    with Session(engine) as session:
        yield session

# 创建一个 Annotated 的依赖项 SessionDep 来简化其他也会用到此依赖的代码
SessionDep = Annotated[Session, Depends(get_session)]
