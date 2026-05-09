import httpx
from app.core.config import settings
from app.utils.cache import cache_get, cache_set


async def _fetch(path: str, params: dict | None = None) -> dict:
    headers = {}
    if settings.quran_foundation_api_key:
        headers["x-auth-token"] = settings.quran_foundation_api_key

    async with httpx.AsyncClient(base_url=settings.quran_foundation_api_base) as client:
        resp = await client.get(path, params=params, headers=headers, timeout=10.0)
        resp.raise_for_status()
        return resp.json()


async def get_page(page_number: int) -> dict:
    key = f"qf:page:{page_number}"
    cached = await cache_get(key)
    if cached:
        return cached
    data = await _fetch(f"/verses/by_page/{page_number}", {"words": "true", "word_fields": "text_uthmani,text_imlaei,transliteration,translation"})
    await cache_set(key, data)
    return data


async def get_verse(surah: int, ayah: int) -> dict:
    key = f"qf:verse:{surah}:{ayah}"
    cached = await cache_get(key)
    if cached:
        return cached
    data = await _fetch(f"/verses/by_key/{surah}:{ayah}", {"words": "true"})
    await cache_set(key, data)
    return data


async def get_word(surah: int, ayah: int, position: int) -> dict:
    key = f"qf:word:{surah}:{ayah}:{position}"
    cached = await cache_get(key)
    if cached:
        return cached
    data = await _fetch(f"/words/{surah}:{ayah}:{position}")
    await cache_set(key, data)
    return data


async def get_audio(chapter: int, reciter_id: int = 7) -> dict:
    key = f"qf:audio:{chapter}:{reciter_id}:segments"
    cached = await cache_get(key)
    if cached:
        return cached
    data = await _fetch(f"/chapter_recitations/{reciter_id}/{chapter}", {"segments": "true"})
    await cache_set(key, data)
    return data


async def get_tafseer(surah: int, ayah: int, tafseer_id: int = 169) -> dict:
    key = f"qf:tafseer:{tafseer_id}:{surah}:{ayah}"
    cached = await cache_get(key)
    if cached:
        return cached
    data = await _fetch(f"/tafsirs/{tafseer_id}/by_ayah/{surah}:{ayah}")
    await cache_set(key, data)
    return data
