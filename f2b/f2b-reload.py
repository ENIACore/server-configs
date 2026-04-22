#!/usr/bin/env python3

import subprocess
import sys
import time

sys.path.insert(0, "/usr/local/sbin/_lib")
from common import ensure_dir, run_cmd, write_lines
from config import F2B_CONFIG_PATH
from formatting import (
    print_error,
    print_header,
    print_info,
    print_step,
    print_success,
)

NGINX_LOG_DIR = "/var/log/nginx"
NGINX_LOG_PLACEHOLDERS = ["access.log", "error.log"]
F2B_JAIL_SRC = F2B_CONFIG_PATH / "jail.local"
F2B_JAIL_DEST = "/etc/fail2ban/jail.local"
F2B_PING_RETRIES = 10


def wait_for_fail2ban():
    """Poll fail2ban-client ping until ready or timeout."""
    for _ in range(F2B_PING_RETRIES):
        result = subprocess.run(
            ["sudo", "fail2ban-client", "ping"],
            capture_output=True,
        )
