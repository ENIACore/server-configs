#!/usr/bin/env python3

import re
import subprocess
import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from formatting import (
    get_input,
    print_error,
    print_header,
    print_info,
    print_step,
    print_success,
    print_warning,
)

CRON_COMMENT = "# healthchecks.io ping"
CRON_SCHEDULE = "*/2 * * * *"


def validate_url(url: str) -> bool:
    return bool(re.match(r"^https?://", url))


def get_current_crontab() -> str:
    r = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    if r.returncode != 0:
        return ""
    return r.stdout


def set_crontab(content: str) -> bool:
    r = subprocess.run(["crontab", "-"], input=content, text=True, capture_output=True)
    return r.returncode == 0


def remove_existing_entry(crontab: str) -> str:
    lines = crontab.splitlines(keepends=True)
    filtered = []
    skip_next = False
    for line in lines:
        if line.strip() == CRON_COMMENT:
            skip_next = True
            continue
        if skip_next:
            skip_next = False
            continue
        filtered.append(line)
    return "".join(filtered)


def build_cron_entry(url: str) -> str:
    return f"{CRON_COMMENT}\n{CRON_SCHEDULE} curl -fsS --retry 3 {url} > /dev/null\n"


def main() -> None:
    print_header("HEALTHCHECKS.IO CRON SETUP")

    print_info("This script adds a cron job that pings your healthchecks.io URL every 2 minutes.")
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

    print_step("Reading current crontab...")
    current = get_current_crontab()

    if CRON_COMMENT in current:
        print_warning("Existing healthcheck cron entry found — replacing it.")
        current = remove_existing_entry(current)

    entry = build_cron_entry(url)
    new_crontab = current.rstrip("\n") + ("\n" if current else "") + entry

    print_step("Writing updated crontab...")
    if not set_crontab(new_crontab):
        print_error("Failed to write crontab.")
        sys.exit(1)

    print_success("Cron job added successfully!")
    print_info(f"Schedule: every 2 minutes → {url}")


if __name__ == "__main__":
    main()
