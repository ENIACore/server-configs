#!/usr/bin/env python3

import sys
import urllib.parse

sys.path.insert(0, "/usr/local/sbin/_lib")
from common import run_cmd
from config import (
    DOCKER_NETWORK_NAME,
    prompt_and_save,
    require_config_value,
    set_config_value,
)
from docker import ensure_network, run_container
from formatting import print_header, print_info

PG_USER = "postgres"
PG_HOST = "server-pg"
PG_PORT = 5432
PG_DB = "postgres"


