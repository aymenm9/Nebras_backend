# Admin APIs Guide

This document covers endpoints requiring `IsSuperAdmin` privileges (is_superuser=True).

## 1. Moderator Management
- **List/Create**: `POST/GET /api/admin/moderators/`
- **RUD**: `PUT/DELETE /api/admin/moderators/<id>/`
- **Fields**: email, username, password (write-only), first_name, last_name, `section` assignments.

## 2. Ban Management
- **List/Create**: `POST/GET /api/admin/bans/`
- **RUD**: `PUT/DELETE /api/admin/bans/<id>/`
- **Fields**: user, reason, banned_start, banned_end.

## 3. Section Administration
- **Main Sections**: `GET /api/admin/sections/main/`, `DELETE /api/admin/sections/main/<id>/`
- **Sub Sections**: `GET /api/admin/sections/sub/`, `DELETE /api/admin/sections/sub/<id>/`
- **Secondary Sub Sections**: `GET /api/admin/sections/secondary/`, `DELETE /api/admin/sections/secondary/<id>/`

## 4. Content Administration
- **YouTube**: `GET /api/admin/content/youtube/`, `DELETE /api/admin/content/youtube/<id>/`
- **R2 Files**: `GET /api/admin/content/files/`, `DELETE /api/admin/content/files/<id>/`

## 5. Chat Administration
- **Messages**: `GET /api/admin/chat/messages/`, `DELETE /api/admin/chat/messages/<id>/`
- **Files**: `GET /api/admin/chat/files/`, `DELETE /api/admin/chat/files/<id>/`
