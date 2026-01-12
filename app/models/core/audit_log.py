"""Audit log model for tracking RBAC changes."""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class AuditLog(Base):
    """Audit log model to track all RBAC changes."""

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE, ASSIGN_ROLE, etc.
    entity_type = Column(String(50), nullable=False)  # USER, ROLE, PERMISSION
    entity_id = Column(Integer, nullable=False)
    entity_name = Column(String(255), nullable=True)
    old_values = Column(Text, nullable=True)  # JSON
    new_values = Column(Text, nullable=True)  # JSON
    status = Column(String(20), default="SUCCESS")  # SUCCESS, FAILED
    error_message = Column(Text, nullable=True)
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    actor = relationship("User", foreign_keys=[actor_id])

    def __repr__(self):
        return f"<AuditLog {self.action} on {self.entity_type} {self.entity_id}>"
