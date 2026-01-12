from __future__ import annotations

import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_permission
from app.core.database import get_db
from app.core.security import get_password_hash
from app.models.core.rbac import Permission, Role
from app.models.core.user import User
from app.models.core.audit_log import AuditLog
from app.schemas.core.rbac import (
    AdminUserCreate,
    AdminUserOut,
    AdminUserUpdate,
    PermissionCreate,
    PermissionOut,
    PermissionUpdate,
    RoleCreate,
    RoleOut,
    RoleUpdate,
)
from app.api.routes.core.admin_rbac.helpers import log_audit, get_changed_fields

router = APIRouter()


@router.get("/permissions", response_model=list[PermissionOut])
def list_permissions(
    db: Session = Depends(get_db),
    _u: User = Depends(require_permission("rbac:admin")),
):
    return db.query(Permission).order_by(Permission.key.asc()).all()


@router.post("/permissions", response_model=PermissionOut, status_code=status.HTTP_201_CREATED)
def create_permission(
    payload: PermissionCreate,
    db: Session = Depends(get_db),
    _u: User = Depends(require_permission("rbac:admin")),
):
    key = payload.key.strip()
    exists = db.query(Permission).filter(Permission.key == key).first()
    if exists:
        raise HTTPException(status_code=400, detail="Permission key already exists")
    p = Permission(key=key, description=payload.description)
    db.add(p)
    db.commit()
    db.refresh(p)
    
    # Log audit
    log_audit(
        db=db,
        actor_id=_u.id,
        action="CREATE",
        entity_type="PERMISSION",
        entity_id=p.id,
        entity_name=p.key,
        new_values={"key": p.key, "description": p.description}
    )
    
    return p


@router.put("/permissions/{permission_id}", response_model=PermissionOut)
def update_permission(
    permission_id: int,
    payload: PermissionUpdate,
    db: Session = Depends(get_db),
    _u: User = Depends(require_permission("rbac:admin")),
):
    p = db.query(Permission).filter(Permission.id == permission_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Permission not found")

    old_values = {"key": p.key, "description": p.description}
    
    if payload.key is not None:
        new_key = payload.key.strip()
        other = db.query(Permission).filter(Permission.key == new_key, Permission.id != permission_id).first()
        if other:
            raise HTTPException(status_code=400, detail="Permission key already exists")
        p.key = new_key

    if payload.description is not None:
        p.description = payload.description

    db.commit()
    db.refresh(p)
    
    # Log audit
    new_values = {"key": p.key, "description": p.description}
    log_audit(
        db=db,
        actor_id=_u.id,
        action="UPDATE",
        entity_type="PERMISSION",
        entity_id=p.id,
        entity_name=p.key,
        old_values=old_values,
        new_values=new_values
    )
    
    return p


@router.delete("/permissions/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    _u: User = Depends(require_permission("rbac:admin")),
):
    p = db.query(Permission).filter(Permission.id == permission_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    # Check if permission is used by any role
    if p.roles:
        raise HTTPException(
            status_code=400,
            detail=f"Permission is assigned to {len(p.roles)} role(s). Remove it from all roles first."
        )
    
    permission_key = p.key
    db.delete(p)
    db.commit()
    
    # Log audit
    log_audit(
        db=db,
        actor_id=_u.id,
        action="DELETE",
        entity_type="PERMISSION",
        entity_id=permission_id,
        entity_name=permission_key,
        old_values={"key": permission_key}
    )
    
    return None


@router.get("/roles", response_model=list[RoleOut])
def list_roles(
    db: Session = Depends(get_db),
    _u: User = Depends(require_permission("rbac:admin")),
):
    return db.query(Role).order_by(Role.name.asc()).all()


@router.post("/roles", response_model=RoleOut, status_code=status.HTTP_201_CREATED)
def create_role(
    payload: RoleCreate,
    db: Session = Depends(get_db),
    _u: User = Depends(require_permission("rbac:admin")),
):
    name = payload.name.strip()
    exists = db.query(Role).filter(Role.name == name).first()
    if exists:
        raise HTTPException(status_code=400, detail="Role name already exists")

    perms: list[Permission] = []
    if payload.permission_keys:
        perms = db.query(Permission).filter(Permission.key.in_([k.strip() for k in payload.permission_keys])).all()

    r = Role(name=name, description=payload.description, is_system=False)
    r.permissions = perms
    db.add(r)
    db.commit()
    db.refresh(r)
    
    # Log audit
    log_audit(
        db=db,
        actor_id=_u.id,
        action="CREATE",
        entity_type="ROLE",
        entity_id=r.id,
        entity_name=r.name,
        new_values={
            "name": r.name,
            "description": r.description,
            "permission_keys": [p.key for p in r.permissions]
        }
    )
    
    return r


@router.put("/roles/{role_id}", response_model=RoleOut)
def update_role(
    role_id: int,
    payload: RoleUpdate,
    db: Session = Depends(get_db),
    _u: User = Depends(require_permission("rbac:admin")),
):
    r = db.query(Role).filter(Role.id == role_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Role not found")

    old_values = {
        "name": r.name,
        "description": r.description,
        "permission_keys": [p.key for p in r.permissions]
    }

    if payload.name is not None:
        new_name = payload.name.strip()
        other = db.query(Role).filter(Role.name == new_name, Role.id != role_id).first()
        if other:
            raise HTTPException(status_code=400, detail="Role name already exists")
        r.name = new_name

    if payload.description is not None:
        r.description = payload.description

    if payload.permission_keys is not None:
        keys = [k.strip() for k in payload.permission_keys]
        perms = db.query(Permission).filter(Permission.key.in_(keys)).all() if keys else []
        r.permissions = perms

    db.commit()
    db.refresh(r)
    
    # Log audit
    new_values = {
        "name": r.name,
        "description": r.description,
        "permission_keys": [p.key for p in r.permissions]
    }
    log_audit(
        db=db,
        actor_id=_u.id,
        action="UPDATE",
        entity_type="ROLE",
        entity_id=r.id,
        entity_name=r.name,
        old_values=old_values,
        new_values=new_values
    )
    
    return r


@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    _u: User = Depends(require_permission("rbac:admin")),
):
    r = db.query(Role).filter(Role.id == role_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Role not found")
    if r.is_system:
        raise HTTPException(status_code=400, detail="System roles cannot be deleted")
    
    role_name = r.name
    db.delete(r)
    db.commit()
    
    # Log audit
    log_audit(
        db=db,
        actor_id=_u.id,
        action="DELETE",
        entity_type="ROLE",
        entity_id=role_id,
        entity_name=role_name,
        old_values={"name": role_name}
    )
    
    return None


@router.get("/users", response_model=list[AdminUserOut])
def list_users(
    db: Session = Depends(get_db),
    _u: User = Depends(require_permission("rbac:admin")),
):
    return db.query(User).order_by(User.id.asc()).all()


@router.post("/users", response_model=AdminUserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: AdminUserCreate,
    db: Session = Depends(get_db),
    _u: User = Depends(require_permission("rbac:admin")),
):
    existing = db.query(User).filter((User.email == payload.email) | (User.username == payload.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this email or username already exists")

    u = User(
        email=payload.email,
        username=payload.username,
        full_name=payload.full_name,
        hashed_password=get_password_hash(payload.password),
        is_active=payload.is_active,
        is_superuser=payload.is_superuser,
    )

    if payload.role_ids:
        roles = db.query(Role).filter(Role.id.in_(payload.role_ids)).all()
        u.roles = roles  # type: ignore[attr-defined]

    db.add(u)
    db.commit()
    db.refresh(u)
    
    # Log audit
    log_audit(
        db=db,
        actor_id=_u.id,
        action="CREATE",
        entity_type="USER",
        entity_id=u.id,
        entity_name=u.username,
        new_values={
            "email": u.email,
            "username": u.username,
            "full_name": u.full_name,
            "is_active": u.is_active,
            "is_superuser": u.is_superuser,
            "role_ids": [r.id for r in u.roles]
        }
    )
    
    return u


@router.put("/users/{user_id}", response_model=AdminUserOut)
def update_user(
    user_id: int,
    payload: AdminUserUpdate,
    db: Session = Depends(get_db),
    _u: User = Depends(require_permission("rbac:admin")),
):
    u = db.query(User).filter(User.id == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="User not found")

    old_values = {
        "email": u.email,
        "username": u.username,
        "full_name": u.full_name,
        "is_active": u.is_active,
        "is_superuser": u.is_superuser,
        "role_ids": [r.id for r in u.roles]
    }

    if payload.email is not None:
        u.email = payload.email
    if payload.username is not None:
        u.username = payload.username
    if payload.full_name is not None:
        u.full_name = payload.full_name
    if payload.is_active is not None:
        u.is_active = payload.is_active
    if payload.is_superuser is not None:
        u.is_superuser = payload.is_superuser
    if payload.password is not None:
        u.hashed_password = get_password_hash(payload.password)

    if payload.role_ids is not None:
        roles = db.query(Role).filter(Role.id.in_(payload.role_ids)).all() if payload.role_ids else []
        u.roles = roles  # type: ignore[attr-defined]

    db.commit()
    db.refresh(u)
    
    # Log audit
    new_values = {
        "email": u.email,
        "username": u.username,
        "full_name": u.full_name,
        "is_active": u.is_active,
        "is_superuser": u.is_superuser,
        "role_ids": [r.id for r in u.roles]
    }
    log_audit(
        db=db,
        actor_id=_u.id,
        action="UPDATE",
        entity_type="USER",
        entity_id=u.id,
        entity_name=u.username,
        old_values=old_values,
        new_values=new_values
    )
    
    return u


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _u: User = Depends(require_permission("rbac:admin")),
):
    u = db.query(User).filter(User.id == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    
    username = u.username
    db.delete(u)
    db.commit()
    
    # Log audit
    log_audit(
        db=db,
        actor_id=_u.id,
        action="DELETE",
        entity_type="USER",
        entity_id=user_id,
        entity_name=username,
        old_values={"username": username}
    )
    
    return None


# --- Audit Logs ---

@router.get("/audit-logs", response_model=list)
def list_audit_logs(
    skip: int = 0,
    limit: int = 100,
    entity_type: str = None,
    action: str = None,
    db: Session = Depends(get_db),
    _u: User = Depends(require_permission("rbac:admin")),
):
    """Get audit logs (superuser only)."""
    query = db.query(AuditLog)
    
    if entity_type:
        query = query.filter(AuditLog.entity_type == entity_type)
    if action:
        query = query.filter(AuditLog.action == action)
    
    logs = query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()
    return logs


@router.get("/audit-logs/{entity_type}/{entity_id}", response_model=list)
def get_entity_audit_logs(
    entity_type: str,
    entity_id: int,
    db: Session = Depends(get_db),
    _u: User = Depends(require_permission("rbac:admin")),
):
    """Get audit logs for a specific entity."""
    logs = db.query(AuditLog).filter(
        AuditLog.entity_type == entity_type,
        AuditLog.entity_id == entity_id
    ).order_by(AuditLog.created_at.desc()).all()
    return logs
