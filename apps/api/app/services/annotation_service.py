from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.models.annotation import Annotation
from app.models.category import Category
from app.schemas.annotation import AnnotationCreate, AnnotationUpdate


async def list_annotations(
    db: AsyncSession,
    user_id: UUID,
    surah_number: int | None = None,
    ayah_number: int | None = None,
    category_id: UUID | None = None,
    is_resolved: bool | None = None,
) -> list[Annotation]:
    q = (
        select(Annotation)
        .where(Annotation.user_id == user_id)
        .options(selectinload(Annotation.category))
    )
    if surah_number is not None:
        q = q.where(Annotation.surah_number == surah_number)
    if ayah_number is not None:
        q = q.where(Annotation.ayah_number == ayah_number)
    if category_id is not None:
        q = q.where(Annotation.category_id == category_id)
    if is_resolved is not None:
        q = q.where(Annotation.is_resolved == is_resolved)
    result = await db.execute(q)
    return list(result.scalars().all())


async def get_annotation(db: AsyncSession, user_id: UUID, annotation_id: UUID) -> Annotation:
    q = (
        select(Annotation)
        .where(Annotation.id == annotation_id, Annotation.user_id == user_id)
        .options(selectinload(Annotation.category))
    )
    result = await db.execute(q)
    annotation = result.scalar_one_or_none()
    if not annotation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Annotation not found")
    return annotation


async def create_annotation(db: AsyncSession, user_id: UUID, data: AnnotationCreate) -> Annotation:
    category = await db.get(Category, data.category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    annotation = Annotation(
        user_id=user_id,
        **data.model_dump(),
    )
    db.add(annotation)
    await db.commit()
    await db.refresh(annotation)
    return await get_annotation(db, user_id, annotation.id)


async def update_annotation(
    db: AsyncSession, user_id: UUID, annotation_id: UUID, data: AnnotationUpdate
) -> Annotation:
    annotation = await get_annotation(db, user_id, annotation_id)
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(annotation, field, value)
    await db.commit()
    return await get_annotation(db, user_id, annotation_id)


async def delete_annotation(db: AsyncSession, user_id: UUID, annotation_id: UUID) -> None:
    annotation = await get_annotation(db, user_id, annotation_id)
    await db.delete(annotation)
    await db.commit()


async def search_annotations(db: AsyncSession, user_id: UUID, q: str) -> list[Annotation]:
    stmt = (
        select(Annotation)
        .where(
            Annotation.user_id == user_id,
            Annotation.note_text.ilike(f"%{q}%"),
        )
        .options(selectinload(Annotation.category))
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_stats(db: AsyncSession, user_id: UUID) -> dict:
    total_q = await db.execute(select(func.count()).where(Annotation.user_id == user_id))
    total = total_q.scalar()

    resolved_q = await db.execute(
        select(func.count()).where(Annotation.user_id == user_id, Annotation.is_resolved == True)
    )
    resolved = resolved_q.scalar()

    return {
        "total": total,
        "resolved": resolved,
        "unresolved": total - resolved,
        "by_severity": {},
        "by_category": {},
    }
