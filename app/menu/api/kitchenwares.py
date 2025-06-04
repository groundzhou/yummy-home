from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select

from app.core.db import SessionDep
from app.core.dependencies import get_token_header
from ..models import Kitchenware, KitchenwareCreate, KitchenwareUpdate, KitchenwareRead

router = APIRouter(
    prefix="/kitchenwares",
    tags=["kitchenwares"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


# 获取全部
@router.get("/", response_model=list[KitchenwareRead])
def get_kitchenwares(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    kitchenwares = session.exec(select(Kitchenware).offset(offset).limit(limit)).all()
    return kitchenwares


# 获取单个
@router.get("/{kitchenware_id}", response_model=KitchenwareRead)
def get_kitchenware(kitchenware_id: int, session: SessionDep) -> Kitchenware:
    kitchenware = session.get(Kitchenware, kitchenware_id)
    if not kitchenware:
        raise HTTPException(status_code=404, detail="Kitchenware not found")
    return kitchenware


# 新增
@router.post("/", response_model=KitchenwareRead)
def create_kitchenware(kitchenware: KitchenwareCreate, session: SessionDep):
    db_kitchenware = Kitchenware.model_validate(kitchenware)
    session.add(db_kitchenware)
    session.commit()
    session.refresh(db_kitchenware)
    return db_kitchenware


# 删除
@router.delete("/{kitchenware_id}")
def delete_kitchenware(kitchenware_id: int, session: SessionDep):
    kitchenware = session.get(Kitchenware, kitchenware_id)
    if not kitchenware:
        raise HTTPException(status_code=404, detail="Kitchenware not found")
    session.delete(kitchenware)
    session.commit()
    return {"ok": True}


# 更新
@router.patch("/{kitchenware_id}", response_model=KitchenwareRead)
def update_kitchenware(
    kitchenware_id: int, kitchenware: KitchenwareUpdate, session: SessionDep
):
    kitchenware_db = session.get(Kitchenware, kitchenware_id)
    if not kitchenware_db:
        raise HTTPException(status_code=404, detail="Kitchenware not found")
    kitchenware_data = kitchenware.model_dump(exclude_unset=True)  # 排除默认值
    kitchenware_db.sqlmodel_update(kitchenware_data)
    session.add(kitchenware_db)
    session.commit()
    session.refresh(kitchenware_db)
    return kitchenware_db
