import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from app.services.annotation_service import (
    list_annotations,
    get_annotation,
    create_annotation,
    update_annotation,
    delete_annotation,
)
from app.schemas.annotation import AnnotationCreate, AnnotationUpdate
from app.models.annotation import Severity, Source


@pytest.fixture
def user_id():
    return uuid4()


@pytest.fixture
def mock_db():
    db = AsyncMock()
    return db


@pytest.mark.asyncio
async def test_create_annotation_validates_word_order():
    with pytest.raises(Exception):
        AnnotationCreate(
            surah_number=2,
            ayah_number=255,
            word_start=5,
            word_end=3,  # invalid: end < start
            category_id=uuid4(),
        )


@pytest.mark.asyncio
async def test_annotation_create_schema_valid():
    data = AnnotationCreate(
        surah_number=1,
        ayah_number=1,
        word_start=1,
        word_end=4,
        category_id=uuid4(),
        note_text="Test note",
        severity=Severity.warning,
    )
    assert data.word_end >= data.word_start
    assert data.surah_number == 1


@pytest.mark.asyncio
async def test_annotation_update_schema_partial():
    data = AnnotationUpdate(is_resolved=True)
    dumped = data.model_dump(exclude_none=True)
    assert dumped == {"is_resolved": True}
