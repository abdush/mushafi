from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_current_user_id
from app.core.database import get_db
from app.schemas.annotation import AnnotationCreate, AnnotationUpdate, AnnotationResponse, AnnotationStats
import app.services.annotation_service as svc

router = APIRouter()


@router.get("", response_model=list[AnnotationResponse])
async def list_annotations(
    surah_number: int | None = None,
    ayah_number: int | None = None,
    category_id: UUID | None = None,
    is_resolved: bool | None = None,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await svc.list_annotations(db, user_id, surah_number, ayah_number, category_id, is_resolved)


@router.get("/search", response_model=list[AnnotationResponse])
async def search_annotations(
    q: str = Query(min_length=1),
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await svc.search_annotations(db, user_id, q)


@router.get("/stats", response_model=AnnotationStats)
async def get_stats(
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await svc.get_stats(db, user_id)


@router.get("/{annotation_id}", response_model=AnnotationResponse)
async def get_annotation(
    annotation_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await svc.get_annotation(db, user_id, annotation_id)


@router.post("", response_model=AnnotationResponse, status_code=201)
async def create_annotation(
    data: AnnotationCreate,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await svc.create_annotation(db, user_id, data)


@router.patch("/{annotation_id}", response_model=AnnotationResponse)
async def update_annotation(
    annotation_id: UUID,
    data: AnnotationUpdate,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await svc.update_annotation(db, user_id, annotation_id, data)


@router.delete("/{annotation_id}", status_code=204)
async def delete_annotation(
    annotation_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    await svc.delete_annotation(db, user_id, annotation_id)
