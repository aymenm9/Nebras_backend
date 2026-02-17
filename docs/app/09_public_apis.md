# Public APIs Module

## Overview
This module exposes **read-only** endpoints for unauthorized consumption. It allows the frontend to fetch sections hierarchy and content metadata without user authentication.

## Purpose
The primary use case is for unauthenticated users exploring the application (e.g., browsing library categories, viewing free content).

## Coverage
- **Sections**: List/Retrieve Main, Sub, and Secondary Sub Sections.
- **Content**: Fetch YouTube videos, R2 files (documents/videos), and generic metadata.

## Security
- **Authentication**: None (AllowAny).
- **Permissions**: Read-Only. No write/update/delete operations are permitted.
- **Filters**: Supports DjangoFilterBackend (e.g., by section ID) and SearchFilter (by title/description).
