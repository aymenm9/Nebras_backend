import logging
import time

logger = logging.getLogger('request_logger')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        # Get IP Address (handles proxy/load balancers if present)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        response = self.get_response(request)

        # Calculate response duration
        duration = time.time() - start_time
        
        log_message = (
            f"IP: {ip} | {request.method} {request.get_full_path()} | "
            f"Status: {response.status_code} | Duration: {duration:.2f}s"
        )
        
        # Distinct logging based on status codes
        if response.status_code >= 500:
            logger.error(log_message)
        elif response.status_code >= 400:
            # Capture response content for detailing 400 errors
            error_reason = ""
            if not getattr(response, 'streaming', False):
                try:
                    error_reason = response.content.decode('utf-8', errors='ignore')[:1000] # Limit length
                    log_message += f" | Reason: {error_reason}"
                except Exception:
                    pass
            logger.warning(log_message)
        else:
            logger.info(log_message)

        return response
