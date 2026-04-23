#!/usr/bin/env python3

import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from common import ensure_dir, run_cmd
from config import UFW_CONFIG_PATH
from formatting import (
    print_header,
    print_info,
    print_step,
    print_success,
    print_warning,
)

BLOCKLIST_URL = "https://gist.githubusercontent.com/arter97/2b71e193700ab002c75d1e5a0e7da6dc/raw/firewall.sh"
BLOCKLIST_SCRIPT = UFW_CONFIG_PATH / "blocklist.sh"

UFW_RULES = [
    ("22/tcp", "OpenSSH"),
    ("80/tcp", "HTTP"),
    ("443/tcp", "HTTPS"),
    ("25565/tcp", "Minecraft"),
]


def install_packages() -> None:
    print_step("Installing required packages...")
    run_cmd("sudo apt install iptables ipset ufw cron curl wget rsyslog -y")
