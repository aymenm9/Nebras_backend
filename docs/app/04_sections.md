# 04 Sections Management

## Endpoints

### Main Sections (Super Admin Only)
- `GET /api/sections/main/`: List all main sections.
  - **Pagination**: Yes.
  - **Filters**: `created_by`.
  - **Search**: `name`.
- `POST /api/sections/main/`: Create a new main section.
- `GET /api/sections/main/<id>/`: Get main section details.
- `PATCH /api/sections/main/<id>/`: Update main section.
- `DELETE /api/sections/main/<id>/`: Delete main section.

### Sub Sections (Moderators + Super Admin)
- `GET /api/sections/sub/`: List all sub sections.
  - **Pagination**: Yes.
  - **Filters**: `created_by`, `main_section`.
  - **Search**: `name`.
- `POST /api/sections/sub/`: Create a new sub section.
- `GET /api/sections/sub/<id>/`: Get sub section details.
- `PATCH /api/sections/sub/<id>/`: Update sub section.
- `DELETE /api/sections/sub/<id>/`: Delete sub section.

### Secondary Sub Sections (Moderators + Super Admin)
- `GET /api/sections/secondary/`: List all secondary sub sections.
  - **Pagination**: Yes.
  - **Filters**: `created_by`, `sub_section`, `sub_section__main_section`.
  - **Search**: `name`.
- `POST /api/sections/secondary/`: Create a new secondary sub section.
- `GET /api/sections/secondary/<id>/`: Get secondary sub section details.
- `PATCH /api/sections/secondary/<id>/`: Update secondary sub section.
- `DELETE /api/sections/secondary/<id>/`: Delete secondary sub section.

## Public Endpoints (No Auth Required)
- `GET /api/public/sections/main/`: List all main sections.
  - **Pagination**: Yes.
  - **Filters**: `created_by`.
  - **Search**: `name`.
- `GET /api/public/sections/main/<id>/`: Get main section details.
- `GET /api/public/sections/sub/`: List all sub sections.
  - **Pagination**: Yes.
  - **Filters**: `created_by`, `main_section`.
  - **Search**: `name`.
- `GET /api/public/sections/sub/<id>/`: Get sub section details.
- `GET /api/public/sections/secondary/`: List all secondary sub sections.
  - **Pagination**: Yes.
  - **Filters**: `created_by`, `sub_section`, `sub_section__main_section`.
  - **Search**: `name`.
- `GET /api/public/sections/secondary/<id>/`: Get secondary sub section details.
