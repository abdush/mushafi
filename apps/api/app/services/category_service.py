from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.models.category import Category, Scope
from app.schemas.category import CategoryCreate, CategoryUpdate


async def get_category_tree(db: AsyncSession, user_id: UUID) -> list[Category]:
    q = (
        select(Category)
        .where(
            (Category.scope == Scope.global_) | (Category.user_id == user_id),
            Category.parent_id == None,
        )
        .options(selectinload(Category.children).selectinload(Category.children))
        .order_by(Category.sort_order)
    )
    result = await db.execute(q)
    return list(result.scalars().all())


async def get_category(db: AsyncSession, category_id: UUID) -> Category:
    category = await db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


async def create_category(db: AsyncSession, user_id: UUID, data: CategoryCreate) -> Category:
    if data.parent_id:
        parent = await db.get(Category, data.parent_id)
        if not parent:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parent category not found")

    category = Category(
        user_id=user_id,
        scope=Scope.user,
        **data.model_dump(),
    )
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def update_category(
    db: AsyncSession, user_id: UUID, category_id: UUID, data: CategoryUpdate
) -> Category:
    category = await get_category(db, category_id)
    if category.scope == Scope.global_:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot modify global categories")
    if category.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your category")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(category, field, value)
    await db.commit()
    await db.refresh(category)
    return category


async def delete_category(db: AsyncSession, user_id: UUID, category_id: UUID) -> None:
    category = await get_category(db, category_id)
    if category.scope == Scope.global_:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete global categories")
    if category.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your category")
    if category.annotations:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete category with existing annotations",
        )
    await db.delete(category)
    await db.commit()
