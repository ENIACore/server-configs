#!/usr/bin/env python3
# Config management for server-configs - /usr/local/sbin/_lib/config.py

import json
import sys
from pathlib import Path

sys.path.insert(0, "/usr/local/sbin/_lib")
from formatting import (
    get_input,
    print_error,
    print_group_end,
    print_group_start,
    print_group_step,
    print_info,
    print_success,
    print_warning,
)

# Server paths
SERVER_BIN = "/usr/local/sbin"
SERVER_ENV_PATH = Path(f"{SERVER_BIN}/source-env")
SERVER_CLONE_PATH = Path("/tmp/server-configs")
SERVER_CONFIG_PATH = Path("/etc/server")
SERVER_CONFIG_FILE_PATH = SERVER_CONFIG_PATH / "config.json"

# Service paths
CF_CONFIG_PATH = Path("/etc/cloudflare")
NGINX_CONFIG_PATH = Path("/etc/nginx")
F2B_CONFIG_PATH = Path("/etc/f2b")
UFW_CONFIG_PATH = Path("/etc/ufw")
JELLY_CONFIG_PATH = Path("/etc/jelly")
JFA_CONFIG_PATH = Path("/etc/jfa")
NEXTCLOUD_CONFIG_PATH = Path("/etc/nextcloud")
JACKETT_CONFIG_PATH = Path("/etc/jackett")
VAULT_CONFIG_PATH = Path("/etc/vault")
