# Content Management Guide

This document defines the workflows for managing content (YouTube Videos & File Uploads).

## Workflow 1: YouTube Videos
embed existing YouTube videos.

### Step 1: Create
- **Endpoint**: `POST /api/content/youtube/`
- **Body**:
  ```json
  {
    "video_url": "https://youtube.com/watch?v=...",
    "metadata": {
      "title": "Intro to Python",
      "description": "...",
      "subsection": 5,
      "secondary_subsection": 10,
      "content_type": "youtube"
    },
    "thumbnail": "(file)"
  }
  ```

---

## Workflow 2: File Uploads (R2/S3)
Unified workflow for videos, audio, and documents. The backend automatically determines if a file should be uploaded as a single file or in multipart chunks based on size (> 5MB).

### Step 1: Initiate Upload
Create the file metadata and get the upload strategy.

- **Endpoint**: `POST /api/content/files/`
- **Body**:
  ```json
  {
    "file_size": 10485760,  // Size in bytes
    "file_type": "video/mp4",
    "filename": "lecture.mp4",
    "metadata": {
      "title": "Lecture 1",
      "description": "...",
      "subsection": 5
    },
     "thumbnail": "(file)" // optional
  }
  ```
- **Response**:
  ```json
  {
    "id": 105,
    "upload_type": "multipart",  // or "single"
    "multipart_uploader": { "id": 12, "total_parts": 2, ... }
  }
  ```

### Step 2: Get Upload URL
Get the presigned URL for the file (if single) or the specific part (if multipart).

- **Endpoint**: `POST /api/content/files/<id>/upload-url/`
- **Response (Single)**: `{ "presigned_url": "..." }`
- **Response (Multipart)**: `{ "presigned_url": "...", "next_part_number": 1 }`

### Step 3: Upload to Cloud (Client-Side)
Perform a `PUT` request to the `presigned_url` with the file raw binary data.
- **Header**: Ensure `Content-Type` matches `file_type`.
- **Action**: 
  - If **Single**: Upload entire file.
  - If **Multipart**: Upload the specific chunk (10MB default).
- **Result**: Capture the `ETag` header from the response (for multipart).

### Step 4: Register Part (Multipart Only)
Notify the backend that a part has been uploaded.

- **Endpoint**: `POST /api/content/parts/`
- **Body**:
  ```json
  {
    "multipart_upload": 12,  // ID from Step 1 response
    "part_number": 1,        // Number from Step 2 response
    "etag": "\"a1b2c3...\""  // From Step 3 response headers
  }
  ```
- **Loop**: Repeat Steps 2-4 for all parts until `uploaded_parts` == `total_parts`.

### Step 5: Complete Upload
Finalize the upload. Required for **both** Single and Multipart flows.

- **Endpoint**: `POST /api/content/files/<id>/complete/`
- **Response**: R2File object with `upload_status: "completed"`.

---

## Workflow 3: Public Consumption
Fetch content for end-users (No Auth).

### Step 1: List Content
- **Endpoint**: `GET /api/public/metadata/`
- **Filters**: `?subsection=<id>`, `?search=<term>`

### Step 2: Get Content Details
- **Youtube**: `GET /api/public/youtube/<id>/` → Returns `video_url`.
- **Files**: `GET /api/public/files/<id>/` → Returns `file_url` (Signed GET URL) and metadata.
