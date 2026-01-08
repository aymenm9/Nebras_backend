# Sections Management Guide

This guide details how to manage the content hierarchy. The structure is strict: **Main -> Sub -> Secondary**.

## 1. Workflow Tips
*   **To create a Sub Section**, you must first select a **Main Section** to attach it to.
*   **To create a Secondary Sub Section**, you must first select a **Sub Section**.
*   **Filtering**: You can currently list all sections. In the future, we may add filtering by parent ID (e.g., `?main_section=1`).

---

## 2. Main Sections (Super Admin Only)
**Purpose**: The top-level categories (e.g., "Books", "Audio").

### List All
*   **GET** `/api/sections/main/`
*   **Response**: `[ { "id": 1, "name": "Books", ... }, ... ]`
*   **Search**: `/api/sections/main/?search=Books`

### Create
*   **POST** `/api/sections/main/`
*   **Body**:
    ```json
    {
      "name": "New Main Section",
      "order_index": 0
    }
    ```

### Update
*   **PATCH** `/api/sections/main/<id>/`
*   **Body**: `{ "name": "Updated Name" }`

### Delete
*   **DELETE** `/api/sections/main/<id>/`

---

## 3. Sub Sections (Moderators)
**Purpose**: Children of Main Sections (e.g., "Non-Fiction" inside "Books").

### List All
*   **GET** `/api/sections/sub/`
*   **Filter by Main Section**: `/api/sections/sub/?main_section=1`
*   **Search**: `/api/sections/sub/?search=History`

### Create
*   **POST** `/api/sections/sub/`
*   **Prerequisite**: You need a `main_section` ID (fetched from the Main Section list).
*   **Body**:
    ```json
    {
      "main_section": 1,
      "name": "History"
    }
    ```

### Update
*   **PATCH** `/api/sections/sub/<id>/`
*   **Body**: `{ "name": "Updated History" }`

### Delete
*   **DELETE** `/api/sections/sub/<id>/`

---

## 4. Secondary Sub Sections (Moderators)
**Purpose**: Children of Sub Sections (e.g., "19th Century" inside "History").

### List All
*   **GET** `/api/sections/secondary/`
*   **Filter by Sub Section**: `/api/sections/secondary/?sub_section=5`
*   **Search**: `/api/sections/secondary/?search=19th`

### Create
*   **POST** `/api/sections/secondary/`
*   **Prerequisite**: You need a `sub_section` ID.
*   **Body**:
    ```json
    {
      "sub_section": 5,
      "name": "19th Century"
    }
    ```

### Update
*   **PATCH** `/api/sections/secondary/<id>/`
*   **Body**: `{ "name": "Updated Name" }`

### Delete
*   **DELETE** `/api/sections/secondary/<id>/`

---

## 5. Public Access (No Auth)
Use these for the client application (Android/Web public view).

*   **Main Sections**:
    *   List: `GET /api/public/sections/main/`
    *   Detail: `GET /api/public/sections/main/<id>/`
*   **Sub Sections**:
    *   List: `GET /api/public/sections/sub/`
    *   Detail: `GET /api/public/sections/sub/<id>/`
*   **Secondary Sub Sections**:
    *   List: `GET /api/public/sections/secondary/`
    *   Detail: `GET /api/public/sections/secondary/<id>/`
