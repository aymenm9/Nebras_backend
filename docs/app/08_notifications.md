# Notifications Module

## Overview
The Notifications module handles device registration and the delivery of push notifications to users via Firebase Cloud Messaging (FCM).

## Architecture
- **Device Management**: Users register their devices (Android/iOS) with a unique FCM token.
- **Provider**: Firebase Admin SDK is used to send messages.
- **Failover**: If a notification fails to send, the device is marked as `inactive`.

## Models
### Device
Stores user device tokens.
- `user`: ForeignKey to User.
- `token`: Unique FCM token.
- `platform`: `android` or `ios`.
- `is_active`: Boolean status.
- `created_at` / `updated_at`: Timestamps.

## Workflows
1. **Registration**: Client sends FCM token to backend on app launch/login.
2. **Sending**: Backend triggers `send_message(device, title, body)` utility.
3. **Deactivation**: Client requests deactivation on logout.
