# restaurant/security/middleware.py
import re
import functools
from typing import Any, Callable, Optional
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import SuspiciousOperation
from django.db import connection
from django.db.backends.utils import CursorWrapper  # <- NEW
from security.sql_injection_guard import DANGER


class SecurityMiddleware:
    # your existing security middleware (unchanged)
    MALICIOUS_PATTERNS = [
        re.compile(r"<script.*?>.*?</script>", re.IGNORECASE),  # XSS
        re.compile(r"(?:union.*select.*\()", re.IGNORECASE),    # SQL Injection
        re.compile(r"(?:\bor\b.+?=.+)", re.IGNORECASE),         # boolean SQLi
    ]

    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request):
        if self.is_malicious(request):
            return HttpResponseForbidden("Malicious request blocked.")
        response = self.get_response(request)
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["X-XSS-Protection"] = "1; mode=block"
        response["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; object-src 'none'"
        response["Referrer-Policy"] = "same-origin"
        return response

    def is_malicious(self, request):
        all_data = " ".join([*request.GET.values(), *request.POST.values()])
        for pattern in self.MALICIOUS_PATTERNS:
            if pattern.search(all_data):
                return True
        return False


class SQLInjectionMiddleware(MiddlewareMixin):
    """
    Middleware that wraps connection.cursor() so each cursor.execute(...) call
    is scanned for dangerous SQL patterns before being sent to the DB.
    """

    def __init__(self, get_response: Callable):
        super().__init__(get_response)

    def __call__(self, request):
        # tell Pylance this is never None
        original_cursor: Callable[..., CursorWrapper] = connection.cursor

        def safe_cursor(*args: Any, **kwargs: Any) -> CursorWrapper:
            cursor = original_cursor(*args, **kwargs)
            # same here
            original_execute: Callable = cursor.execute

            @functools.wraps(original_execute)
            def guarded_execute(sql: Any, params: Optional[Any] = None) -> Any:
                sql_text = str(sql) if sql else ""
                if DANGER.search(sql_text):
                    raise SuspiciousOperation(
                        f"Potential SQL injection attempt detected: {sql_text[:200]}"
                    )
                return original_execute(sql, params)

            cursor.execute = guarded_execute
            return cursor

        connection.cursor = safe_cursor
        try:
            response = self.get_response(request) # pyright: ignore[reportOptionalCall]
        finally:
            connection.cursor = original_cursor  # restore
        return response