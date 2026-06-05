#!/usr/bin/env python3
import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from formatting import print_error, print_info, print_success

SLEEP_TARGETS = [
    "sleep.target",
    "suspend.target",
    "hibernate.target",
    "hybrid-sleep.target",
]


def mask_sleep_targets() -> None:
    import subprocess

    print_info("Masking sleep/suspend/hibernate targets...")
