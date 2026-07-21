#!/usr/bin/env python3

import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from checks import require_dir
from common import ensure_dir
from config import DOCKER_NETWORK_NAME, require_config_value
from docker import ensure_network, run_container
from formatting import print_header, print_info, print_step


def main():
    print_header("SETTING UP NEXTCLOUD ALL-IN-ONE")

    core_path = require_config_value("CORE_SERVICES_PATH")
    require_dir(core_path, "Core services path")

    nextcloud_data_dir = f"{core_path}/nextcloud-data"

    print_step(
        f"Creating Nextcloud data directory at {nextcloud_data_dir}..."
