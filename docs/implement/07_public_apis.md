# Public APIs Guide (No Auth)

This document contains endpoints for fetching data without an account.

## 1. Sections Discovery
### Main Sections
- **List**: `GET /api/public/sections/main/`
- **Retrieve**: `GET /api/public/sections/main/<id>/`
- **Filters**: `?search=Name`

### Sub Sections
- **List**: `GET /api/public/sections/sub/`
- **Param**: `?main_section=<main_id>`
- **Retrieve**: `GET /api/public/sections/sub/<id>/`

### Secondary Sub Sections
- **List**: `GET /api/public/sections/secondary/`
- **Param**: `?sub_section=<sub_id>`
- **Retrieve**: `GET /api/public/sections/secondary/<id>/`

## 2. Content Discovery
### Metadata
Fetch generic metadata for all content types.
- **Endpoint**: `GET /api/public/metadata/`
- **Filters**:
  - `?subsection=<id>`
  - `?secondary_subsection=<id>`
  - `?content_type=video|audio|document|youtube`
  - `?search=<term>`

### YouTube Videos
Fetch YouTube-specific content (including `video_url`).
- **Endpoint**: `GET /api/public/youtube/`
- **Retrieve**: `GET /api/public/youtube/<id>/`
- **Field**: `video_url` (direct link)

### R2 Files (Storage)
Fetch content stored in Cloudflare R2 / S3.
- **Endpoint**: `GET /api/public/files/`
- **Retrieve**: `GET /api/public/files/<id>/`
- **Important**: This endpoint only returns files with `upload_status='completed'`.
- **Response**: Contains `file_key` and other file metadata. Use the signed `file_url` if the backend generates one, or construct access URL if public.
