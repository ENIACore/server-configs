#!/usr/bin/env python3

import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from checks import require_server_user
from config import DOCKER_NETWORK_NAME, prompt_and_save, require_config_value
from docker import ensure_network, run_container
from formatting import print_header, print_success

PG_CONTAINER_NAME = "server-pg"
PG_IMAGE = "postgres:latest"
PG_DATA_VOLUME = "server-pg-data"
PG_DATA_PATH = "/var/lib/postgresql"


def main():
    print_header("SETTING UP POSTGRES DATABASE")
