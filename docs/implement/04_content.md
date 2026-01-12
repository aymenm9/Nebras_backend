# Content Management Guide

This document defines the workflows for uploading and managing media content.

## Workflow 1: YouTube Content
Add a strictly linked YouTube video.

### Step 1: Select Hierarchy
To maintain consistency, the frontend should follow this filtering flow:
1.  **Select Main Section**: Fetch from `GET /api/sections/main/`.
2.  **Filter Sub Sections**: Fetch from `GET /api/sections/sub/?main_section=<main_section_id>`.
3.  **(Optional) Filter Secondary Sub Sections**: Fetch from `GET /api/sections/secondary/?sub_section=<sub_section_id>`.

> **Note**: Only the `subsection` (mandatory) and `secondary_subsection` (optional) IDs are sent to the backend. The `MainSection` is used only for UI filtering.

### Step 2: Create Entry
- **Endpoint**: `POST /api/content/youtube/`
- **Body**:
  ```json
  {
    "video_url": "https://youtube.com/watch?v=...",
    "metadata": { 
      "title": "Video Title",
      "subsection": 5,
      "secondary_subsection": 10 
    }
  }
  ```

---

## Workflow 2: File Upload (Presigned URL)
Upload a file (PDF, Audio, etc.) to Object Storage (R2).

### Step 1: Initialize Upload
- **Endpoint**: `POST /api/content/files/upload/`
- **Body**:
  ```json
  {
    "filename": "book.pdf",
    "file_type": "application/pdf",
    "file_size": 10240,
    "metadata": {
      "title": "Book Title",
      "description": "Optional description",
      "subsection": 5,
      "secondary_subsection": 10
    }
  }
  ```
- **Response**: Returns a `file_url`, `id`, and storage details.
  ```json
  {
    "id": 105,
    "file_url": "https://<r2_bucket>.../book.pdf?X-Amz-Signature=...",
    "filename": "book.pdf",
    "file_size": 10240,
    "file_type": "application/pdf",
    "metadata": {
       "id": 201,
       "title": "Book Title",
       "content_type": "document",
       ...
    }
  }
  ```

### Step 2: Upload to R2 (Client-Side)
- **Action**: Perform a `PUT` request to the `file_url` received in Step 1.
- **Body**: The raw file binary.
- **Headers**: `Content-Type: application/pdf`

### Step 3: Confirm Completion
- **Endpoint**: `PATCH /api/content/files/<id>/`
- **Body**:
  ```json
  { "upload_completed": true }
  ```
- **Result**: The file is now visible in the Public API.

---

## Workflow 3: Public Consumption
Fetch content for end-users (No Auth).

### Step 1: List Content
- **Endpoint**: `GET /api/public/metadata/`
- **Filters**: `?subsection=<id>`, `?search=<term>`

### Step 2: Get Streaming URL
- **Endpoint**: `GET /api/public/files/<id>/`
- **Response**: Contains a `file_url` (Presigned GET URL) and metadata.
  ```json
  {
    "id": 105,
    "file_url": "https://<r2_bucket>.../book.pdf?X-Amz-Signature=...",
    "filename": "book.pdf",
    "file_size": 10240,
    "file_type": "application/pdf",
    "metadata": {
       "id": 201,
       "title": "Book Title",
       "description": "...",
       "content_type": "document",
       "subsection": 5,
       "secondary_subsection": 10
    }
  }
  ```
- **Action**: Stream/Download directly from that URL.
