# Chat Implementation Guide

This document defines the exact workflows for implementing the frontend chat features. Follow these steps sequentially.

## 1. Authentication Setup
All requests require a **JWT Access Token**.
- **REST Headers**: `Authorization: Bearer <your_access_token>`
- **WebSocket URL**: `ws://<domain>/ws/chat/?token=<your_access_token>`

---

## 2. Workflow: Standard Chat (Moderators & Admins)
This is the main chat interface used by both Moderators and Super Admins.

### Step 1: Initialize & Connect
1.  **Connect** to the WebSocket URL.
2.  **Listen** for the first message. It will be of type `"history"`.
3.  **Render** the list of messages provided in the `messages` array.

### Step 2: Handling Valid Events
Listen for incoming JSON messages and handle based on `type`:

| Type | Action |
| :--- | :--- |
| `history` | Replace/Hydrate the message list with `event.messages`. |
| `message` | Append the new message object (`event`) to the bottom of the chat list. |

### Step 3: Sending Text Messages
Send the following JSON payload to the open WebSocket:
```json
{
  "message": "Hello world!"
}
```

### Step 4: Sending Files (2-Step Process)
To send files (Images, PDFs, etc.):

**A. Upload File via REST**
- **Endpoint**: `POST /api/chat/files/`
- **Body**: `multipart/form-data` with key `file`.
- **Response**:
  ```json
  { "id": 105, "file": "...", "user": 1 }
  ```
- **Action**: Save the `id` (e.g., `105`).

**B. Send WebSocket Message**
Send the message including the `file_ids` array:
```json
{
  "message": "Check out this document",
  "file_ids": [105]
}
```
*Result: The server will link the file to this message and broadcast it to everyone.*

---

## 3. Workflow: Admin Monitoring (Super Admin Only)
This is a **separate view** (e.g., "Audit Logs") visible only to Super Admins.

### Step 1: Browse Logs (REST)
- **Endpoint**: `GET /api/admin/chat/messages/`
- **Params**: `?page=1`
- **Action**: Render the list of messages. This endpoint shows ALL messages from ALL users (unlike the standard chat which essentially shows the same but this is for moderation).

### Step 2: Delete Content
To remove inappropriate content:
- **Endpoint**: `DELETE /api/admin/chat/messages/<id>/`
- **Action**: Remove the item from the UI upon success (204 No Content).

---

## 4. JSON Schemas

### Message Object (Received via WS & REST)
```json
{
  "id": 123,
  "username": "aymen_mod",
  "message": "Project update attached.",
  "timestamp": "2024-01-09T12:00:00Z",
  "files": [
    {
      "id": 105,
      "url": "https://r2.cloudflarestorage.com/.../file.pdf",
      "type": "application/pdf",
      "size": 10240
    }
  ]
}
```

### WebSocket Event: History
```json
{
  "type": "history",
  "messages": [ { ...Message Object... }, { ... } ]
}
```

### WebSocket Event: New Message
```json
{
  "type": "message",
  "message_id": 123,
  "username": "aymen_mod",
  "message": "Hello!",
  "timestamp": "...",
  "files": []
}
```
