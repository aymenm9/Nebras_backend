# Content Management & Delivery Guide

This guide explains how to manage and access content (YouTube videos, PDF books, Audio files, etc.).

## 1. Staff Management (Auth Required)

### YouTube Videos
*   **List/Create**: `POST /api/content/youtube/`
*   **Detail/Update/Delete**: `GET/PATCH/DELETE /api/content/youtube/<id>/`

### File Uploads (R2)
1.  **Initiate Upload**: `POST /api/content/files/upload/`
    *   This returns a `file_url` which is a **presigned PUT URL**.
2.  **Upload to R2**: Use a standard HTTP PUT request to the `file_url` with the file binary.
3.  **Completion**: Once the file is successfully uploaded to R2, you **MUST** send a `PATCH` request to `/api/content/files/<id>/` with `{ "upload_completed": true }`.
    *   Files with `upload_completed=False` will **NOT** appear in the public API.

---

## 2. Public Access (No Auth)

Use these for the client application (Android/Web public view) under the `/api/public/` prefix.

### YouTube Videos
*   **List**: `GET /api/public/youtube/`
    *   **Filters**: `?metadata__subsection=1`, `?metadata__content_type=VIDEO`
    *   **Search**: `?search=Physics`
*   **Detail**: `GET /api/public/youtube/<id>/`

### R2 Files (Books / Audio)
*   **List**: `GET /api/public/files/`
    *   This returns objects including a `file_url` which is a **presigned GET URL** for streaming/downloading.
*   **Detail**: `GET /api/public/files/<id>/`

### Metadata (Generic Search)
*   **List**: `GET /api/public/metadata/`
    *   Useful for searching across all types of content.
*   **Detail**: `GET /api/public/metadata/<id>/`

---

## 3. Filtering & Search Tips
All public list endpoints support:
*   `search`: Fuzzy search on titles and descriptions.
*   `metadata__subsection`: Filter by subsection ID.
*   `metadata__subsection__main_section`: Filter by main section ID.
*   `metadata__content_type`: Filter by type (`BOOK`, `AUDIO`, `VIDEO`).
