# RBAC System Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### 1. Run Database Migration
```bash
cd flash-backend-coolify
alembic upgrade add_audit_log_table
```

### 2. Restart Backend
```bash
python startup.py
# or
python -m uvicorn app.main:app --reload
```

### 3. You're Ready!
All RBAC endpoints are now active at `/admin/*`

---

## 📋 Common Tasks

### Create a New Super Admin User
```bash
curl -X POST http://localhost:8000/admin/users \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "superadmin@company.com",
    "username": "superadmin",
    "full_name": "Super Admin",
    "password": "SuperSecure123!",
    "is_active": true,
    "is_superuser": true,
    "role_ids": []
  }'
```

### Create a New Role
```bash
curl -X POST http://localhost:8000/admin/roles \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "HR Manager",
    "description": "Manages HR operations",
    "permission_keys": ["users:read", "employees:create", "employees:update", "reports:view"]
  }'
```

### Create a New Permission
```bash
curl -X POST http://localhost:8000/admin/permissions \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "payroll:approve",
    "description": "Approve payroll transactions"
  }'
```

### Assign Role to User
```bash
curl -X PUT http://localhost:8000/admin/users/5 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "role_ids": [1, 2, 3]
  }'
```

### Update User Status
```bash
curl -X PUT http://localhost:8000/admin/users/5 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "is_active": false
  }'
```

### View All Audit Logs
```bash
curl -X GET http://localhost:8000/admin/audit-logs \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### View User's Activity
```bash
curl -X GET http://localhost:8000/admin/audit-logs/USER/5 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Check Who Created a Role
```bash
curl -X GET http://localhost:8000/admin/audit-logs/ROLE/2 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Delete a Permission
```bash
curl -X DELETE http://localhost:8000/admin/permissions/5 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🔍 Audit Log Examples

### All Changes to User #5
```bash
GET /admin/audit-logs/USER/5
```

### All Permission Creation Events
```bash
GET /admin/audit-logs?entity_type=PERMISSION&action=CREATE
```

### All User Updates
```bash
GET /admin/audit-logs?entity_type=USER&action=UPDATE
```

### All Deletions
```bash
GET /admin/audit-logs?action=DELETE
```

---

## 📊 Data Models

### User Model
```python
{
  "id": int,
  "email": str,
  "username": str,
  "full_name": str,
  "is_active": bool,
  "is_superuser": bool,
  "roles": [Role]
}
```

### Role Model
```python
{
  "id": int,
  "name": str,
  "description": str,
  "is_system": bool,
  "permissions": [Permission]
}
```

### Permission Model
```python
{
  "id": int,
  "key": str,
  "description": str
}
```

### Audit Log Model
```python
{
  "id": int,
  "actor_id": int,
  "action": str,           # CREATE, UPDATE, DELETE
  "entity_type": str,      # USER, ROLE, PERMISSION
  "entity_id": int,
  "entity_name": str,
  "old_values": str,       # JSON
  "new_values": str,       # JSON
  "status": str,           # SUCCESS, FAILED
  "error_message": str,
  "ip_address": str,
  "created_at": datetime
}
```

---

## 🔐 Security Checklist

- ✅ All endpoints require `rbac:admin` permission
- ✅ All changes are audited
- ✅ Passwords are hashed with bcrypt
- ✅ System roles are protected
- ✅ Permissions in use cannot be deleted
- ✅ Email/username must be unique
- ✅ Token required for all operations

---

## 🛠️ Troubleshooting

### "Permission denied" Error
→ Ensure your user has `rbac:admin` permission

### "Role not found" Error
→ Check the role ID is correct and exists

### "Cannot delete system role" Error
→ System roles are protected, create a custom role instead

### "Permission is assigned to X roles" Error
→ Remove the permission from all roles first, then delete

### "User with this email already exists" Error
→ Email must be unique, use a different email

---

## 📚 Complete Documentation

- Full API specification: `docs/RBAC_API_SPECIFICATION.md`
- Enhancement details: `docs/RBAC_ENHANCEMENT.md`
- Summary: `docs/RBAC_ENHANCEMENT_SUMMARY.md`

---

## 🎯 Next Steps

1. ✅ Create super admin user
2. ✅ Create roles for your organization
3. ✅ Create required permissions
4. ✅ Assign roles to users
5. ✅ Monitor audit logs
6. ✅ Implement frontend UI for admin panel

---

## 💡 Tips

- Use meaningful role names (Admin, Manager, Viewer, etc.)
- Follow permission naming: `resource:action`
- Review audit logs weekly
- Deactivate users instead of deleting them
- Keep system roles unchanged
- Document your permission structure

---

## 📞 Need Help?

Check the audit logs for what happened:
```bash
curl -X GET http://localhost:8000/admin/audit-logs \
  -H "Authorization: Bearer YOUR_TOKEN" \
  | jq . # Pretty print JSON
```

All operations are logged with:
- Who did it (actor_id)
- What happened (action)
- What changed (old_values, new_values)
- When it happened (created_at)
- If it succeeded (status)
