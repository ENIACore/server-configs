#!/usr/bin/env python3

import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from common import ensure_dir, run_cmd, write_lines
from config import F2B_CONFIG_PATH
from formatting import print_header, print_info, print_step, print_success

NGINX_LOG_DIR = "/var/log/nginx"
F2B_JAIL_SRC = F2B_CONFIG_PATH / "jail.local"
F2B_JAIL_DEST = "/etc/fail2ban/jail.local"


def install_fail2ban() -> None:
    result = run_cmd("dpkg -s fail2ban", capture_output=True)
    if result.returncode == 0:
        print_info("fail2ban already installed, skipping")
        return
    print_step("Installing fail2ban...")
    run_cmd("sudo apt update && sudo apt install fail2ban -y")


def generate_jail_local() -> None:
    print_step(f"Generating jail.local at {F2B_JAIL_SRC}...")
    write_lines(
        F2B_JAIL_SRC,
        [
            "[DEFAULT]",
            "bantime = 15m",
