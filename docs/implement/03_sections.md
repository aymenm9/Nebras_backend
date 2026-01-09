# Sections Management Guide

This document defines the workflows for managing the content hierarchy.
**Structure**: Main Section -> Sub Section -> Secondary Sub Section.

## Workflow 1: Main Sections (Super Admin)
Top-level categories (e.g., "Books").

### Step 1: List & Search
- **Endpoint**: `GET /api/sections/main/`
- **Params**: `?search=<term>`
- **Response**:
  ```json
  [
    { "id": 1, "name": "Books", "order_index": 0 }
  ]
  ```

### Step 2: Create
- **Endpoint**: `POST /api/sections/main/`
- **Body**:
  ```json
  { "name": "New Section", "order_index": 0 }
  ```

---

## Workflow 2: Sub Sections (Moderators)
Children of Main Sections.

### Step 1: Select Parent
- **Action**: User must select a `main_section_id` from Workflow 1.

### Step 2: List Children
- **Endpoint**: `GET /api/sections/sub/?main_section=<main_section_id>`
- **Response**:
  ```json
  [
    { "id": 5, "name": "History", "main_section": 1 }
  ]
  ```

### Step 3: Create Sub Section
- **Endpoint**: `POST /api/sections/sub/`
- **Body**:
  ```json
  {
    "main_section": 1,
    "name": "History"
  }
  ```

---

## Workflow 3: Secondary Sub Sections (Moderators)
Children of Sub Sections.

### Step 1: Select Parent
- **Action**: User must select a `sub_section_id` from Workflow 2.

### Step 2: List Children
- **Endpoint**: `GET /api/sections/secondary/?sub_section=<sub_section_id>`
- **Response**:
  ```json
  [
    { "id": 10, "name": "19th Century", "sub_section": 5 }
  ]
  ```

### Step 3: Create Secondary Section
- **Endpoint**: `POST /api/sections/secondary/`
- **Body**:
  ```json
  {
    "sub_section": 5,
    "name": "19th Century"
  }
  ```
