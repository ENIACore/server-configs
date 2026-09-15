#!/usr/bin/env python3

import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from checks import require_dir
from common import ensure_dir
from config import DOCKER_NETWORK_NAME, require_config_value
from docker import ensure_network, run_container
from formatting import print_header, print_info, print_step


def main():
    print_header("SETTING UP JFA-GO (JELLYFIN ACCOUNT MANAGER)")

    media_path = require_config_value("MEDIA_SERVICES_PATH")

    require_dir(media_path, "Media services path")

    jfa_config_dir = f"{media_path}/jfa/config"
    jelly_config_dir = f"{media_path}/jelly/config"

    print_info(f"Jellyfin config dir: {jelly_config_dir}")

    print_step("Creating JFA directories...")
    ensure_dir(jfa_config_dir)

    ensure_network()

    run_container(
        name="jfa-go",
        opts=[
            "--network",
            DOCKER_NETWORK_NAME,
            "--volume",
            f"{jfa_config_dir}:/data",
