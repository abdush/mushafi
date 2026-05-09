from fastapi import APIRouter, Depends
from uuid import UUID

from app.core.auth import get_current_user_id
import app.services.quran_service as svc

router = APIRouter()


@router.get("/page/{page_number}")
async def get_page(
    page_number: int,
    _: UUID = Depends(get_current_user_id),
):
    return await svc.get_page(page_number)


@router.get("/verse/{surah}/{ayah}")
async def get_verse(
    surah: int,
    ayah: int,
    _: UUID = Depends(get_current_user_id),
):
    return await svc.get_verse(surah, ayah)


@router.get("/word/{surah}/{ayah}/{position}")
async def get_word(
    surah: int,
    ayah: int,
    position: int,
    _: UUID = Depends(get_current_user_id),
):
    return await svc.get_word(surah, ayah, position)


@router.get("/audio/{chapter}")
async def get_audio(
    chapter: int,
    reciter_id: int = 7,
    _: UUID = Depends(get_current_user_id),
):
    return await svc.get_audio(chapter, reciter_id)


@router.get("/tafseer/{surah}/{ayah}")
async def get_tafseer(
    surah: int,
    ayah: int,
    tafseer_id: int = 169,
    _: UUID = Depends(get_current_user_id),
):
    return await svc.get_tafseer(surah, ayah, tafseer_id)
