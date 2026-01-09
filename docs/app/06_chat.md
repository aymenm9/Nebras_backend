# 06 Chat & Messaging

Internal communication system for Moderators and Super Admins using WebSockets for real-time updates and REST for file management/history.

## Authentication
- **REST**: Standard JWT Bearer token in Header.
- **WebSocket**: JWT passed via Query Parameter: `ws://...?token=<access_token>`.
  - Handled by `chat.middleware.TokenAuthMiddleware`.
  - Invalid tokens result in `AnonymousUser`, causing the connection to close.

## Endpoints (REST)

### Messages
- `GET /api/chat/messages/`: List all chat messages (History).
  - **Ordering**: Newest first.
- `GET /api/chat/messages/<id>/`: Get specific message details.
- `PATCH /api/chat/messages/<id>/`: Update a message.
- `DELETE /api/chat/messages/<id>/`: Delete a message.

### Files
- `GET /api/chat/files/`: List files uploaded by the current user.
- `POST /api/chat/files/`: Upload a new file (Max 10MB).
  - **Note**: Files are uploaded orphan (no message ID) first, then linked during message creation via WebSocket.
- `GET /api/chat/files/<id>/`: Get file details.
- `PATCH /api/chat/files/<id>/`: Update file.
- `DELETE /api/chat/files/<id>/`: Delete file.

---

## WebSocket Protocol

**URL**: `ws://<domain>/ws/chat/?token=<access_token>`

### 1. Connection
- **On Connect**: Server accepts connection and immediately sends `type: "history"` event with the last 50 messages.
- **On Fail**: Connection closes if token is invalid or missing.

### 2. Client -> Server Events
Send a JSON object to the WebSocket:

```json
{
  "type": "text",          // "text" or "file" (informational)
  "message": "Hello!",     // The text content
  "file_ids": [12, 14]     // Optional: Array of file IDs uploaded via REST
}
```

### 3. Server -> Client Events
The server broadcasts these events to all connected clients:

#### New Message (`type: "message"`)
```json
{
  "type": "message",
  "message_id": 123,
  "message": "Hello!",
  "username": "aymen",
  "timestamp": "2024-01-01T12:00:00Z",
  "message_type": "text",
  "files": [
    {
        "id": 12,
        "url": "/media/chat_files/image.png",
        "type": "image/png",
        "size": 1024
    }
  ]
}
```

#### History (`type: "history"`)
Sent on connection. Contains a `messages` array with objects identical to the "New Message" format.

---

## Admin Monitoring (Super Admin Only)
Super Admins use these endpoints via `/api/admin/chat/` to oversee communication.

- `GET /api/admin/chat/messages/`: View all chat logs.
  - **Filters**: `user`.
  - **Search**: `message`, `user__username`, `user__email`.
- `GET /api/admin/chat/messages/<id>/`: View specific message.
- `DELETE /api/admin/chat/messages/<id>/`: Remove inappropriate content.
- `GET /api/admin/chat/files/`: View all uploaded chat files.
- `DELETE /api/admin/chat/files/<id>/`: Remove shared files.
