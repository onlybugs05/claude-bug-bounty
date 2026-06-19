"""Shared ANSI color constants and log helpers.

Consolidates the color definitions and logging functions that were
duplicated across hunt.py, validate.py, learn.py, intel_engine.py,
token_scanner.py, mindmap.py, engine.py, agent.py, and others.

Usage:
    from tools._colors import RED, GREEN, YELLOW, CYAN, BOLD, DIM, NC, log
"""

# Standard ANSI escape codes (8-color safe).
RED = "\033[0;31m"
RED_BRIGHT = "\033[91m"
GREEN = "\033[0;32m"
GREEN_BRIGHT = "\033[92m"
YELLOW = "\033[1;33m"
YELLOW_BRIGHT = "\033[93m"
CYAN = "\033[0;36m"
CYAN_BRIGHT = "\033[96m"
BLUE = "\033[0;34m"
BLUE_BRIGHT = "\033[94m"
MAGENTA = "\033[0;35m"
BOLD = "\033[1m"
DIM = "\033[2m"
NC = "\033[0m"

# Alias used by several files that call it RESET instead of NC.
RESET = NC

_LOG_COLORS = {"ok": GREEN, "err": RED, "warn": YELLOW, "info": CYAN}
_LOG_SYMBOLS = {"ok": "+", "err": "-", "warn": "!", "info": "*"}


def log(level: str, msg: str) -> None:
    """Print a bracketed log line: ``[+] msg``, ``[-] msg``, etc."""
    color = _LOG_COLORS.get(level, "")
    symbol = _LOG_SYMBOLS.get(level, "*")
    print(f"{color}{BOLD}[{symbol}]{NC} {msg}")
