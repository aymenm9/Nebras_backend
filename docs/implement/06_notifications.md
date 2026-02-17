# Notifications API Guide

This document covers the endpoints for managing devices and receiving notifications.

## 1. Register Device
Update or create a device token for the current user.

- **Endpoint**: `POST /api/notifications/devices/`
- **Authentication**: `Bearer <token>`
- **Body**:
  ```json
  {
      "token": "<FCM_TOKEN_STRING>",
      "platform": "android|ios"
  }
  ```
- **Response** (201 Created):
  ```json
  {
      "id": 1,
      "token": "...",
      "platform": "android",
      "is_active": true
  }
  ```

## 2. Deactivate Device
Deactivate the current user's registered device.
*Note: This endpoint currently acts on the first device found for the user.*

- **Endpoint**: `POST /api/notifications/devices/deactivate/`
- **Authentication**: `Bearer <token>`
- **Response** (200 OK):
  ```json
  {
      "message": "Device deactivated successfully"
  }
  ```

## 3. Delete Device
Permanently remove a device.

- **Endpoint**: `DELETE /api/notifications/devices/<id>/`
- **Authentication**: `Bearer <token>`
- **Response** (204 No Content).
