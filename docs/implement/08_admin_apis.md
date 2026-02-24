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

## Workflow 6: Statistics Administration (Super Admin)
Retrieve global overview statistics across the platform.

### Step 1: Get Totals
Get the absolute counts of moderators, content, sections, and chat queries.

- **Endpoint**: `GET /api/admin/statistics/totals/`
- **Response**:
  ```json
  {
    "total_moderators": 2,
    "total_content_items": 100,
    "total_main_sections": 5,
    "total_sub_sections": 10,
    "total_secondary_sections": 5,
    "total_sections": 20,
    "total_chat_queries": 500
  }
  ```

### Step 2: Get Content Distribution
Ratio of Video vs Audio vs Document vs YouTube.

- **Endpoint**: `GET /api/admin/statistics/content-distribution/`
- **Response**:
  ```json
  {
    "video": 50,
    "audio": 10,
    "document": 20,
    "youtube": 20
  }
  ```

### Step 3: Get Top Sections
Highest ranking Main Sections based on content count.

- **Endpoint**: `GET /api/admin/statistics/top-sections/`
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Programming",
      "content_count": 50
    }
  ]
  ```

### Step 4: Get Registrations Chart (All Time)
- **Endpoint**: `GET /api/admin/statistics/registrations-chart/`
- **Response**:
  ```json
  {
    "data": [
      {
        "date": "2026-02-01",
        "count": 5
      }
    ]
  }
  ```

### Step 5: Get Content Added Chart (Last 30 Days)
- **Endpoint**: `GET /api/admin/statistics/content-added-chart/`
- **Response**:
  ```json
  {
    "data": [
      {
        "date": "2026-02-01",
        "content_type": "video",
        "count": 2
      }
    ]
  }
  ```
