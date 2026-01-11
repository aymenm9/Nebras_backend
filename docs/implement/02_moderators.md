# Moderator Management Guide

This document defines the workflows for Super Admins to manage staff accounts.
**Auth Required**: Super Admin Token.

## Workflow 1: Manage Moderators
View and manage staff accounts.

### Step 1: List Moderators
- **Endpoint**: `GET /api/admin/moderators/`
- **Optional Params**: `?search=<name>`, `?page=1`
- **Action**: Render the list of users.
  ```json
  [
    {
      "id": 2,
      "username": "mod1",
      "email": "mod1@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "is_active": true
    },
    ...
  ]
  ```

### Step 2: Create Moderator
- **Endpoint**: `POST /api/admin/moderators/`
- **Body**:
  ```json
  {
    "username": "new_mod",
    "email": "mod@email.com",
    "password": "secure_password",
    "first_name": "Jane",
    "last_name": "Doe"
  }
  ```

### Step 3: Update Moderator
- **Endpoint**: `PATCH /api/admin/moderators/<id>/`
- **Body**: Any subset of fields (e.g., `{ "first_name": "Janet" }`).

### Step 4: Delete Moderator
- **Endpoint**: `DELETE /api/admin/moderators/<id>/`

---

## Workflow 2: Ban Management
Temporarily block a moderator without deleting them.

### Step 1: Check Ban Status
- **Endpoint**: `GET /api/admin/bans/?user=<user_id>`
- **Action**: Check if any active ban exists.

### Step 2: Apply Ban
- **Endpoint**: `POST /api/admin/bans/`
- **Body**:
  ```json
  {
    "user": 5,
    "reason": "Policy violation",
    "banned_end": "2025-12-31T23:59:59Z",
    "is_banned": true
  }
  ```

### Step 3: Lift Ban
- **Endpoint**: `PATCH /api/admin/bans/<ban_id>/`
- **Body**:
  ```json
  {
    "is_banned": false
  }
  ```
