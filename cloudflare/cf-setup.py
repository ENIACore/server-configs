#!/usr/bin/env python3

import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from checks import ensure_server_user
from common import ensure_dir, run_cmd, write_lines
from config import (
    CF_CONFIG_PATH,
    SERVER_USER,
    prompt_and_save,
)
from formatting import print_error, print_header, print_step, print_success


def main():
    print_header("SETTING UP CLOUDFLARE DNS AND CRON JOB")

    CF_API_KEY = prompt_and_save(
