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

