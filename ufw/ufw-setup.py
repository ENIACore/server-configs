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


def configure_ufw() -> None:
    print_step("Configuring UFW rules...")
    run_cmd("sudo ufw --force reset")
    run_cmd("sudo ufw default deny incoming")
    run_cmd("sudo ufw default allow outgoing")

    print_step("Allowing SSH, HTTP, HTTPS, and Minecraft...")
    for port, comment in UFW_RULES:
        run_cmd(f"sudo ufw allow {port} comment '{comment}'")


def setup_blocklist() -> None:
    print_step("Downloading IP blocklist updater...")
    run_cmd(f"sudo wget -q {BLOCKLIST_URL} -O {BLOCKLIST_SCRIPT}")
    run_cmd(f"sudo chmod 755 {BLOCKLIST_SCRIPT}")

    print_step("Running initial IP blocklist update...")
    import subprocess

    result = subprocess.run(
        ["sudo", str(BLOCKLIST_SCRIPT)], capture_output=True
    )
    if result.returncode == 0:
        print_info("IP blocklist updated successfully")
    else:
        print_warning("Failed to update IP blocklist, continuing anyway")


