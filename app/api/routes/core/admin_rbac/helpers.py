"""Helper functions for RBAC operations."""

import json
from typing import Any, Optional
from sqlalchemy.orm import Session
from app.models.core.audit_log import AuditLog
from app.models.core.user import User


def log_audit(
    db: Session,
    actor_id: Optional[int],
    action: str,
    entity_type: str,
    entity_id: int,
    entity_name: Optional[str] = None,
    old_values: Optional[dict] = None,
    new_values: Optional[dict] = None,
    status: str = "SUCCESS",
    error_message: Optional[str] = None,
    ip_address: Optional[str] = None,
):
    """
    Log an audit event.
    
    Args:
        db: Database session
        actor_id: User ID performing the action
        action: Action type (CREATE, UPDATE, DELETE, ASSIGN_ROLE, etc.)
        entity_type: Entity type (USER, ROLE, PERMISSION)
        entity_id: Entity ID
        entity_name: Entity name for context
        old_values: Previous values (dict)
        new_values: New values (dict)
        status: Operation status (SUCCESS, FAILED)
        error_message: Error message if failed
        ip_address: Client IP address
    """
    audit = AuditLog(
        actor_id=actor_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        entity_name=entity_name,
        old_values=json.dumps(old_values) if old_values else None,
        new_values=json.dumps(new_values) if new_values else None,
        status=status,
        error_message=error_message,
        ip_address=ip_address,
    )
    db.add(audit)
    db.commit()


def get_changed_fields(old_obj: Any, update_data: dict) -> dict:
    """
    Extract only changed fields from update data.
    
    Args:
        old_obj: Original object
        update_data: New values dictionary
    
    Returns:
        Dictionary with only changed fields
    """
    changed = {}
    for key, new_value in update_data.items():
        if hasattr(old_obj, key):
            old_value = getattr(old_obj, key)
            if old_value != new_value:
                changed[key] = {"old": old_value, "new": new_value}
    return changed
