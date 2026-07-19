#!/usr/bin/env python3

import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from checks import require_dir
from config import DOCKER_NETWORK_NAME, require_config_value
from docker import ensure_network, run_container
from formatting import print_header


def main():
    print_header("SETTING UP FLARESOLVERR")

    media_path = require_config_value("MEDIA_SERVICES_PATH")
    require_dir(media_path, "Media services path")

    ensure_network()

    run_container(
        name="flaresolverr",
