# 🏗️ RBAC System Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                          FastAPI Application                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    API Routes Layer                         │ │
│  │                                                             │ │
│  │  /admin/users          /admin/roles       /admin/perms     │ │
│  │  ├─ GET    (list)      ├─ GET    (list)   ├─ GET  (list)   │ │
│  │  ├─ POST   (create)    ├─ POST   (create) ├─ POST (create) │ │
│  │  ├─ PUT    (update)    ├─ PUT    (update) ├─ PUT  (update) │ │
│  │  └─ DELETE (delete)    └─ DELETE (delete) └─ DEL  (delete) │ │
│  │                                                             │ │
│  │  /admin/audit-logs (LIST, FILTER)  ⭐ NEW                 │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ↓                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                   Router Functions                          │ │
│  │                                                             │ │
│  │  create_user()      create_role()      create_permission() │ │
│  │  update_user()      update_role()      update_permission() │ │
│  │  delete_user()      delete_role()      delete_permission() │ │
│  │  list_users()       list_roles()       list_permissions()  │ │
│  │                                                             │ │
│  │  list_audit_logs()  get_entity_audit_logs()               │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ↓                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                  Helper Functions                           │ │
│  │                                                             │ │
│  │  log_audit()          → Record changes to audit_logs       │ │
│  │  get_changed_fields() → Extract changed fields            │ │
│  │  require_permission() → Check rbac:admin permission       │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ↓                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                   Database Layer (SQLAlchemy)              │ │
│  │                                                             │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │ │
│  │  │    users     │  │    roles     │  │  permissions     │ │ │
│  │  ├──────────────┤  ├──────────────┤  ├──────────────────┤ │ │
│  │  │ id (PK)      │  │ id (PK)      │  │ id (PK)          │ │ │
│  │  │ email        │  │ name         │  │ key              │ │ │
│  │  │ username     │  │ description  │  │ description      │ │ │
│  │  │ password     │  │ is_system    │  └──────────────────┘ │ │
│  │  │ full_name    │  │              │                       │ │
│  │  │ is_active    │  │              │                       │ │
│  │  │ is_superuser │  └──────────────┘                       │ │
│  │  │ roles (M2M)  │                                          │ │
│  │  └──────────────┘                                          │ │
│  │         ↑                                                   │ │
│  │         │ M2M                                               │ │
│  │         ├─────────────────────────────────────────┐        │ │
│  │         │                                         │        │ │
│  │  ┌──────────────────────┐        ┌──────────────┐ │        │ │
│  │  │   user_roles         │        │role_permis   │ │        │ │
│  │  │  (Junction Table)    │        │  (Junction)  │ │        │ │
│  │  ├──────────────────────┤        ├──────────────┤ │        │ │
│  │  │ user_id (FK)         │        │ role_id (FK) │ │        │ │
│  │  │ role_id (FK)         │        │ perm_id (FK) │ │        │ │
│  │  └──────────────────────┘        └──────────────┘ │        │ │
│  │                                          │          │        │ │
│  │                                          └──────────┘        │ │
│  │                                                              │ │
│  │  ┌────────────────────────────────────────────────────────┐ │ │
│  │  │              audit_logs (NEW)                           │ │ │
│  │  ├────────────────────────────────────────────────────────┤ │ │
│  │  │ id                                                      │ │ │
│  │  │ actor_id (FK → users)                                  │ │ │
│  │  │ action (CREATE, UPDATE, DELETE)                        │ │ │
│  │  │ entity_type (USER, ROLE, PERMISSION)                   │ │ │
│  │  │ entity_id                                              │ │ │
│  │  │ entity_name                                            │ │ │
│  │  │ old_values (JSON)                                      │ │ │
│  │  │ new_values (JSON)                                      │ │ │
│  │  │ status (SUCCESS, FAILED)                               │ │ │
│  │  │ error_message                                          │ │ │
│  │  │ ip_address                                             │ │ │
│  │  │ created_at (TIMESTAMP)                                 │ │ │
│  │  └────────────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

### Creating a User Flow
```
┌──────────────┐
│ HTTP Request │  POST /admin/users
│  with Token  │
└──────────────┘
       ↓
┌──────────────────────────┐
│ Authentication Check     │
│ (get_current_user)       │
└──────────────────────────┘
       ↓
┌──────────────────────────┐
│ Permission Check         │
│ (require_permission)     │
│ Checks: rbac:admin       │
└──────────────────────────┘
       ↓
┌──────────────────────────┐
│ Input Validation         │
│ - Check email unique     │
│ - Check username unique  │
│ - Validate password      │
└──────────────────────────┘
       ↓
┌──────────────────────────┐
│ Hash Password            │
│ (bcrypt)                 │
└──────────────────────────┘
       ↓
┌──────────────────────────┐
│ Create User in Database  │
│ - Insert into users      │
│ - Assign roles (if any)  │
└──────────────────────────┘
       ↓
┌──────────────────────────┐
│ Log Audit Event          │
│ log_audit():             │
│ - action: CREATE         │
│ - entity_type: USER      │
│ - new_values: {...}      │
└──────────────────────────┘
       ↓
┌──────────────────────────┐
│ Return Response (201)    │
│ User data               │
└──────────────────────────┘
```

### Updating a User with Audit Flow
```
┌──────────────┐
│ HTTP Request │  PUT /admin/users/5
└──────────────┘
       ↓
┌──────────────────────────┐
│ Authentication & Auth    │
│ - Get current user       │
│ - Check rbac:admin       │
└──────────────────────────┘
       ↓
┌──────────────────────────┐
│ Fetch Current User       │
│ Store old values         │
└──────────────────────────┘
       ↓
┌──────────────────────────┐
│ Validate Changes         │
│ - Check duplicates       │
│ - Validate new values    │
└──────────────────────────┘
       ↓
┌──────────────────────────┐
│ Update Database          │
│ - Set new values         │
│ - Update relationships   │
└──────────────────────────┘
       ↓
┌──────────────────────────┐
│ Get Changed Fields       │
│ get_changed_fields():    │
│ Compare old vs new       │
└──────────────────────────┘
       ↓
┌──────────────────────────┐
│ Log Audit Event          │
│ log_audit():             │
│ - action: UPDATE         │
│ - old_values: {...}      │
│ - new_values: {...}      │
│ - actor_id: user_id      │
└──────────────────────────┘
       ↓
┌──────────────────────────┐
│ Return Response (200)    │
│ Updated user data        │
└──────────────────────────┘
```

## Relationships Diagram

```
┌─────────────────────────────────────────────────────┐
│                    RELATIONSHIPS                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  User                                              │
│    ├── 1:N → AuditLog (as actor)                   │
│    └── M:M → Role (via user_roles table)           │
│                                                     │
│  Role                                              │
│    ├── 1:N ← User (via user_roles)                 │
│    └── M:M → Permission (via role_permissions)     │
│                                                     │
│  Permission                                        │
│    └── M:M ← Role (via role_permissions)           │
│                                                     │
│  AuditLog                                          │
│    └── N:1 → User (as actor)                       │
│                                                     │
│  Audit Logging:                                    │
│    Triggers: CREATE, UPDATE, DELETE on             │
│    - users                                          │
│    - roles                                          │
│    - permissions                                    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## API Call Sequence Diagram

### Delete Permission with Validation
```
Client
  │
  ├─→ DELETE /admin/permissions/5
  │
  Server
    │
    ├─→ Verify JWT Token
    │
    ├─→ Check Permission (rbac:admin)
    │
    ├─→ Find Permission ID=5
    │
    ├─→ Check if in use by roles
    │   │
    │   ├─ If in use: Return 400 Error
    │   │
    │   └─ If not in use: Continue
    │
    ├─→ Store permission name (for audit)
    │
    ├─→ Delete from database
    │
    ├─→ Log audit event:
    │   {
    │     action: DELETE,
    │     entity_type: PERMISSION,
    │     entity_name: "stored_name",
    │     old_values: {key, description}
    │   }
    │
    └─→ Return 204 No Content
  │
  ← Return Response
```

## Class Hierarchy

```
SQLAlchemy Base
├── User
│   ├── id: int (PK)
│   ├── email: str (unique)
│   ├── username: str (unique)
│   ├── full_name: str
│   ├── hashed_password: str
│   ├── is_active: bool
│   ├── is_superuser: bool
│   ├── created_at: DateTime
│   ├── updated_at: DateTime
│   ├── roles: relationship[Role]
│   └── audit_logs: relationship[AuditLog]
│
├── Role
│   ├── id: int (PK)
│   ├── name: str (unique)
│   ├── description: str
│   ├── is_system: bool
│   ├── permissions: relationship[Permission]
│   └── users: relationship[User]
│
├── Permission
│   ├── id: int (PK)
│   ├── key: str (unique)
│   ├── description: str
│   └── roles: relationship[Role]
│
└── AuditLog
    ├── id: int (PK)
    ├── actor_id: int (FK)
    ├── action: str
    ├── entity_type: str
    ├── entity_id: int
    ├── entity_name: str
    ├── old_values: str (JSON)
    ├── new_values: str (JSON)
    ├── status: str
    ├── error_message: str
    ├── ip_address: str
    ├── created_at: DateTime
    └── actor: relationship[User]
```

## Request/Response Format

### Successful User Creation
```
REQUEST:
POST /admin/users
Authorization: Bearer eyJ0...
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "john_doe",
  "full_name": "John Doe",
  "password": "SecurePassword123!",
  "is_active": true,
  "is_superuser": false,
  "role_ids": [1, 2]
}

RESPONSE (201 Created):
{
  "id": 5,
  "email": "user@example.com",
  "username": "john_doe",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "roles": [
    {
      "id": 1,
      "name": "Admin",
      "description": "Administrator",
      "is_system": true,
      "permissions": [...]
    }
  ]
}

AUDIT LOG ENTRY:
{
  "id": 42,
  "actor_id": 1,
  "action": "CREATE",
  "entity_type": "USER",
  "entity_id": 5,
  "entity_name": "john_doe",
  "old_values": null,
  "new_values": "{...}",
  "status": "SUCCESS",
  "created_at": "2026-01-11T14:30:00Z"
}
```

## Error Handling Flow

```
Request comes in
    ↓
┌─ Authentication Check
│   ├─ No token → 401 Unauthorized
│   └─ Invalid token → 401 Unauthorized
│
├─ Permission Check
│   └─ Missing rbac:admin → 403 Forbidden
│
├─ Input Validation
│   ├─ Invalid format → 422 Unprocessable Entity
│   ├─ Duplicate email → 400 Bad Request
│   └─ Duplicate username → 400 Bad Request
│
├─ Database Query
│   ├─ Not found → 404 Not Found
│   └─ Constraint violation → 400 Bad Request
│
├─ Operation Validation
│   ├─ Cannot delete system role → 400 Bad Request
│   └─ Permission in use → 400 Bad Request
│
└─ Response
    ├─ Success → 200/201/204
    └─ Error → 400/401/403/404 + JSON error detail
```

## Audit Log Storage Format

```
AuditLog Entry:
{
  "id": 1,
  "actor_id": 1,
  "action": "UPDATE",
  "entity_type": "USER",
  "entity_id": 5,
  "entity_name": "john_doe",
  "old_values": JSON String
    {
      "is_active": true,
      "roles": [1, 2]
    }
  "new_values": JSON String
    {
      "is_active": false,
      "roles": [1, 3]
    }
  "status": "SUCCESS",
  "error_message": null,
  "ip_address": "192.168.1.100",
  "created_at": "2026-01-11T15:45:00Z"
}
```

## Security Layers

```
Layer 1: Transport Security
├── HTTPS/TLS (recommended for production)
└── Secure cookies for token storage

Layer 2: Authentication
├── JWT token validation
├── Token expiration checks
└── User status verification

Layer 3: Authorization
├── Permission checks (rbac:admin)
├── Role-based access control
└── User activity logging

Layer 4: Data Security
├── Password hashing (bcrypt)
├── Input validation
├── SQL injection prevention (ORM)
└── CORS configuration

Layer 5: Audit Trail
├── All operations logged
├── Change tracking (old/new values)
├── Actor identification
└── Timestamp recording
```

## Performance Optimization

```
Database Indexes:
├── users.email (unique)
├── users.username (unique)
├── roles.name (unique)
├── permissions.key (unique)
├── audit_logs.entity_type
├── audit_logs.action
└── audit_logs.created_at

Query Optimization:
├── Pagination with skip/limit
├── Relationship eager loading (joinedload)
├── Filtered queries by entity_type/action
└── Connection pooling (SQLAlchemy)
```

## Scalability Considerations

```
Horizontal Scaling:
├── Stateless API design
├── Database replication ready
├── Audit logs can be archived
└── Independent CRUD operations

Monitoring:
├── Audit log volume tracking
├── Failed operation logging
├── Permission usage analysis
└── User activity patterns
```

---

This architecture provides a scalable, secure, and auditable RBAC system suitable for enterprise applications.
