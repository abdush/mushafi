from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.user import AuthProvider


class UserResponse(BaseModel):
    model_config = {"from_attributes": True}

    id:                   UUID
    email:                str
    display_name:         str | None
    auth_provider:        AuthProvider
    preferred_reciter_id: int | None
    preferred_tafseer_id: int | None
    created_at:           datetime


class UserUpdate(BaseModel):
    display_name:         str | None = None
    preferred_reciter_id: int | None = None
    preferred_tafseer_id: int | None = None
