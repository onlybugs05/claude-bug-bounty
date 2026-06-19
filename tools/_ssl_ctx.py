"""Shared SSL context creation with certifi fallback.

Consolidates the identical SSL setup from validate.py, learn.py,
_spray_http_form.py, _spray_oauth.py, and h1_mutation_idor.py.

Usage:
    from tools._ssl_ctx import get_ssl_context, get_permissive_ssl_context
"""
from __future__ import annotations

import ssl


def get_ssl_context() -> ssl.SSLContext:
    """Return an SSL context, using certifi certs when available.

    Falls back to an unverified context when certifi is not installed
    (common on macOS system Python).
    """
    ctx = ssl.create_default_context()
    try:
        import certifi
        ctx = ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    return ctx


def get_permissive_ssl_context() -> ssl.SSLContext:
    """Return an SSL context that skips certificate verification.

    Used by spray modules and tools that target staging environments
    with self-signed certs.
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx
