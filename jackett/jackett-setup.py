#!/usr/bin/env python3

import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from checks import require_dir
from common import ensure_dir
from config import (
    DOCKER_NETWORK_NAME,
    require_config_value,
)
from docker import ensure_network, run_container
from formatting import print_header, print_step


def main():
    print_header("SETTING UP JACKETT INDEXER")

    media_path = require_config_value("MEDIA_SERVICES_PATH")
    root_domain = require_config_value("ROOT_DOMAIN")

    require_dir(media_path, "Media services path")
