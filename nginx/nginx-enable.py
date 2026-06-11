#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

sys.path.insert(0, "/usr/local/sbin/_lib")
from common import run_cmd
from config import NGINX_CONFIG_PATH
from formatting import (
    print_error,
    print_header,
    print_info,
    print_step,
    print_success,
)

AVAILABLE_DIRS = {
    "sites": (
        NGINX_CONFIG_PATH / "sites-available",
        NGINX_CONFIG_PATH / "sites-enabled",
    ),
    "streams": (
        NGINX_CONFIG_PATH / "streams-available",
        NGINX_CONFIG_PATH / "streams-enabled",
    ),
}


def find_config(site_name: str) -> tuple[Path, Path]:
    """Find sitename.conf in sites-available or streams-available.
    Returns (src, dest_dir) or exits with error."""
    filename = f"{site_name}.conf"

    for kind, (available, enabled) in AVAILABLE_DIRS.items():
        candidate = available / filename
        if candidate.exists():
            print_info(f"Found {filename} in {kind}-available")
            return candidate, enabled

    print_error(
        f"Config '{filename}' not found in sites-available or streams-available"
    )
    sys.exit(1)


