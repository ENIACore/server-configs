#!/usr/bin/env python3
# Requirement check functions for server-configs - /usr/local/sbin/_lib/checks.py

import pwd
import subprocess
import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from config import SERVER_USER
from formatting import print_error, print_info, print_success


def _user_exists(username: str) -> bool:
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False


def ensure_server_user() -> None:
    """Ensure server user exists, creating it if necessary."""
    if _user_exists(SERVER_USER):
        print_info(f"Validated system user '{SERVER_USER}' exists")
        return

    print_info(f"System user '{SERVER_USER}' does not exist, creating...")

    result = subprocess.run(
        [
            "sudo",
            "useradd",
            "--system",
            "--no-create-home",
            "--shell",
            "/usr/sbin/nologin",
            "--comment",
            "Server service user",
            SERVER_USER,
        ],
    )

    if result.returncode == 0:
        print_success(f"System user '{SERVER_USER}' created")
    else:
        print_error(f"Failed to create user '{SERVER_USER}'")
        sys.exit(1)


def require_server_user() -> None:
    """Check if server user exists, exit with error if not."""
    if not _user_exists(SERVER_USER):
        print_error(f"ERROR: System user '{SERVER_USER}' does not exist")
        print_error("Run cf-setup or ufw-schedule to create it")
        sys.exit(1)
