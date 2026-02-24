# Dashboard Statistics Guide

This document defines the workflows for consuming analytical endpoints to populate dashboards. Currently, it focuses on endpoints requiring `IsModerator` privileges.

## Workflow 1: Moderator Dashboard
These endpoints enforce strict filtering so the moderator only sees statistics related to content or sections they have personally created.

### Step 1: Get Totals
Get the aggregate total counts of content items, YouTube videos, and sections created by the logged-in moderator.

- **Endpoint**: `GET /api/dashboard-statistics/moderator/totals/`
- **Response**:
  ```json
  {
    "total_content_items": 15,
    "total_youtube_videos": 5,
    "total_sections": 3
  }
  ```

### Step 2: Get Content Distribution
Get the breakdown of different content types uploaded by the moderator.

- **Endpoint**: `GET /api/dashboard-statistics/moderator/content-distribution/`
- **Response**:
  ```json
  {
    "video": 10,
    "audio": 2,
    "document": 3,
    "youtube": 5
  }
  ```

### Step 3: Get Content Added Chart (Last 30 Days)
Get daily upload counts by content type for the last 30 days, specific to the moderator.

- **Endpoint**: `GET /api/dashboard-statistics/moderator/content-added-chart/`
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
