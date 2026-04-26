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
        (plaintext_password, argon2id_phc_hash)
    """
    password = base64.b64encode(secrets.token_bytes(36)).decode()
    salt = base64.b64encode(secrets.token_bytes(24)).decode()

    # Bitwarden defaults: m=65540 (64MiB), t=3, p=4
    result = subprocess.run(
        ["argon2", salt, "-e", "-id", "-k", "65540", "-t", "3", "-p", "4"],
        input=password.encode(),
        capture_output=True,
    )

    if result.returncode != 0 or not result.stdout.strip():
        print_error("Failed to generate argon2id PHC string")
        sys.exit(1)

    token = result.stdout.strip().decode()
    return password, token


def save_admin_password(vault_data_dir: str, password: str) -> str:
    from pathlib import Path

    pass_file = Path(vault_data_dir) / VAULT_ADMIN_PASS_FILE
    pass_file.write_text(password + "\n")
    pass_file.chmod(0o600)
