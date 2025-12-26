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
