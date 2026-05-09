import enum
import uuid
from sqlalchemy import Column, SmallInteger, Text, Boolean, DateTime, ForeignKey, Enum as SAEnum, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class Severity(str, enum.Enum):
    info = "info"
    warning = "warning"
    critical = "critical"


class Source(str, enum.Enum):
    manual = "manual"
    tarteel_auto = "tarteel_auto"


class Annotation(Base):
    __tablename__ = "annotations"

    id           = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id      = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    category_id  = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    surah_number = Column(SmallInteger, nullable=False)
    ayah_number  = Column(SmallInteger, nullable=False)
    word_start   = Column(SmallInteger, nullable=False)
    word_end     = Column(SmallInteger, nullable=False)
    note_text    = Column(Text, nullable=True)
    severity     = Column(SAEnum(Severity), nullable=False, default=Severity.info)
    is_resolved  = Column(Boolean, nullable=False, default=False)
    source       = Column(SAEnum(Source), nullable=False, default=Source.manual)
    created_at   = Column(DateTime(timezone=True), server_default="now()")
    updated_at   = Column(DateTime(timezone=True), server_default="now()", onupdate="now()")

    __table_args__ = (
        CheckConstraint("word_end >= word_start", name="ck_word_end_gte_start"),
        CheckConstraint("word_start >= 1",        name="ck_word_start_positive"),
        CheckConstraint("surah_number BETWEEN 1 AND 114", name="ck_valid_surah"),
    )

    user     = relationship("User",     back_populates="annotations")
    category = relationship("Category", back_populates="annotations")
