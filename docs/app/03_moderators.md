# 03 Moderators Management

## Endpoints (Super Admin Only)
- `GET /api/users/moderators/`: List all moderators (staff, but not superusers).
  - **Pagination**: Yes (`?page=1`).
  - **Filters**: `is_staff`, `is_superuser`, `is_active`.
  - **Search**: `username`, `email`, `first_name`, `last_name`.
- `POST /api/users/moderators/`: Create a new moderator.
- `GET /api/users/moderators/<id>/`: Get moderator details.
- `PATCH /api/users/moderators/<id>/`: Update moderator.
- `DELETE /api/users/moderators/<id>/`: Delete moderator.

**Note**: Moderators are automatically assigned `is_staff=True`.

---

## Ban Management (Super Admin Only)
- `GET /api/users/bans/`: List all ban records.
  - **Filters**: `user`, `is_banned`, `banned_start`, `banned_end`.
  - **Search**: `user__username`, `user__email`, `reason`.
- `POST /api/users/bans/`: Ban a user (creates a new ban record).
- `GET /api/users/bans/<id>/`: Get ban details.
- `PATCH /api/users/bans/<id>/`: Update a ban (e.g., lift early by setting `is_banned=False`).
- `DELETE /api/users/bans/<id>/`: Remove a ban record.

**Enforcement**: If a user has an active ban record (`is_banned=True` and `banned_end > now`), they will be denied access to all endpoints requiring `IsModerator` permissions.
