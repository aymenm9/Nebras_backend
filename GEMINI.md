# 📜 Project-Specific Rules & Coding Standards

This document defines the rules and preferences for any AI agent working on the **Nebras Backend** project. These rules must be followed strictly to maintain consistency and simplicity.

## 🛠️ General Principles

*   **Simplicity Over Complexity**: Prioritize simple, readable code over "clever" or overly engineered solutions.
*   **Keep it Simple**: Don't overcomplicate stuff. Focus on the core request without adding unnecessary abstraction.
*   **Be Direct**: Perform only the tasks explicitly requested. Do not suggest or implement extra features without approval.
*   **One Step at a Time**: Work on one feature or task at a time. Do not rush or bundle multiple features.
*   **Documentation First**: Every new feature must be documented in the `docs/` folder, explaining how it works and how to use it.

## 🐍 Backend (Django/DRF) Standards

*   **DRF Generics First**: For standard CRUD operations, always use Django REST Framework's generic views (`ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`, etc.).
*   **Views.APIView for Complexity**: Only use `APIView` if the logic requires significant customization that generic views cannot handle cleanly.
*   **Minimal Comments**: Avoid cluttering the code with comments. If logic is complex, explain it here in the chat or in the project documentation.
*   **Explicit Imports**: Always use explicit imports (e.g., `from rest_framework import generics` instead of `from rest_framework import *`).

## 📁 Documentation Policy

*   Any changes to the system architecture or API must be reflected in `docs/00_overview.md` or a new specific documentation file.
*   **Documentation Folders**:
    *   `docs/app/`: Technical documentation for the backend application.
    *   `docs/implement/`: Implementation guides and API usage instructions for the frontend developers.
*   Explain the "How-To" for every feature added.

---
*Created on 2025-12-24 to guide all future AI development on this repository.*
