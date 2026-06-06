#!/usr/bin/env python3
import shutil
import subprocess
import sys
from pathlib import Path

REPO_URL = "https://github.com/ENIACore/server-configs.git"
CLONE_PATH = Path("/tmp/server-configs")

if CLONE_PATH.exists():
