#!/usr/bin/env python3

import base64
import secrets
import subprocess
import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from checks import ensure_packages, require_dir
from common import ensure_dir
from config import DOCKER_NETWORK_NAME, require_config_value
from docker import ensure_network, run_container
from formatting import (
    print_error,
    print_header,
    print_info,
    print_step,
)

VAULT_ADMIN_PASS_FILE = ".admin_password"


def generate_admin_token() -> tuple[str, str]:
    """Generate a random admin password and its argon2id PHC hash.

    Returns:
