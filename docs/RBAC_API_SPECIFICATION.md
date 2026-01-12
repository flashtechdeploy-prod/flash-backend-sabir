# Complete RBAC API Specification

## Base URL
```
http://localhost:8000/admin
```

## Authentication
All endpoints require a valid JWT token in the `Authorization` header:
```
Authorization: Bearer <token>
```

## Permission Required
All endpoints require the `rbac:admin` permission.

---

## Users Endpoints

### 1. List All Users
```
GET /users
```

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Number of records to return (default: 100)

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "email": "user@example.com",
    "username": "john_doe",
    "full_name": "John Doe",
    "is_active": true,
    "is_superuser": false,
    "roles": [
      {
        "id": 1,
        "name": "Admin",
        "description": "Administrator role",
        "is_system": true,
        "permissions": [...]
      }
    ]
  }
]
```

---

### 2. Get User by ID
```
GET /users/{user_id}
```

**Path Parameters:**
- `user_id` (int): User ID

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "john_doe",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "roles": [...]
}
```

**Error Responses:**
- `404 Not Found`: User does not exist

---

### 3. Create User
```
POST /users
```

**Request Body:**
```json
{
  "email": "newuser@example.com",
  "username": "new_user",
  "full_name": "New User",
  "password": "secure_password",
  "is_active": true,
  "is_superuser": false,
  "role_ids": [1, 2, 3]
}
```

**Response:** `201 Created`
```json
{
  "id": 10,
  "email": "newuser@example.com",
  "username": "new_user",
  "full_name": "New User",
  "is_active": true,
  "is_superuser": false,
  "roles": [...]
}
```

**Error Responses:**
- `400 Bad Request`: User with this email or username already exists
- `400 Bad Request`: Invalid role IDs

**Audit Log Generated:**
```
action: CREATE
entity_type: USER
entity_id: 10
new_values: {email, username, full_name, is_active, is_superuser, role_ids}
```

---

### 4. Update User
```
PUT /users/{user_id}
```

**Path Parameters:**
- `user_id` (int): User ID

**Request Body:** (all fields optional)
```json
{
  "email": "updated@example.com",
  "username": "updated_username",
  "full_name": "Updated Name",
  "password": "new_password",
  "is_active": true,
  "is_superuser": false,
  "role_ids": [1, 2]
}
```

**Response:** `200 OK`
```json
{
  "id": 10,
  "email": "updated@example.com",
  "username": "updated_username",
  "full_name": "Updated Name",
  "is_active": true,
  "is_superuser": false,
  "roles": [...]
}
```

**Error Responses:**
- `404 Not Found`: User does not exist
- `400 Bad Request`: Email/username already in use

**Audit Log Generated:**
```
action: UPDATE
entity_type: USER
old_values: {previous values}
new_values: {updated values}
```

---

### 5. Delete User
```
DELETE /users/{user_id}
```

**Path Parameters:**
- `user_id` (int): User ID

**Response:** `204 No Content`

**Error Responses:**
- `404 Not Found`: User does not exist

**Audit Log Generated:**
```
action: DELETE
entity_type: USER
old_values: {username}
```

---

## Roles Endpoints

### 1. List All Roles
```
GET /roles
```

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Number of records to return (default: 100)

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Admin",
    "description": "Administrator role",
    "is_system": true,
    "permissions": [
      {
        "id": 1,
        "key": "users:create",
        "description": "Create users"
      }
    ]
  }
]
```

---

### 2. Create Role
```
POST /roles
```

**Request Body:**
```json
{
  "name": "Manager",
  "description": "Manager role",
  "permission_keys": ["users:read", "reports:view", "reports:create"]
}
```

**Response:** `201 Created`
```json
{
  "id": 2,
  "name": "Manager",
  "description": "Manager role",
  "is_system": false,
  "permissions": [...]
}
```

**Error Responses:**
- `400 Bad Request`: Role name already exists
- `400 Bad Request`: Invalid permission keys

**Audit Log Generated:**
```
action: CREATE
entity_type: ROLE
new_values: {name, description, permission_keys}
```

---

### 3. Update Role
```
PUT /roles/{role_id}
```

**Path Parameters:**
- `role_id` (int): Role ID

**Request Body:** (all fields optional)
```json
{
  "name": "Senior Manager",
  "description": "Updated description",
  "permission_keys": ["users:read", "users:update", "reports:view"]
}
```

**Response:** `200 OK`
```json
{
  "id": 2,
  "name": "Senior Manager",
  "description": "Updated description",
  "is_system": false,
  "permissions": [...]
}
```

**Error Responses:**
- `404 Not Found`: Role does not exist
- `400 Bad Request`: Role name already exists
- `400 Bad Request`: Cannot modify system roles

**Audit Log Generated:**
```
action: UPDATE
entity_type: ROLE
old_values: {previous values}
new_values: {updated values}
```

---

### 4. Delete Role
```
DELETE /roles/{role_id}
```

**Path Parameters:**
- `role_id` (int): Role ID

**Response:** `204 No Content`

**Error Responses:**
- `404 Not Found`: Role does not exist
- `400 Bad Request`: System roles cannot be deleted

**Audit Log Generated:**
```
action: DELETE
entity_type: ROLE
old_values: {name}
```

---

## Permissions Endpoints

### 1. List All Permissions
```
GET /permissions
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "key": "users:create",
    "description": "Create users"
  }
]
```

---

### 2. Create Permission
```
POST /permissions
```

**Request Body:**
```json
{
  "key": "reports:export",
  "description": "Export reports to PDF/Excel"
}
```

**Response:** `201 Created`
```json
{
  "id": 5,
  "key": "reports:export",
  "description": "Export reports to PDF/Excel"
}
```

**Error Responses:**
- `400 Bad Request`: Permission key already exists

**Audit Log Generated:**
```
action: CREATE
entity_type: PERMISSION
new_values: {key, description}
```

---

### 3. Update Permission ⭐ NEW
```
PUT /permissions/{permission_id}
```

**Path Parameters:**
- `permission_id` (int): Permission ID

**Request Body:** (all fields optional)
```json
{
  "key": "reports:export_full",
  "description": "Export full reports with all data"
}
```

**Response:** `200 OK`
```json
{
  "id": 5,
  "key": "reports:export_full",
  "description": "Export full reports with all data"
}
```

**Error Responses:**
- `404 Not Found`: Permission does not exist
- `400 Bad Request`: Permission key already exists

**Audit Log Generated:**
```
action: UPDATE
entity_type: PERMISSION
old_values: {key, description}
new_values: {updated values}
```

---

### 4. Delete Permission ⭐ NEW
```
DELETE /permissions/{permission_id}
```

**Path Parameters:**
- `permission_id` (int): Permission ID

**Response:** `204 No Content`

**Error Responses:**
- `404 Not Found`: Permission does not exist
- `400 Bad Request`: Permission is assigned to {N} role(s). Remove it from all roles first.

**Audit Log Generated:**
```
action: DELETE
entity_type: PERMISSION
old_values: {key}
```

---

## Audit Logs Endpoints ⭐ NEW

### 1. List Audit Logs
```
GET /audit-logs
```

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Number of records to return (default: 100)
- `entity_type` (string, optional): Filter by entity type (USER, ROLE, PERMISSION)
- `action` (string, optional): Filter by action (CREATE, UPDATE, DELETE)

**Examples:**
```
GET /audit-logs?entity_type=USER
GET /audit-logs?action=CREATE&skip=0&limit=50
GET /audit-logs?entity_type=ROLE&action=UPDATE
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "actor_id": 1,
    "action": "CREATE",
    "entity_type": "USER",
    "entity_id": 5,
    "entity_name": "john_doe",
    "old_values": null,
    "new_values": "{\"email\": \"john@example.com\", \"username\": \"john_doe\", ...}",
    "status": "SUCCESS",
    "error_message": null,
    "ip_address": "192.168.1.100",
    "created_at": "2026-01-11T10:30:00Z"
  }
]
```

---

### 2. Get Audit Logs for Entity
```
GET /audit-logs/{entity_type}/{entity_id}
```

**Path Parameters:**
- `entity_type` (string): Entity type (USER, ROLE, PERMISSION)
- `entity_id` (int): Entity ID

**Examples:**
```
GET /audit-logs/USER/5        - Get all logs for user ID 5
GET /audit-logs/ROLE/2        - Get all logs for role ID 2
GET /audit-logs/PERMISSION/1  - Get all logs for permission ID 1
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "actor_id": 1,
    "action": "CREATE",
    "entity_type": "USER",
    "entity_id": 5,
    "entity_name": "john_doe",
    "old_values": null,
    "new_values": "{...}",
    "status": "SUCCESS",
    "error_message": null,
    "ip_address": "192.168.1.100",
    "created_at": "2026-01-11T10:30:00Z"
  },
  {
    "id": 2,
    "actor_id": 1,
    "action": "UPDATE",
    "entity_type": "USER",
    "entity_id": 5,
    "entity_name": "john_doe",
    "old_values": "{\"email\": \"john@example.com\"}",
    "new_values": "{\"email\": \"john.doe@example.com\"}",
    "status": "SUCCESS",
    "error_message": null,
    "ip_address": "192.168.1.100",
    "created_at": "2026-01-11T11:15:00Z"
  }
]
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "User with this email or username already exists"
}
```

### 404 Not Found
```json
{
  "detail": "User not found"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid or expired token"
}
```

---

## Common Permission Keys

```
# User Management
users:create
users:read
users:update
users:delete

# Role Management
roles:create
roles:read
roles:update
roles:delete

# Permission Management
permissions:create
permissions:read
permissions:update
permissions:delete

# Reports
reports:view
reports:create
reports:export
reports:delete

# System
rbac:admin
system:config
```

---

## Examples Using curl

### Create User
```bash
curl -X POST http://localhost:8000/admin/users \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "email": "manager@example.com",
    "username": "manager1",
    "full_name": "Manager One",
    "password": "SecurePass123!",
    "is_active": true,
    "is_superuser": false,
    "role_ids": [2]
  }'
```

### Create Role
```bash
curl -X POST http://localhost:8000/admin/roles \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Viewer",
    "description": "Read-only access",
    "permission_keys": ["users:read", "reports:view"]
  }'
```

### Update Permission
```bash
curl -X PUT http://localhost:8000/admin/permissions/5 \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Export reports in all formats"
  }'
```

### Get Audit Logs
```bash
curl -X GET "http://localhost:8000/admin/audit-logs?entity_type=USER&action=CREATE" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Get User's Audit Trail
```bash
curl -X GET http://localhost:8000/admin/audit-logs/USER/5 \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

---

## Response Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 204 | No Content - Successful deletion or update |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Invalid/expired token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error |

---

## Best Practices

1. **Always validate input** on the client side before sending
2. **Use meaningful role names** (Admin, Manager, Viewer, etc.)
3. **Follow permission naming convention** (resource:action)
4. **Review audit logs regularly** for security
5. **Never expose sensitive data** in error messages
6. **Use strong passwords** for user accounts
7. **Implement rate limiting** on the frontend for API calls
8. **Keep token refresh time short** for security
