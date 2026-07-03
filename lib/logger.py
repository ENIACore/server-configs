#!/usr/bin/env python3
# Logger functionality with rotating logs for server scripts - /usr/local/sbin/_lib/logger.py

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, "/usr/local/sbin/_lib")
from formatting import print_error, print_info

# ------------------------------------------------------------------------------
# Private State
# ------------------------------------------------------------------------------
_SERVER_LOG_FILE: Path | None = None
_SERVER_MAX_LOG_LINES: int = 1000
_SERVER_LOG_COUNT: int = 0
_SERVER_LOG_INITIALIZED: bool = False


# ------------------------------------------------------------------------------
# Public Functions
# ------------------------------------------------------------------------------


def init_logger(log_file: str, max_lines: int = 1000) -> bool:
    """Initialize the logger with a file path and optional max lines.

    Args:
        log_file: Path to log file (required)
        max_lines: Maximum lines before rotation (default: 1000)

    Returns:
        True on success, False on failure
    """
    global \
        _SERVER_LOG_FILE, \
        _SERVER_MAX_LOG_LINES, \
        _SERVER_LOG_COUNT, \
        _SERVER_LOG_INITIALIZED

    if not log_file:
        print_error("ERROR: Log file path is required.")
        print_error("Usage: init_logger(log_file, max_lines=1000)")
        return False

    if not isinstance(max_lines, int) or max_lines <= 0:
        print_error("ERROR: max_lines must be a positive integer.")
        return False

    log_path = Path(log_file)
    log_dir = log_path.parent

    if not log_dir.exists():
        try:
            log_dir.mkdir(parents=True, exist_ok=True)
        except OSError:
            print_error(f"ERROR: Could not create log directory: {log_dir}")
            return False

    _SERVER_LOG_FILE = log_path
    _SERVER_MAX_LOG_LINES = max_lines
    _SERVER_LOG_COUNT = 0
