# Content Management Guide

This document defines the workflows for uploading and managing media content.

## Workflow 1: YouTube Content
Add a strictly linked YouTube video.

### Step 1: Create Entry
- **Endpoint**: `POST /api/content/youtube/`
- **Body**:
  ```json
  {
    "title": "Video Title",
    "video_url": "https://youtube.com/watch?v=...",
    "metadata": { "subsection": 1 }
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
    "content_type": "application/pdf"
  }
  ```
- **Response**: Returns a `file_url`, `id`, and storage details.
  ```json
  {
    "id": 105,
    "file_url": "https://<r2_bucket>.../book.pdf?X-Amz-Signature=...",
    "storage_key": "books/105.pdf"
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
- **Filters**: `?metadata__subsection=<id>`, `?search=<term>`

### Step 2: Get Streaming URL
- **Endpoint**: `GET /api/public/files/<id>/`
- **Response**: Contains a `file_url` (Presigned GET URL).
  ```json
  {
    "id": 105,
    "title": "My Book",
    "file_url": "https://<r2_bucket>.../book.pdf?X-Amz-Signature=...",
    "mime_type": "application/pdf"
  }
  ```
- **Action**: Stream/Download directly from that URL.
