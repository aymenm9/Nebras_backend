# 05 Content Management

## Endpoints

### YouTube Videos (Moderators + Super Admin)
- `GET /api/content/youtube/`: List YouTube videos created by the user (Super Admins see all).
  - **Filters**: `metadata__created_by`.
- `POST /api/content/youtube/`: Upload a new YouTube video metadata.
- `GET /api/content/youtube/<id>/`: Get YouTube video details.
- `PATCH /api/content/youtube/<id>/`: Update YouTube video.
- `DELETE /api/content/youtube/<id>/`: Delete YouTube video.

### R2 Files (Moderators + Super Admin)
- `GET /api/content/files/`: List files created by the user (Super Admins see all).
  - **Filters**: `created_by`.
  - **Note**: This view shows ALL files (completed and incomplete) for management purposes.
- `POST /api/content/files/upload/`: Initiate a file upload (Returns a presigned PUT URL).
- `GET /api/content/files/<id>/`: Get file details (Returns a presigned GET URL).
- `PATCH /api/content/files/<id>/`: Update file metadata.
- `DELETE /api/content/files/<id>/`: Delete file.

## Public Endpoints (No Auth Required)

### YouTube Videos
- `GET /api/public/youtube/`: List all public YouTube videos.
  - **Filters**: `metadata__created_by`, `metadata__subsection`, `metadata__subsection__main_section`, `metadata__secondary_subsection`, `metadata__content_type`.
  - **Search**: `metadata__title`, `metadata__description`.
- `GET /api/public/youtube/<id>/`: Get YouTube video details.

### Metadata
- `GET /api/public/metadata/`: List all content metadata.
  - **Filters**: `created_by`, `subsection`, `subsection__main_section`, `secondary_subsection`, `content_type`.
  - **Search**: `title`, `description`.
- `GET /api/public/metadata/<id>/`: Get metadata details.

### R2 Files
- `GET /api/public/files/`: List all public R2 files (Provides presigned GET URLs).
  - **Implicit Filter**: `upload_completed=True`.
  - **Filters**: `created_by`, `metadata__subsection`, `metadata__subsection__main_section`, `metadata__secondary_subsection`, `metadata__content_type`.
  - **Search**: `metadata__title`, `metadata__description`.
- `GET /api/public/files/<id>/`: Get R2 file details.
