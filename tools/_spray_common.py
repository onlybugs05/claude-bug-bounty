"""Shared helpers for the spray modules (_spray_http_form, _spray_oauth).

Consolidates the five identical functions that were copy-pasted between
the two spray modules: env, env_required, read_lines, sha256_prefix, audit.

Usage:
    from tools._spray_common import (
        env, env_required, read_lines, sha256_prefix, audit,
        SSL_CTX, USER_AGENT,
    )
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone

from tools._ssl_ctx import get_permissive_ssl_context

SSL_CTX = get_permissive_ssl_context()
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Bug-Bounty-Research"


def env(name: str, default: str = "") -> str:
    """Read an optional environment variable."""
    return os.environ.get(name, default)


def env_required(name: str) -> str:
    """Read a required environment variable, exiting on failure."""
    v = os.environ.get(name)
    if not v:
        print(f"[-] Missing required env var: {name}", file=sys.stderr)
        sys.exit(1)
    return v


def read_lines(path: str) -> list[str]:
    """Read non-empty lines from a text file."""
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]


def sha256_prefix(s: str) -> str:
    """Return the first 12 hex chars of the SHA-256 of *s*."""
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]


def audit(record: dict, audit_log_path: str) -> None:
    """Append a timestamped JSON record to the audit log."""
    record["ts"] = datetime.now(timezone.utc).isoformat()
    with open(audit_log_path, "a") as f:
        f.write(json.dumps(record) + "\n")
