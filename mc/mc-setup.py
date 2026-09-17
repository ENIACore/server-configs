#!/usr/bin/env python3

import secrets
import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from checks import require_dir
from common import ensure_dir
from config import DOCKER_NETWORK_NAME, prompt_and_save, require_config_value
from docker import ensure_network, run_container
from formatting import print_header, print_info, print_step

# Server settings
MC_CONTAINER_NAME = "server-mc"
MC_TYPE = "FABRIC"
MC_VERSION = "LATEST"
MC_MEMORY = "3G"
MC_DIFFICULTY = "normal"
MC_MAX_PLAYERS = "10"
MC_VIEW_DISTANCE = "10"
MC_ENFORCE_WHITELIST = "TRUE"
MC_TZ = "America/Chicago"

# Mods (auto-downloaded from Modrinth)
MC_MODRINTH_PROJECTS = "lithium"


def generate_rcon_password(rcon_pass_file: str) -> str:
    password = secrets.token_hex(16)
