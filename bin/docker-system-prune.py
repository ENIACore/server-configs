#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, "/usr/local/sbin/_lib")
from formatting import print_error, print_info, print_success


def prune_docker_system() -> None:
    print_info("Pruning docker containers, volumes, and images...")
    result = subprocess.run(
        ["docker", "system", "prune", "-a", "-f"],
        text=True,
