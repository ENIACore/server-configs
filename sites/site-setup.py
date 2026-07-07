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


def build_pg_conn_str(password: str) -> str:
    encoded = urllib.parse.quote(password, safe="")
    return f"postgresql://{PG_USER}:{encoded}@{PG_HOST}:{PG_PORT}/{PG_DB}"


def main():
    print_header("SETTING UP PERSONAL SITE")

    pg_password = require_config_value("PG_PASSWORD")
    pg_conn_str = build_pg_conn_str(pg_password)
    set_config_value("PG_CONN_STR", pg_conn_str)
    print_info(
        f"Built Postgres connection string for {PG_USER}@{PG_HOST}:{PG_PORT}/{PG_DB}"
    )

    payload_secret = prompt_and_save(
        "PERSONAL_SITE_PAYLOAD_SECRET",
        "Enter Payload CMS secret key",
        secret=True,
    )

    ensure_network()

