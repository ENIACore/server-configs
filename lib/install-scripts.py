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
}


def create_dirs():
    SBIN.mkdir(parents=True, exist_ok=True)
    LIB_DIR.mkdir(parents=True, exist_ok=True)
    init = LIB_DIR / "init.py"
    if not init.exists():
        init.touch()


def copy_scripts():
    lib_prefix = SCRIPTS_DIR / "lib"

    for script in SCRIPTS_DIR.rglob("*.py"):
        if script.stem in IGNORE:
            continue

        try:
            script.relative_to(lib_prefix)
            dest = LIB_DIR / script.name
        except ValueError:
            dest = SBIN / script.stem
