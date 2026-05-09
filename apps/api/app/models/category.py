import enum
import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class Scope(str, enum.Enum):
    global_ = "global"
    user = "user"


class Category(Base):
    __tablename__ = "categories"

    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id    = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    parent_id  = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    label_ar   = Column(String(100), nullable=False)
    label_en   = Column(String(100), nullable=True)
    color_hex  = Column(String(7), nullable=False)
    icon       = Column(String(50), nullable=True)
    scope      = Column(SAEnum(Scope), nullable=False, default=Scope.user)
    sort_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default="now()")
    updated_at = Column(DateTime(timezone=True), server_default="now()", onupdate="now()")

    user        = relationship("User",     back_populates="categories")
    parent      = relationship("Category", remote_side="Category.id", back_populates="children")
    children    = relationship("Category", back_populates="parent", order_by="Category.sort_order")
    annotations = relationship("Annotation", back_populates="category")
