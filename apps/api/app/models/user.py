import enum
import uuid
from sqlalchemy import Column, String, Integer, DateTime, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class AuthProvider(str, enum.Enum):
    email = "email"
    google = "google"
    quran_foundation = "quran_foundation"


class User(Base):
    __tablename__ = "users"

    id                  = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email               = Column(String(255), unique=True, nullable=False)
    display_name        = Column(String(100), nullable=True)
    auth_provider       = Column(SAEnum(AuthProvider), nullable=False, default=AuthProvider.email)
    auth_provider_id    = Column(String(255), nullable=True)
    preferred_reciter_id  = Column(Integer, nullable=True)
    preferred_tafseer_id  = Column(Integer, nullable=True)
    created_at          = Column(DateTime(timezone=True), server_default="now()")
    updated_at          = Column(DateTime(timezone=True), server_default="now()", onupdate="now()")

    annotations = relationship("Annotation", back_populates="user")
    categories  = relationship("Category",   back_populates="user")
