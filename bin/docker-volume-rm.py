#!/usr/bin/env python3
import subprocess
import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from formatting import print_error, print_info, print_success, print_warning


def get_docker_volumes() -> list[str]:
    result = subprocess.run(
        ["docker", "volume", "ls", "-q"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print_error("Failed to list docker volumes")
