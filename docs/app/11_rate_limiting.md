# Nebras Rate Limiting Strategy

This document outlines the rate limiting rules implemented in the Nebras backend to protect resources and prevent abuse. The implementation uses a mix of Django REST Framework (DRF) built-in throttles, custom DRF throttles, and Django Cache for WebSockets.

## 1. Global REST API Rate Limits
These rules apply to all standard REST endpoints unless explicitly overridden.

*   **Anonymous Users:** `100 requests / minute` (Protects public APIs from scraping)
*   **Authenticated Users:** `1000 requests / minute` (General safety net for logged-in users and admins)

## 2. Authentication & Security
Brute force attacks on logins or password resets are strictly throttled.

*   **Login (`api/users/login/`):** `5 attempts / minute`
    *   **Custom Strategy (`UserLoginRateThrottle`):** Throttling is applied based on the provided `username` or `email` in the request body. If none are provided, it falls back to the IP address. This effectively prevents distributed attacks attempting to breach a specific account from multiple IP addresses.
*   **Password Change (`api/users/me/password/change/`):** `3 attempts / minute` (Scope: `password_change`, per user)

## 3. Resource-Intensive Operations
Endpoints like uploading files and content are limited to prevent server/storage exhaustion.

*   **File & Content Uploads:** `20 requests / minute` (Scope: `uploads`)
    *   *Applies to:* Creating Youtube Videos and R2 File uploads (starting/initiating multipart uploads).

## 4. Interactive Endpoints (Chat WebSockets)
Since Django Channels (WebSockets) does not use DRF throttling classes, a custom rate limiter is implemented in the chat consumer.

*   **Chat Send Message (WebSocket):** `20 messages / minute` per user.
    *   **Implementation:** The consumer checks the Django cache for recent message timestamps within the last 60 seconds (`RATE_LIMIT = 20`, `WINDOW = 60`). If the limit is exceeded, the server returns an error message: `{"type": "error", "message": "Rate limit exceeded..."}` without broadcasting the message.
