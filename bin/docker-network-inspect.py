#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, "/usr/local/sbin/_lib")
from formatting import get_input, print_error, print_info, print_success


def inspect_docker_network(container_name: str) -> None:
    result = subprocess.run(
        ["docker", "inspect", container_name],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
