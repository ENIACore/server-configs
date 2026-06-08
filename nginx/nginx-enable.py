#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

sys.path.insert(0, "/usr/local/sbin/_lib")
from common import run_cmd
from config import NGINX_CONFIG_PATH
from formatting import (
    print_error,
    print_header,
    print_info,
    print_step,
    print_success,
)

AVAILABLE_DIRS = {
    "sites": (
        NGINX_CONFIG_PATH / "sites-available",
        NGINX_CONFIG_PATH / "sites-enabled",
    ),
    "streams": (
        NGINX_CONFIG_PATH / "streams-available",
