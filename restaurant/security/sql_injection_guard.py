# restaurant/security/sql_injection_guard.py
import re
from django.core.exceptions import SuspiciousOperation
from django.db import models

DANGER = re.compile(
    r'\b(union|select|insert|update|delete|drop|alter|create|exec|script|'
    r'declare|truncate|pg_catalog|information_schema|pg_sleep)\b',
    flags=re.I
)

class SQLInjectionGuardMixin:
    """
    Mixin to harden a Model against accidental raw SQL.
    Usage:
        class MyModel(SQLInjectionGuardMixin, models.Model):
            ...
    """
    @classmethod
    def _validate_sql(cls, sql: str) -> None:
        if DANGER.search(sql):
            raise SuspiciousOperation(
                f"Possible SQL-injection pattern detected: {sql[:100]}"
            )

    @classmethod
    def raw(cls, *args, **kwargs):
        raise SuspiciousOperation("Raw SQL is forbidden on this model.")

    @classmethod
    def extra(cls, *args, **kwargs):
        raise SuspiciousOperation("extra() is forbidden on this model.")