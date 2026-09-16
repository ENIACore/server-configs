#!/usr/bin/env python3

import json
import subprocess
import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from formatting import (
    print_error,
    print_header,
    print_info,
    print_step,
    print_success,
    print_warning,
)

# AIO sub-containers are managed exclusively by the master container
AIO_CONTAINERS = {
    "nextcloud-aio-apache",
    "nextcloud-aio-nextcloud",
    "nextcloud-aio-imaginary",
    "nextcloud-aio-fulltextsearch",
    "nextcloud-aio-clamav",
    "nextcloud-aio-redis",
    "nextcloud-aio-database",
    "nextcloud-aio-whiteboard",
    "nextcloud-aio-notify-push",
    "nextcloud-aio-collabora",
    "nextcloud-aio-borgbackup",
    "nextcloud-aio-watchtower",
}
AIO_MASTER = "nextcloud-aio-mastercontainer"
AIO_MASTER_IMAGE = "ghcr.io/nextcloud-releases/all-in-one:latest"


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def docker_available() -> bool:
    return _run(["docker", "info"]).returncode == 0


def update_system_packages() -> None:
    print_header("UPDATING SYSTEM PACKAGES")

    print_step("Running apt-get update...")
    r = subprocess.run(["apt-get", "update", "-qq"])
    if r.returncode != 0:
        print_error("apt-get update failed")
        sys.exit(1)

    print_step("Running apt-get upgrade...")
    r = subprocess.run(["apt-get", "upgrade", "-y"])
    if r.returncode != 0:
        print_error("apt-get upgrade failed")
        sys.exit(1)

    print_step("Running apt-get autoremove...")
    subprocess.run(["apt-get", "autoremove", "-y"])

    print_step("Running apt-get autoclean...")
    subprocess.run(["apt-get", "autoclean"])

    print_success("System packages are up to date")


def _image_id(image: str) -> str:
    r = _run(["docker", "image", "inspect", "--format", "{{.Id}}", image])
    return r.stdout.strip() if r.returncode == 0 else ""


def pull_image(image: str) -> bool:
    """Pull image and return True if a newer version was downloaded."""
    before = _image_id(image)
    r = _run(["docker", "pull", image])
    if r.returncode != 0:
        print_warning(f"Failed to pull {image}: {r.stderr.strip()}")
        return False
    return _image_id(image) != before


def inspect_container(name: str) -> dict | None:
    r = _run(["docker", "inspect", name])
    if r.returncode != 0:
        return None
    data = json.loads(r.stdout)
    return data[0] if data else None


def _build_run_args(info: dict) -> list[str]:
    """Reconstruct docker run flags from docker inspect output."""
    args = []
    hc = info.get("HostConfig", {})
    cfg = info.get("Config", {})

    if hc.get("Init"):
        args.append("--init")

    rp = hc.get("RestartPolicy", {})
    rp_name = rp.get("Name", "no")
    if rp_name and rp_name != "no":
        if rp_name == "on-failure":
            n = rp.get("MaximumRetryCount", 0)
            args += ["--restart", f"on-failure:{n}" if n else "on-failure"]
        else:
            args += ["--restart", rp_name]

    net_mode = hc.get("NetworkMode", "")
    if net_mode not in ("", "default", "bridge"):
        args += ["--network", net_mode]

    for port, bindings in (hc.get("PortBindings") or {}).items():
        for b in bindings or []:
            hip, hport = b.get("HostIp", ""), b.get("HostPort", "")
            if hip and hip not in ("0.0.0.0", "::"):
                args += ["-p", f"{hip}:{hport}:{port}"]
            else:
                args += ["-p", f"{hport}:{port}"]

    for bind in hc.get("Binds") or []:
        args += ["-v", bind]

    bound_sources = {b.split(":")[0] for b in hc.get("Binds") or []}
    for m in info.get("Mounts") or []:
        if m.get("Type") == "volume" and m.get("Name") not in bound_sources:
            args += ["-v", f"{m['Name']}:{m['Destination']}"]

    # Skip HOSTNAME — Docker sets this automatically from the container ID
    for env in cfg.get("Env") or []:
        if not env.startswith("HOSTNAME="):
            args += ["--env", env]

    return args


def _extra_networks(info: dict) -> list[str]:
    """Return networks the container was connected to beyond its primary."""
    primary = info.get("HostConfig", {}).get("NetworkMode", "")
    nets = info.get("NetworkSettings", {}).get("Networks", {}) or {}
    return [n for n in nets if n != primary and n not in ("bridge", "host", "none")]


def recreate_container(name: str, info: dict) -> bool:
    """Stop, remove, and re-run a container with its current configuration."""
    image = info["Config"]["Image"]
    was_running = info.get("State", {}).get("Running", False)

    if was_running:
        print_step(f"Stopping '{name}'...")
        _run(["docker", "stop", name])

    print_step(f"Removing '{name}'...")
    r = _run(["docker", "rm", name])
    if r.returncode != 0:
        print_error(f"Failed to remove '{name}': {r.stderr.strip()}")
        return False

    if not was_running:
        print_info(f"'{name}' was stopped — image updated, container removed")
        return True

    cmd = ["docker", "run", "-d", "--name", name, *_build_run_args(info), image]
    print_step(f"Starting updated '{name}'...")
    r = _run(cmd)
    if r.returncode != 0:
        print_error(f"Failed to restart '{name}': {r.stderr.strip()}")
        return False

    for net in _extra_networks(info):
        _run(["docker", "network", "connect", net, name])

    print_success(f"'{name}' updated and restarted")
    return True


def get_all_containers() -> list[str]:
    r = _run(["docker", "ps", "-a", "--format", "{{.Names}}"])
    if r.returncode != 0:
        print_error("Failed to list containers")
        sys.exit(1)
    return [n.strip() for n in r.stdout.strip().splitlines() if n.strip()]


def update_aio() -> None:
    print_header("UPDATING NEXTCLOUD AIO")

    updated = pull_image(AIO_MASTER_IMAGE)
    if not updated:
        print_info("Nextcloud AIO master container is already up to date")
        return

    info = inspect_container(AIO_MASTER)
    if not info:
        print_warning(f"'{AIO_MASTER}' not found — skipping")
        return

    if recreate_container(AIO_MASTER, info):
        print_info(
            "Master container updated — open https://<server-ip>:8443 to update AIO sub-containers"
        )


def update_containers(names: list[str]) -> None:
    print_header("UPDATING DOCKER CONTAINERS")

    skip = AIO_CONTAINERS | {AIO_MASTER}
    for name in names:
        if name in skip:
            continue

        info = inspect_container(name)
        if not info:
            print_warning(f"Could not inspect '{name}' — skipping")
            continue

        image = info["Config"]["Image"]
        print_step(f"Checking '{name}' ({image})...")

        if not pull_image(image):
            print_info(f"'{name}' is up to date")
            continue

        recreate_container(name, info)


def main() -> None:
    update_system_packages()

    if not docker_available():
        print_warning("Docker not available — skipping container updates")
        return

    names = get_all_containers()
    update_aio()
    update_containers(names)

    print_header("ALL UPDATES COMPLETE")
    print_info(
        "Nextcloud AIO sub-containers: update via https://<server-ip>:8443 if needed"
    )


if __name__ == "__main__":
    main()
