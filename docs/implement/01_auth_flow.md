# Authentication Guide

This guide details the complete authentication flow for the application.

## 1. Login
**Endpoint**: `POST /api/users/login/`
**Purpose**: Authenticate user with Username OR Email.

**Request Body**:
```json
{
  "username": "myuser OR myemail@example.com",
  "password": "mypassword"
}
```

**Success Response (200 OK)**:
```json
{
  "refresh": "eyJ0eX...",
  "access": "eyJ0eX...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "profile": { "profile_image": null },
    "is_super_admin": true,
    "is_moderator": true,
    "first_name": "Admin",
    "last_name": "User"
  }
}
```
*Tip: Store `access` token in memory/state and `refresh` token in secure storage.*

---

## 2. Refresh Token
**Endpoint**: `POST /api/users/token/refresh/`
**Purpose**: Get a new access token when the old one expires.

**Request Body**:
```json
{
  "refresh": "eyJ0eX..."
}
```

**Success Response (200 OK)**:
```json
{
  "access": "eyJ0eX...",
  "refresh": "eyJ0eX..."
}
```

---

## 3. Get Current Profile (Me)
**Endpoint**: `GET /api/users/me/`
**Purpose**: Reload current user data (useful on app startup).
**Headers**: `Authorization: Bearer <access_token>`

**Success Response (200 OK)**:
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
