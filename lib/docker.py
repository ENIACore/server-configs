#!/usr/bin/env python3

import subprocess
import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from config import (
    DOCKER_NETWORK_GATEWAY,
    DOCKER_NETWORK_NAME,
    DOCKER_NETWORK_SUBNET,
)
from formatting import (
    GREY,
    RESET,
    YELLOW,
    print_error,
    print_group_end,
    print_group_start,
    print_group_step,
    print_info,
    print_step,
    print_success,
)


def ensure_network() -> None:
    """Ensure the Docker network exists, creating it if necessary."""
    probe = subprocess.run(
        ["docker", "network", "inspect", DOCKER_NETWORK_NAME],
        capture_output=True,
    )

    if probe.returncode == 0:
        print_info(f"Validated Docker network '{DOCKER_NETWORK_NAME}' exists")
        return

    print_step(f"Creating Docker network '{DOCKER_NETWORK_NAME}'")

    result = subprocess.run(
        [
            "docker",
            "network",
            "create",
            "--driver",
            "bridge",
            "--subnet",
            DOCKER_NETWORK_SUBNET,
            "--gateway",
            DOCKER_NETWORK_GATEWAY,
            DOCKER_NETWORK_NAME,
        ],
        capture_output=True,
    )

    if result.returncode == 0:
        print_success(f"Docker network '{DOCKER_NETWORK_NAME}' created")
    else:
        print_error(
            f"Failed to create Docker network '{DOCKER_NETWORK_NAME}' "
            "(subnet or gateway already in use, choose a new range)"
        )
        sys.exit(1)


def pull_image(image: str) -> None:
    """Pull the latest version of an image, exiting on failure."""
    print_step(f"Pulling image '{image}'")

    result = subprocess.run(
        ["docker", "pull", image], capture_output=True, text=True
    )

    if result.returncode == 0:
        print_success(f"Image '{image}' is up to date")
    else:
        print_error(f"Failed to pull image '{image}': {result.stderr.strip()}")
        sys.exit(1)


def remove_container(name: str) -> None:
    """Stop and remove an existing container so it can be recreated."""
    probe = subprocess.run(
        ["docker", "container", "inspect", name],
        capture_output=True,
    )

    if probe.returncode != 0:
        return

    print_step(f"Removing existing container '{name}' to recreate it")

    result = subprocess.run(
        ["docker", "rm", "-f", name], capture_output=True, text=True
    )

    if result.returncode == 0:
        print_success(f"Removed existing container '{name}'")
    else:
        print_error(
            f"Failed to remove container '{name}': {result.stderr.strip()}"
        )
        sys.exit(1)


def run_container(
    name: str,
    image: str,
    opts: list[str],
    notes: list[str] | None = None,
) -> None:
    """Pull the image, replace any existing container, and run it.

    Pulls first so a failed pull leaves the existing container running.

    Args:
        name:  Container name (passed as --name and used in output).
        image: Image to pull and run (e.g. 'nginx:latest').
        opts:  All additional docker run args (volumes, network, restart, etc.).
               Do not include 'docker', 'run', '-d', '--name', or the image.
        notes: Optional list of follow-up info lines printed on success.
    """
    pull_image(image)
    remove_container(name)

    print_group_start(f"Starting container '{name}'")

    cmd = ["docker", "run", "-d", "--name", name, *opts, image]
    print_group_step(f"Running: {GREY}{' '.join(cmd)}{RESET}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print_group_end(
            f"Container '{name}' started successfully", success=True
        )
        if notes:
            print_info("")
            print_info("Next steps:")
            for i, note in enumerate(notes, start=1):
                print_info(f"{YELLOW}{i}. {note}{RESET}")
    else:
        err = result.stderr.strip()
        print_group_step(err)
        print_group_end(f"Failed to start container '{name}'", success=False)
        sys.exit(1)
