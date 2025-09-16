import re
from django.http import HttpResponseForbidden


# Middleware to enhance security by filtering malicious requests and adding security headers
# USED IN: restaurant/settings.py

class SecurityMiddleware:
    """
    Basic middleware to protect Django project against common malware patterns
    and enforce security headers.
    """

    MALICIOUS_PATTERNS = [
        re.compile(r"<script.*?>.*?</script>", re.IGNORECASE),   # XSS
        re.compile(r"(?:union.*select.*\()", re.IGNORECASE),     # SQL Injection
        re.compile(r"(?:\bor\b.+?=.+)", re.IGNORECASE),          # Boolean-based SQLi
        re.compile(r"(?:\bdrop\s+table\b)", re.IGNORECASE),      # DROP TABLE attack
        re.compile(r"(?:\binsert\s+into\b)", re.IGNORECASE),     # INSERT attack
        re.compile(r"(?:<iframe.*?>)", re.IGNORECASE),           # Hidden iframe
        re.compile(r"(?:javascript:)", re.IGNORECASE),           # JS protocol injection
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Block suspicious query strings and POST data
        if self.is_malicious(request):
            return HttpResponseForbidden("Malicious request blocked.")

        response = self.get_response(request)

        # Add security headers
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["X-XSS-Protection"] = "1; mode=block"
        response["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; object-src 'none'"
        response["Referrer-Policy"] = "same-origin"

        return response

    def is_malicious(self, request):
        """Check GET/POST params for malicious patterns"""
        all_data = " ".join([
            " ".join(request.GET.values()),
            " ".join(request.POST.values()),
        ])
        for pattern in self.MALICIOUS_PATTERNS:
            if pattern.search(all_data):
                return True
        return False
