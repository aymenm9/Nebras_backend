# Moderator Management Guide

This guide is for **Super Admins** to manage the staff (Moderators).
**All endpoints require**: `Authorization: Bearer <super_admin_token>`

## 1. List All Moderators
**Endpoint**: `GET /api/users/moderators/`
**Purpose**: View all staff members (excluding Super Admins).

**Response**:
```
[
  {
    "id": 2,
    "username": "mod1",
    "email": "mod1@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  ...
]
```

### Filtering & Search
- **Filter**: `/api/users/moderators/?is_active=false`
- **Search**: `/api/users/moderators/?search=john`
- **Pagination**: `/api/users/moderators/?page=2`

---

## 2. Create Moderator
**Endpoint**: `POST /api/users/moderators/`
**Purpose**: Create a new staff account.
**Note**: `is_staff` is automatically set to `true`.

**Request Body**:
```json
{
  "username": "new_mod",
  "email": "mod@email.com",
  "password": "securePass123!",
  "first_name": "Jane",
  "last_name": "Doe"
}
```

---

## 3. Update Moderator
**Endpoint**: `PATCH /api/users/moderators/<id>/`
**Purpose**: Update details like email or name.
**Note**: You cannot change a user's password here (use a separate reset flow if needed).

**Request Body** (All fields optional):
```json
{
  "first_name": "Janet",
  "email": "newemail@example.com"
}
```

---

## 4. Delete Moderator
**Endpoint**: `DELETE /api/users/moderators/<id>/`
**Purpose**: Permanently remove a moderator account.

---

## 5. Ban Management
Banning is used to temporarily or permanently block a moderator from using their account without deleting it.

### Ban a User
**Endpoint**: `POST /api/users/bans/`
**Request Body**:
```json
{
  "user": 2,
  "reason": "Repeated policy violations",
  "banned_end": "2026-02-07T00:00:00Z",
  "is_banned": true
}
```
*   `user`: The ID of the moderator.
*   `banned_end`: The UTC timestamp when the ban expires.
*   `is_banned`: Must be `true` to active the ban.

### List Active Bans
**Endpoint**: `GET /api/users/bans/?is_banned=true`

### Lift a Ban Early
**Endpoint**: `PATCH /api/users/bans/<id>/`
**Request Body**:
```json
{
  "is_banned": false
}
```
Once `is_banned` is set to `false`, the user instantly regains access, even if `banned_end` is still in the future.
