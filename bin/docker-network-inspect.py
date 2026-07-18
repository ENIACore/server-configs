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
        print_error(f"Failed to inspect container '{container_name}'")
        print_error(result.stderr.strip())
        sys.exit(1)

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print_error("Failed to parse docker inspect output")
        sys.exit(1)

    if not data:
        print_error(f"No data returned for container '{container_name}'")
        sys.exit(1)

    networks = data[0].get("NetworkSettings", {}).get("Networks", {})

    if not networks:
        print_info(f"No networks found for container '{container_name}'")
