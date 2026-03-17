# Logging Strategy Documentation

This document explains the logging configuration setup for the Nebras backend.

## 🛠️ Overview

The logging strategy comprises:
1.  **Standard LOGGING dictionary** in `settings.py` adding `console` output.
2.  **`RequestLoggingMiddleware`** in `main/middleware.py` that intercepts all requests to log:
    *   Client IP Address (handles loaded-balancers / proxies via `HTTP_X_FORWARDED_FOR`).
    *   Request Method & Path.
    *   Response Status Code.
    *   Response Duration.

---

## 🚦 Request Logging Levels

Based on the response status code, logs are emitted at different levels:
*   🟢 **2xx & 3xx**: `INFO` level.
*   🟡 **4xx** (Bad Request, 404, etc.): `WARNING` level.
*   🔴 **5xx** (Server Errors): `ERROR` level.

### Output Format
```text
[LEVEL] [TIMESTAMP] [MODULE] [PROCESS] [THREAD] IP: [IP] | [METHOD] [PATH] | Status: [CODE] | Duration: [TIME]s
```

---

## 📝 Custom Logging Usage

To log custom messages inside your views, tasks, or utilities, use standard Python logging:

```python
import logging

# Initialize logger for the current module
logger = logging.getLogger(__name__)

def my_view(request):
    # Log information
    logger.info("This is an info log message")
    
    try:
        # Some critical operation
        pass
    except Exception as e:
        # Log error
        logger.error(f"Error occurred: {e}")
```

All custom logs will automatically flow to the console formatter set in `settings.py`.
