# Authentication Guide

This document defines the exact workflows for handling user authentication.

## Workflow 1: Login
Authenticate a user and retrieve access tokens.

### Step 1: Submit Credentials
- **Endpoint**: `POST /api/users/login/`
- **Body**:
  ```json
  {
    "username": "user_or_email",
    "password": "password"
  }
  ```

### Step 2: Handle Response
- **Success (200)**:
  - Save `access` token (short-lived) in memory/header.
  - Save `refresh` token (long-lived) in secure storage.
  - Store `user` object for profile info.
  ```json
  {
    "refresh": "eyJ0eX...",
    "access": "eyJ0eX...",
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "profile": { "profile_image": "https://..." },
      "is_super_admin": true,
      "is_moderator": true,
      "first_name": "Admin",
      "last_name": "User"
    }
  }
  ```

---

## Workflow 2: Refresh Token
Get a new access token when the current one expires (401 Unauthorized).

### Step 1: Request New Token
- **Endpoint**: `POST /api/users/token/refresh/`
- **Body**:
  ```json
  {
    "refresh": "<stored_refresh_token>"
  }
  ```

### Step 2: Update Tokens
- **Success (200)**: Replace the old tokens with the new ones.
  ```json
  {
    "access": "...",
    "refresh": "..."
  }
  ```

---

## Workflow 3: Get Current User
Retrieve the latest profile data for the currently logged-in user.

### Step 1: Fetch Profile
- **Endpoint**: `GET /api/users/me/`
- **Header**: `Authorization: Bearer <access_token>`

### Step 2: Update UI
- **Success (200)**: Update the local user state with the returned object.
  ```json
  {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "profile": { "profile_image": null },
    "is_super_admin": true,
    "is_moderator": true,
    "first_name": "Admin",
    "last_name": "User"
  }
  ```
