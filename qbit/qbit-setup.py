#!/usr/bin/env python3

import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from checks import require_dir, require_file
from common import ensure_dir, run_cmd
from config import DOCKER_NETWORK_NAME, QBIT_CONFIG_PATH, require_config_value
from docker import ensure_network, run_container
from formatting import print_header, print_step

# LAN CIDR — allows WebUI access directly from LAN without going through nginx.
# NOTE: Do NOT add the Docker subnet here — it's the container's own
# directly-attached network and including it causes a route conflict
# in hotio's startup (eth0 is already on the subnet). Container-to-
# container traffic on the docker network bypasses the VPN automatically.
VPN_LAN_CIDR = "192.168.1.0/24"

WG_CONF_SRC = QBIT_CONFIG_PATH / "wg0.conf"


def main():
    print_header("SETTING UP QBITTORRENT WITH WIREGUARD VPN")
