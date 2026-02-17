# Content Module

## Overview
The Content module manages educational resources such as videos, audio files, and documents. These resources are organized hierarchically under Sections -> Sub-Sections -> Secondary Sub-Sections.

## Content Types
1.  **YouTube Videos**: Embedded links to external YouTube content.
2.  **R2 Files**: Direct uploads (Video, Audio, Document) stored in Cloudflare R2 / AWS S3 compatible storage.

## Key Features
-   **Hierarchical Organization**: Content is strictly categorized.
-   **Unified Upload Strategy**: Automatically switches between single-file and multipart uploads based on file size (Threshold: 5MB).
-   **Multipart Uploads**: Large files are broken into 10MB chunks for reliability and performance.
-   **Presigned URLs**: Secure, direct-to-cloud uploads without burdening the application server.
-   **Public Access**: Read-only APIs for unauthenticated users to consume content.

## Models
### Metadata
The core model linking content to the section hierarchy.
-   `title`, `description`, `thumbnail`
-   `subsection`, `secondary_subsection`
-   `content_type`: video, audio, document, youtube
-   `created_by`: User (Moderator/Admin)

### YoutubeVideo
Extension of Metadata for YouTube links.
-   `video_url`: URL string.

### R2File
Extension of Metadata for stored files.
-   `file_key`: Storage path.
-   `file_size`, `file_type`.
-   `upload_status`: pending, completed, failed.
-   `upload_type`: single, multipart.

### MultipartUpload & Part
Tracks the state of large file uploads.
-   `upload_id`: S3 upload identifier.
-   `total_parts`: Calculated number of chunks.
-   `uploaded_parts`: Counter for progress tracking.
-   `parts`: Individual chunk records with ETags.
