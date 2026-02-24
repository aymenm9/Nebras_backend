# Admin APIs Module

## Overview
This module handles administrative tasks and superuser-specific functionalities.

## Purpose
- **Admin**: Manage Moderators and Bans.
- **Section Management**: CRUD operations for Sections, Sub-Sections, and Secondary Sub-Sections.
- **Content Management**: CRUD operations for Content (YouTube, R2 Files).
- **Chat Management**: CRUD operations for strict moderation of Chat Messages and Files.
- **Statistics Management**: Aggregation views yielding totals, distributions, and time-series for platform oversight.

## Security
- **Authentication**: JWT Authentication (IsAuthenticated).
- **Permissions**: **IsSuperAdmin** required (checked via `user.is_superuser=True`).
*Note: This is distinct from Moderators who require `is_staff=True` and are not banned.*
