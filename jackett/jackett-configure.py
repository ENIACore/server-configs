#!/usr/bin/env python3

import json
import re
import subprocess
import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from checks import require_dir
from config import prompt_and_save, require_config_value
from formatting import (
    get_input,
    print_error,
    print_header,
    print_info,
    print_step,
    print_success,
    print_warning,
)

QBIT_CONTAINER_NAME = "qbittorrent"
JACKETT_CONTAINER_NAME = "jackett"
JACKETT_URL = "http://jackett.internal:9117"
JACKETT_CONFIG_PATH_IN_QBIT = "/config/data/nova3/engines/jackett.json"
JACKETT_API_KEY_PATTERN = re.compile(r"^[a-zA-Z0-9]{32}$")


def _container_running(name: str) -> bool:
    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True,
        text=True,
    )
    return name in result.stdout.splitlines()


def _docker_exec(
    container: str, cmd: list[str], stdin: str | None = None
) -> subprocess.CompletedProcess:
    args = ["docker", "exec"]
    if stdin is not None:
        args.append("-i")
    args.append(container)
    args.extend(cmd)
    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        input=stdin,
    )
