from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, model_validator
from app.models.annotation import Severity, Source
from app.schemas.category import CategorySummary


class AnnotationCreate(BaseModel):
    surah_number: int = Field(ge=1, le=114)
    ayah_number:  int = Field(ge=1)
    word_start:   int = Field(ge=1)
    word_end:     int = Field(ge=1)
    category_id:  UUID
    note_text:    str | None = None
    severity:     Severity = Severity.info

    @model_validator(mode="after")
    def word_end_gte_start(self):
        if self.word_end < self.word_start:
            raise ValueError("word_end must be >= word_start")
        return self


class AnnotationUpdate(BaseModel):
    category_id: UUID | None = None
    note_text:   str | None = None
    severity:    Severity | None = None
    is_resolved: bool | None = None


class AnnotationResponse(BaseModel):
    model_config = {"from_attributes": True}

    id:           UUID
    surah_number: int
    ayah_number:  int
    word_start:   int
    word_end:     int
    category:     CategorySummary
    note_text:    str | None
    severity:     Severity
    is_resolved:  bool
    source:       Source
    created_at:   datetime
    updated_at:   datetime


class AnnotationStats(BaseModel):
    total: int
    resolved: int
    unresolved: int
    by_severity: dict[str, int]
    by_category: dict[str, int]
