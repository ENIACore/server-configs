#!/usr/bin/env python3

import subprocess
import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from formatting import (
    GREEN,
    RED,
    RESET,
    print_error,
    print_header,
    print_info,
    print_warning,
)

NGINX_CONTAINER_NAME = "server-proxy"
NGINX_LOG_DIR = "/var/log/nginx"
NGINX_ACCESS_LOG = f"{NGINX_LOG_DIR}/access.log"
NGINX_ERROR_LOG = f"{NGINX_LOG_DIR}/error.log"
TAIL_LINES = 100


def container_exists() -> bool:
    result = subprocess.run(
        ["docker", "ps", "-a", "--format", "{{.Names}}"],
        capture_output=True,
        text=True,
    )
    return NGINX_CONTAINER_NAME in result.stdout.splitlines()


def container_running() -> bool:
    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True,
        text=True,
    )
    return NGINX_CONTAINER_NAME in result.stdout.splitlines()


def logs_exist() -> bool:
    from pathlib import Path

    return Path(NGINX_ACCESS_LOG).exists() or Path(NGINX_ERROR_LOG).exists()


def tail_logs() -> None:
    access_label = f"{GREEN}[ACCESS]{RESET}"
    error_label = f"{RED}[ERROR]{RESET}"

