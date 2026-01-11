# 03 Moderators Management

## Endpoints (Super Admin Only)
- `GET /api/admin/moderators/`: List all moderators (staff, but not superusers).
  - **Pagination**: Yes (`?page=1`).
  - **Filters**: `is_staff`, `is_superuser`, `is_active`.
  - **Search**: `username`, `email`, `first_name`, `last_name`.
- `POST /api/admin/moderators/`: Create a new moderator.
- `GET /api/admin/moderators/<id>/`: Get moderator details.
- `PATCH /api/admin/moderators/<id>/`: Update moderator.
- `DELETE /api/admin/moderators/<id>/`: Delete moderator.

**Note**: Moderators are automatically assigned `is_staff=True`.

---

## Ban Management (Super Admin Only)
- `GET /api/admin/bans/`: List all ban records.
  - **Filters**: `user`, `is_banned`, `banned_start`, `banned_end`.
  - **Search**: `user__username`, `user__email`, `reason`.
- `POST /api/admin/bans/`: Ban a user (creates a new ban record).
- `GET /api/admin/bans/<id>/`: Get ban details.
- `PATCH /api/admin/bans/<id>/`: Update a ban (e.g., lift early by setting `is_banned=False`).
- `DELETE /api/admin/bans/<id>/`: Remove a ban record.

**Enforcement**: If a user has an active ban record (`is_banned=True` and `banned_end > now`), they will be denied access to all endpoints requiring `IsModerator` permissions.
