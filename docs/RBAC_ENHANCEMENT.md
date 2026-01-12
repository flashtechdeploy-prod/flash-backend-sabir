# Enhanced RBAC System Documentation

## Overview
Your FastAPI backend now has a complete, production-ready Role-Based Access Control (RBAC) system with audit logging, permission management, and comprehensive CRUD operations for Users, Roles, and Permissions.

## New Features Added

### 1. **Audit Logging**
- Automatic tracking of all RBAC changes
- Records actor (user performing action), action type, entity type, old/new values
- Timestamps and status tracking
- Error message logging for failed operations

**Model**: [app/models/core/audit_log.py](app/models/core/audit_log.py)
**Schema**: [app/schemas/core/audit_log.py](app/schemas/core/audit_log.py)

### 2. **Enhanced Permission Management**
- Added UPDATE endpoint for permissions
- Added DELETE endpoint for permissions (with validation to prevent deletion if in use)
- Permission update/delete includes audit logging

### 3. **Complete CRUD Operations**

#### Users
| Method | Endpoint | Description | Permission |
|--------|----------|-------------|-----------|
| GET | `/admin/users` | List all users | rbac:admin |
| GET | `/admin/users/{user_id}` | Get user by ID | rbac:admin |
| POST | `/admin/users` | Create new user | rbac:admin |
| PUT | `/admin/users/{user_id}` | Update user | rbac:admin |
| DELETE | `/admin/users/{user_id}` | Delete user | rbac:admin |

#### Roles
| Method | Endpoint | Description | Permission |
|--------|----------|-------------|-----------|
| GET | `/admin/roles` | List all roles | rbac:admin |
| POST | `/admin/roles` | Create new role | rbac:admin |
| PUT | `/admin/roles/{role_id}` | Update role | rbac:admin |
| DELETE | `/admin/roles/{role_id}` | Delete role | rbac:admin |

#### Permissions
| Method | Endpoint | Description | Permission |
|--------|----------|-------------|-----------|
| GET | `/admin/permissions` | List all permissions | rbac:admin |
| POST | `/admin/permissions` | Create new permission | rbac:admin |
| PUT | `/admin/permissions/{permission_id}` | Update permission | rbac:admin |
| DELETE | `/admin/permissions/{permission_id}` | Delete permission | rbac:admin |

#### Audit Logs
| Method | Endpoint | Description | Permission |
|--------|----------|-------------|-----------|
| GET | `/admin/audit-logs` | List audit logs (with filters) | rbac:admin |
| GET | `/admin/audit-logs/{entity_type}/{entity_id}` | Get logs for specific entity | rbac:admin |

## API Examples

### Create a New User
```bash
curl -X POST http://localhost:8000/admin/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "email": "user@example.com",
    "username": "john_doe",
    "full_name": "John Doe",
    "password": "secure_password",
    "is_active": true,
    "is_superuser": false,
    "role_ids": [1, 2]
  }'
```

### Create a New Role
```bash
curl -X POST http://localhost:8000/admin/roles \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "name": "Manager",
    "description": "Manager role",
    "permission_keys": ["users:read", "users:create", "reports:view"]
  }'
```

### Create a New Permission
```bash
curl -X POST http://localhost:8000/admin/permissions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "key": "users:delete",
    "description": "Delete users"
  }'
```

### Update Permission
```bash
curl -X PUT http://localhost:8000/admin/permissions/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "description": "Updated description"
  }'
```

### Delete Permission
```bash
curl -X DELETE http://localhost:8000/admin/permissions/1 \
  -H "Authorization: Bearer {token}"
```

### View Audit Logs
```bash
# Get all audit logs
curl -X GET http://localhost:8000/admin/audit-logs?skip=0&limit=50 \
  -H "Authorization: Bearer {token}"

# Filter by entity type
curl -X GET http://localhost:8000/admin/audit-logs?entity_type=USER \
  -H "Authorization: Bearer {token}"

# Filter by action
curl -X GET http://localhost:8000/admin/audit-logs?action=CREATE \
  -H "Authorization: Bearer {token}"

# Get logs for specific entity
curl -X GET http://localhost:8000/admin/audit-logs/USER/5 \
  -H "Authorization: Bearer {token}"
```

## Files Created/Modified

### New Files
- [app/models/core/audit_log.py](app/models/core/audit_log.py) - AuditLog model
- [app/schemas/core/audit_log.py](app/schemas/core/audit_log.py) - AuditLog schemas
- [app/api/routes/core/admin_rbac/helpers.py](app/api/routes/core/admin_rbac/helpers.py) - Audit logging helpers
- [alembic/versions/add_audit_log_table.py](alembic/versions/add_audit_log_table.py) - Database migration

### Modified Files
- [app/api/routes/core/admin_rbac/router.py](app/api/routes/core/admin_rbac/router.py)
  - Added audit logging to all CRUD operations
  - Added permission UPDATE endpoint
  - Added permission DELETE endpoint
  - Added audit log viewing endpoints
- [app/schemas/core/rbac.py](app/schemas/core/rbac.py)
  - Added PermissionUpdate schema
- [app/models/__init__.py](app/models/__init__.py)
  - Added AuditLog model export

## Database Schema

### audit_logs table
```sql
CREATE TABLE audit_logs (
  id INTEGER PRIMARY KEY,
  actor_id INTEGER FOREIGN KEY,
  action VARCHAR(50) NOT NULL,           -- CREATE, UPDATE, DELETE, ASSIGN_ROLE
  entity_type VARCHAR(50) NOT NULL,      -- USER, ROLE, PERMISSION
  entity_id INTEGER NOT NULL,
  entity_name VARCHAR(255),
  old_values TEXT,                       -- JSON format
  new_values TEXT,                       -- JSON format
  status VARCHAR(20) DEFAULT 'SUCCESS',  -- SUCCESS, FAILED
  error_message TEXT,
  ip_address VARCHAR(50),
  created_at TIMESTAMP WITH TIMEZONE DEFAULT NOW()
);
```

## Helper Functions

### `log_audit()`
Logs an audit event to the database.

```python
log_audit(
    db=session,
    actor_id=user_id,
    action="CREATE",
    entity_type="USER",
    entity_id=new_user_id,
    entity_name="john_doe",
    new_values={"email": "john@example.com"},
)
```

### `get_changed_fields()`
Extracts only the fields that changed between old and new values.

```python
changed = get_changed_fields(old_user, {"name": "New Name", "email": "old@email.com"})
# Returns: {"name": {"old": "Old Name", "new": "New Name"}}
```

## Security Features

1. **Permission-based access control**: All endpoints require `rbac:admin` permission
2. **Superuser flag**: Support for super admin users
3. **Audit trail**: Complete history of all changes
4. **Password hashing**: Secure password storage using bcrypt
5. **Unique constraints**: Email and username must be unique
6. **Validation**: 
   - Cannot delete system roles
   - Cannot delete permissions in use
   - Prevents duplicate role/permission names

## Migration Steps

1. Run the audit log migration:
   ```bash
   alembic upgrade add_audit_log_table
   ```

2. Restart your FastAPI server

3. The audit log table will be created automatically

## Future Enhancements

- [ ] Add rate limiting to prevent abuse
- [ ] Add IP-based access logging
- [ ] Add role hierarchy/nesting
- [ ] Add time-based access controls
- [ ] Add permission inheritance
- [ ] Add audit log retention policies
- [ ] Add email notifications for critical changes
