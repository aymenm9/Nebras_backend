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
