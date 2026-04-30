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
