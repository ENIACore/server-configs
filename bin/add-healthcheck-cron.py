#!/usr/bin/env python3

import re
import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from common import run_cmd, write_lines
from formatting import (
    get_input,
    print_error,
    print_header,
    print_info,
    print_step,
    print_success,
    print_warning,
)

CRON_FILE = "/etc/cron.d/healthchecks"
CRON_SCHEDULE = "*/2 * * * *"


def validate_url(url: str) -> bool:
    return bool(re.match(r"^https?://", url))


def main() -> None:
    print_header("HEALTHCHECKS.IO CRON SETUP")

    print_info("This script adds a system-wide cron job that pings your healthchecks.io URL every 2 minutes.")
    print_warning("Configure your check on healthchecks.io with:")
    print_warning("  Period:        2 minutes")
    print_warning("  Grace period:  6 minutes")
    print()

    url = get_input("Enter your healthchecks.io ping URL")
    if not url:
        print_error("No URL provided. Aborting.")
        sys.exit(1)

    if not validate_url(url):
        print_error("URL must start with http:// or https://. Aborting.")
        sys.exit(1)

    print_step(f"Writing system cron job to {CRON_FILE}...")
