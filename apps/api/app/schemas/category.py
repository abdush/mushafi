from uuid import UUID
from pydantic import BaseModel, Field
from app.models.category import Scope


class CategorySummary(BaseModel):
    model_config = {"from_attributes": True}

    id:        UUID
    label_ar:  str
    label_en:  str | None
    color_hex: str


class CategoryCreate(BaseModel):
    parent_id:  UUID | None = None
    label_ar:   str = Field(min_length=1, max_length=100)
    label_en:   str | None = Field(default=None, max_length=100)
    color_hex:  str = Field(pattern=r"^#[0-9a-fA-F]{6}$")
    icon:       str | None = None
    sort_order: int = 0


class CategoryUpdate(BaseModel):
    label_ar:   str | None = Field(default=None, min_length=1, max_length=100)
    label_en:   str | None = None
    color_hex:  str | None = Field(default=None, pattern=r"^#[0-9a-fA-F]{6}$")
    icon:       str | None = None
    sort_order: int | None = None


class CategoryNode(BaseModel):
    model_config = {"from_attributes": True}

    id:               UUID
    label_ar:         str
    label_en:         str | None
    color_hex:        str
    icon:             str | None
    scope:            Scope
    children:         list["CategoryNode"] = []
    annotation_count: int = 0
