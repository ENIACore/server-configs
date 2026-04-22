#!/usr/bin/env python3

import sys
from pathlib import Path

sys.path.insert(0, "/usr/local/sbin/_lib")
from checks import ensure_server_user
from common import run_cmd, write_lines
from config import UFW_CONFIG_PATH
from formatting import (
    print_error,
    print_header,
    print_info,
    print_step,
    print_success,
)

UFW_BLOCKLIST_SCRIPT = UFW_CONFIG_PATH / "blocklist.sh"
UFW_CRON_FILE = "/etc/cron.d/server-ufw-blocklist"
UFW_CRON_SCHEDULE = "0 5 * * *"
