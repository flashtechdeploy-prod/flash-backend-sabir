"""Audit log schemas for API responses."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AuditLogBase(BaseModel):
    action: str
    entity_type: str
    entity_id: int
    entity_name: Optional[str] = None
    status: str = "SUCCESS"


class AuditLogOut(AuditLogBase):
    id: int
    actor_id: Optional[int] = None
    old_values: Optional[str] = None
    new_values: Optional[str] = None
    error_message: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
