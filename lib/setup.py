#!/usr/bin/env python3

"""
Server Setup Script
"""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / "bin" / "_lib"))
from common import copy_path, ensure_dir, write_lines
from config import (
    CF_CONFIG_PATH,
    F2B_CONFIG_PATH,
    JACKETT_CONFIG_PATH,
    JELLY_CONFIG_PATH,
    JFA_CONFIG_PATH,
    MC_CONFIG_PATH,
    NEXTCLOUD_CONFIG_PATH,
    NGINX_CONFIG_PATH,
    QBIT_CONFIG_PATH,
    RAID_CONFIG_PATH,
    SERVER_CLONE_PATH,
    SERVER_CONFIG_PATH,
    SERVER_USER,
    UFW_CONFIG_PATH,
    VAULT_CONFIG_PATH,
    get_config_value,
    prompt_and_save,
    require_config_value,
    set_config_value,
)
from formatting import (
    RED,
    RESET,
    print_group_end,
    print_group_start,
    print_group_step,
    print_info,
    print_step,
    print_success,
    print_warning,
)


def create_directories() -> None:
    print_step("Creating system directories...")

    directories = [
        CF_CONFIG_PATH,
        NGINX_CONFIG_PATH,
        F2B_CONFIG_PATH,
        UFW_CONFIG_PATH,
        JELLY_CONFIG_PATH,
        JFA_CONFIG_PATH,
        NEXTCLOUD_CONFIG_PATH,
        JACKETT_CONFIG_PATH,
        VAULT_CONFIG_PATH,
        RAID_CONFIG_PATH,
        MC_CONFIG_PATH,
        SERVER_CONFIG_PATH,
        QBIT_CONFIG_PATH,
