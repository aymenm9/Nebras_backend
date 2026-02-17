# 1. Project Overview (Broad Idea)

Cloud-based digital archiving and content management system.

Purpose:
- Store and serve large media (books, audio, very long videos)
- Organize content hierarchically
- Enforce role-based access
- Stream content securely without backend handling files

Core principle:
**Backend owns metadata and permissions. Object storage (Cloudflare R2) owns files.**

---

# 2. Actors & Permissions (System Truth)

## Roles

### User (Public / Guest)
- No Login / Signup required
- Read-only access
- Browse categories
- Stream content

### Moderator
- All User permissions
- Upload single content
- Edit/delete content metadata

### Super Admin
- All Moderator permissions
- Manage moderators
- Manage categories
- System-level settings

Enforcement:
- UI hides features
- Backend strictly enforces roles

---

# 3. High-Level Architecture (Top Down)

```
Android App (Users / Guests)
  ├─ Browse & Stream (Public Access)
  ├─ No Login / Account Required
  │
  ▼
Android App (Admins / Moderators)
  ├─ Content Management
  ├─ Internal Chat (REST in MVP)
  │
  ▼
Backend API (Django + DRF)
  ├─ Auth & RBAC (Staff Only: Email + Password)
  ├─ Public API (`api/public/`) -> Guest Access (No Auth)
  ├─ Management API (`api/content/`, `api/sections/`) -> Staff Only
  ├─ Category hierarchy (Public View)
  ├─ Content metadata (Public View)
  ├─ Upload orchestration (Hybrid: Direct & Signed URLs)
  ├─ Signed URL generation (Large files)
  ├─ Admin messaging (Polling/Refresh)
  │
  ▼
Database (PostgreSQL)
  │
  ▼
Object Storage (Cloudflare R2)
  │
  ▼
CDN / Streaming (Cloudflare)
```

Backend is stateless and never handles media bytes.


---

# 4. Backend Responsibilities (Exact Scope)

Backend DOES:
- Authenticate Staff (Mods/Admins via JWT)
- Enforce roles for management actions
- Manage category tree
- Store content metadata
- Generate signed upload URLs
- Generate signed streaming URLs

Backend DOES NOT:
- Store files
- Stream media
- Transcode
- Process media

---

# 5. Data Model (Backend-Centric)

## 5.1 User & Authentication

**Model**: Standard Django `User` + `OneToOne` Profile. (Used for Staff only)

### Authentication
- **Login**: Email + Password (Moderators and Admins only).
- **Signup**: No public signup. Accounts are created by Super Admin.
- **Normal Users**: Anonymous access only. No accounts.

### Profile Model (1-to-1)
```
Profile
- user_id (FK to auth_user)
- profile_image (Small file -> Direct Upload to R2)
```

### Ban Model (1-to-1 per User)
Used for tracking the current ban state of a user.
- **user**: OneToOne to User.
- **is_banned**: Boolean flag.
- **banned_end**: Expiration timestamp.
- **banned_by**: FK to User who issued the ban.
- **reason**: Text field for justification.

### Role Logic
- **Moderator**: Access to content and section management.
- **Super Admin**: Can manage moderators and issue/lift bans.
    - **Ban Logic**: Enforcement is handled via `IsModerator` permission class which checks if a user has an active ban record (`is_banned=True` and `now < banned_end`).

Notes:
- Profile image is uploaded directly to R2 via Django backend (Small file flow).
- Bans are dynamic; access is restored automatically once `banned_end` passes.

---

## 5.2 Category Structure (Fixed Hierarchy)

Not fully recursive. Fixed to **three semantic levels**.

### Levels
- **Main Section** (Root)
- **Sub Section** (Child of Main)
- **Secondary Sub Section** (Optional Child of Sub)

Rules:
- **Main Sections** contain ONLY Sub Sections.
- **Sub Sections** can have EITHER:
  1. Files directly.
  2. Secondary Sub Sections (which then contain files).
- **Secondary Sub Sections** contain ONLY files.

### Data Model

```
Category
- id
- name
- level (MAIN | SUB | SUB_SUB)
- parent_id (nullable)
- order_index
- created_by
```

Validation rules enforced in backend, not UI.


---

## 5.3 Content (Metadata Only)

**Models**:
- **Metadata**: Base info (title, description, parent section).
- **YoutubeVideo**: Links to external videos.
- **R2File**: Stores file details (size, type, status) and handles upload logic.
- **MultipartUpload**: Tracks chunked uploads for large files.

---

# 6. Storage & Security Model

## 6.1 Object Storage (Cloudflare R2)

- **Provider**: Cloudflare R2 (S3-compatible).
- **Buckets**: Private.

### Storage Strategy (Hybrid)
1. **Profile Images / Thumbnails**:
   - **Mechanism**: Direct upload via Django Serializers.
   - **Storage**: `django-storages` (boto3) backend.
   
2. **Content Files (Videos/Docs/Audio)**:
   - **Mechanism**: Unified Upload Strategy.
   - **Small Files (< 5MB)**: Single PUT presigned URL.
   - **Large Files (> 5MB)**: Multipart Chunked Upload (10MB parts).
   - **Flow**: Init -> Get URL(s) -> Client Uploads -> Complete.

Structure:
```
<Section>/<SubSection>/<Type>/{uuid}
```

---

# 7. Upload Flow (Core Backend Logic)

## 7.1 Initialization & URL Generation

Client → Backend:
```
POST /api/content/files/
{ file_size, file_type, metadata: {...} }
```

Backend:
- Creates `R2File` record.
- Determines `upload_type` ("single" vs "multipart").
- If multipart, initializes S3 multipart upload.

Client → Backend:
```
POST /api/content/files/<id>/upload-url/
```

Backend:
- Returns Presigned URL (for whole file or specific part).

## 7.2 Client Upload

Client → S3 (Directly):
- PUTs binary data to the provided Presigned URL.
- For Multipart: Uploads chunks sequentially.

## 7.3 Part Registration (Multipart Only)

Client → Backend:
```
POST /api/content/parts/
{ multipart_upload_id, part_number, etag }
```

## 7.4 Completion

Client → Backend:
```
POST /api/content/files/<id>/complete/
```

Backend:
- Verifies all parts (if multipart) or file existence.
- Marks status as `completed`.
- File becomes available via Public APIs.

---

# 8. Streaming / Download Flow

Client → Backend:
```
GET /api/public/files/{id}/
```

Backend:
- Checks if file is `completed`.
- Generates signed GET URL (short TTL).
- Returns URL + Metadata.

Client:
- Streams directly from R2/CDN.

---

# 9. Signed URL Properties (Critical Understanding)

Signed URLs:
- Cryptographically signed
- Time-limited
- Bound to object + method

They:
- Can be copied
- Expire automatically
- Cannot be reused after expiry

This is standard AWS behavior.

---

# 10. Threat Model (What Is / Is Not Protected)

## Protected Against
- Unauthorized access
- URL guessing
- Hotlinking
- Backend overload
- Storage abuse

## Not Protected Against (By Design)
- Screen recording
- Download during valid window
- Malicious authorized users

Solving those requires DRM (out of MVP scope).

---

# 11. MVP vs Full System (Backend Perspective)

## MVP
- Signed URLs
- Private buckets
- Role-based API
- In-app admin panel (Basic)
- Admin/moderator messaging via WebSockets (Real-time).
- No transcoding
- No analytics

## Full System (Later)
- Web admin dashboard
- Admin chat via WebSockets
- HLS streaming
- Bulk upload UI
- Rate limiting
- Audit logs
- Analytics
- DRM (optional, expensive)

Core architecture does not change.


---

# 12. Storage Usage & Deployment

## Provider
- **Cloudflare R2**

## Authentication
- Access Key ID / Secret Access Key via Environment Variables (Django settings).

## Environments
- Dev Bucket
- Prod Bucket

---

# 13. Backend Tech Stack

- Django
- Django REST Framework
- PostgreSQL
- boto3 (AWS SDK)
- JWT auth

Django logic = CRUD + orchestration.

---

# 14. Final Mental Model

- Backend = authority
- S3 = vault
- Signed URL = temporary permission slip
- Client = untrusted executor

This model is production-proven and scalable.

---

# 15. API Standards

## 15.0 API Prefixes
- **Public API**: `api/public/...` (Read-only, no authentication required).
- **Management API**: `api/chat/...`, `api/content/...`, `api/sections/...`, `api/users/...` (Full CRUD, requires Moderator/Admin authentication).
- **Admin API**: `api/admin/...` (Super Admin only endpoints for global oversight).

## 15.1 Global Pagination
- **Default Page Size**: 10 items per page.
- **Query Parameter**: `?page=<number>`
- **Response Format**:
  ```json
  {
    "count": 102,
    "next": "http://api.example.com/resource/?page=2",
    "previous": null,
    "results": [ ... ]
  }
  ```

## 15.2 Filtering & Search
- **Filtering**: Use exact field names (e.g., `?is_active=true` or `?created_by=5`).
- **Search**: Use `?search=<term>` for fuzzy matching on supported fields (e.g., names, titles).
