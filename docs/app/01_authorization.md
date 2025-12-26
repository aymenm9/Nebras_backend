# 01 Authorization

## Roles
- **Super Admin**: `is_superuser=True`. Full system access.
- **Moderator**: `is_staff=True`. Content management access.

## DRF Permissions (`users.permissions`)
- `IsSuperAdmin`: Only superusers.
- `IsModerator`: Staff + Superusers.

**Example:**
```python
permission_classes = [IsModerator]
```
