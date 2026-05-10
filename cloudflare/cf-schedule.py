#!/usr/bin/env python3

import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from checks import require_server_user
from common import run_cmd, write_lines
from config import require_config_value
from formatting import print_header, print_step, print_success

CF_CRON_FILE = "/etc/cron.d/cloudflare-dns"
CF_CRON_SCHEDULE = "*/5 * * * *"
CF_DNS_SCRIPT = "/usr/local/sbin/cf-update-dns"


def main():
