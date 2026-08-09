#!/usr/bin/env python3
import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from checks import require_dir
from common import ensure_dir
from config import (
    DOCKER_NETWORK_NAME,
    NGINX_CONFIG_PATH,
    require_config_value,
)
from docker import ensure_network, run_container
from formatting import print_header, print_step

NGINX_LOG_DIR = "/var/log/nginx"
NGINX_VAR_DIR = "/var/www/server"
NGINX_CONTAINER_IP = "172.20.0.254"


def main():
    print_header("CREATING SERVER REVERSE PROXY")

    root_domain = require_config_value("ROOT_DOMAIN")
    require_dir(
        f"/etc/letsencrypt/live/{root_domain}",
        "Letsencrypt SSL certificates directory",
    )

    print_step("Processing nginx templates...")
