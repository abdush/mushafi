import pytest
from uuid import uuid4

from app.schemas.category import CategoryCreate, CategoryUpdate


@pytest.mark.asyncio
async def test_category_create_schema_valid():
    data = CategoryCreate(
        label_ar="اختبار",
        label_en="Test",
        color_hex="#ff0000",
    )
    assert data.color_hex == "#ff0000"
    assert data.label_ar == "اختبار"


@pytest.mark.asyncio
async def test_category_create_invalid_color():
    with pytest.raises(Exception):
        CategoryCreate(
            label_ar="اختبار",
            color_hex="not-a-color",
        )


@pytest.mark.asyncio
async def test_category_update_partial():
    data = CategoryUpdate(color_hex="#00ff00")
    dumped = data.model_dump(exclude_none=True)
    assert dumped == {"color_hex": "#00ff00"}
