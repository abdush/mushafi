from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user_id
from app.core.database import get_db
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryNode
import app.services.category_service as svc

router = APIRouter()


@router.get("", response_model=list[CategoryNode])
async def get_category_tree(
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await svc.get_category_tree(db, user_id)


@router.post("", response_model=CategoryNode, status_code=201)
async def create_category(
    data: CategoryCreate,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await svc.create_category(db, user_id, data)


@router.patch("/{category_id}", response_model=CategoryNode)
async def update_category(
    category_id: UUID,
    data: CategoryUpdate,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await svc.update_category(db, user_id, category_id, data)


@router.delete("/{category_id}", status_code=204)
async def delete_category(
    category_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    await svc.delete_category(db, user_id, category_id)
