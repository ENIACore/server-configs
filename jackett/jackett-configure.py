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


def check_containers() -> None:
    print_step("Checking qBittorrent container status...")
    if not _container_running(QBIT_CONTAINER_NAME):
        print_error(
            f"qBittorrent container '{QBIT_CONTAINER_NAME}' is not running"
        )
        print_error("Start it before running this script")
        sys.exit(1)
    print_success("qBittorrent container is running")

    if not _container_running(JACKETT_CONTAINER_NAME):
        print_warning(
            "Jackett container is not running — config will be written, "
            "but searches will fail until it is started"
        )


def prompt_api_key() -> str:
    while True:
        api_key = prompt_and_save(
            "JACKETT_API_KEY",
            "Enter Jackett API key (from the top-right of the Jackett web UI)",
            secret=True,
        )

        if JACKETT_API_KEY_PATTERN.match(api_key):
            return api_key

        print_warning(
            "API key doesn't look like a standard 32-character Jackett key"
        )
        confirm = get_input("Use it anyway? (y/N)", default="n")
        if confirm.lower() == "y":
            return api_key


def write_jackett_config(api_key: str) -> None:
    config = {
        "api_key": api_key,
        "url": JACKETT_URL,
        "tracker_first": False,
        "thread_count": 20,
    }
    config_json = json.dumps(config, indent=4)
    engines_dir = JACKETT_CONFIG_PATH_IN_QBIT.rsplit("/", 1)[0]

    print_step(
