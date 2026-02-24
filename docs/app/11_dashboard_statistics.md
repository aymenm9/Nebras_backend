# Dashboard Statistics Module

## Overview
This module isolates statistical queries specifically designed for dashboards accessed by different user roles, starting with Moderators.

## Purpose
- **Moderator Statistics**: Provides aggregated data scoped strictly to the current `request.user`.
- **Serializers**: Houses the serializers (`TotalsSerializer`, `ContentDistributionSerializer`, etc.) that are also shared by the Super Admin statistics views (located in `admin_apis`).

## Security
- **Authentication**: JWT Authentication (`IsAuthenticated`).
- **Permissions**: **IsModerator** required for moderator endpoints.
