# 02 Authentication

## Endpoints
- `POST /api/users/login/`: Login with `username` (or email) and `password`. Returns JWT tokens and user data.
- `POST /api/users/token/refresh/`: Refresh the access token using the refresh token.
- `GET /api/users/me/`: Get current logged-in user profile (Requires Auth).
