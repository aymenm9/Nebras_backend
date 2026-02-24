from rest_framework.throttling import SimpleRateThrottle

class UserLoginRateThrottle(SimpleRateThrottle):
    scope = 'login'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return None  # Only throttle unauthenticated login attempts

        # Try to get username/email from the request payload
        username = request.data.get('username') or request.data.get('email')
        
        if username:
            # Throttle by requested username to prevent brute-forcing a specific account
            # from different IPs
            ident = username
        else:
            # If no username is provided, fallback to IP address throttling
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
