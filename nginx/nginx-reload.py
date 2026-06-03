#!/usr/bin/env python3
import subprocess
import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from formatting import print_error, print_header, print_info, print_success

NGINX_CONTAINER_NAME = "server-proxy"


def test_config() -> bool:
    result = subprocess.run(
        ["docker", "exec", NGINX_CONTAINER_NAME, "nginx", "-t"],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print_success("Config test passed")
        return True
    print_error("Config test failed")
    print_error(result.stderr.strip())
    return False

