#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

HOME = Path.home()
SCRIPTS_DIR = Path("/tmp/server-configs")
SBIN = Path("/usr/local/sbin")
LIB_DIR = SBIN / "_lib"

BASHRC = HOME / ".bashrc"
ZSHRC = HOME / ".zshrc"

PATH_BLOCK = """
# Add custom scripts directory to PATH
if [[ ':$PATH:' != ':/usr/local/sbin:' ]]; then
    export PATH="/usr/local/sbin:$PATH"
fi
"""

IGNORE = {
    # "setup",
    "install",
    "install-scripts",
