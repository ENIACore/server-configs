#!/usr/bin/env python3

import sys
from pathlib import Path
from subprocess import CompletedProcess

sys.path.insert(0, "/usr/local/sbin/_lib")
from config import SERVER_ENV_PATH
from formatting import (  # noqa: E402
    print_error,
    print_info,
    print_step,
    print_success,
    print_warning,
)


def copy_to_clipboard(text):
    """Copy text to clipboard.
    Returns the tool used, or empty string if none found."""
    import shutil
    import subprocess

    for tool, args in [
        ("pbcopy", ["pbcopy"]),
        ("xclip", ["xclip", "-selection", "clipboard"]),
        ("xsel", ["xsel", "--clipboard", "--input"]),
        ("wl-copy", ["wl-copy"]),
    ]:
        if shutil.which(tool):
            subprocess.run(args, input=text.encode(), check=True)
            return tool
    return ""


def _ensure_source_env() -> None:
    if not SERVER_ENV_PATH.exists():
        SERVER_ENV_PATH.write_text("#!/bin/sh\n")
        SERVER_ENV_PATH.chmod(0o755)


