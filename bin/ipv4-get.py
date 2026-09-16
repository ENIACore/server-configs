#!/usr/bin/env python3
import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from formatting import print_error, print_info, print_success

IPIFY_URL = "https://api.ipify.org"
ICANHAZIP_URL = "https://icanhazip.com"
IFCONFIG_URL = "https://ifconfig.me"


def get_public_ipv4() -> str:
    import urllib.request

    for url in [IPIFY_URL, ICANHAZIP_URL, IFCONFIG_URL]:
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                ip = resp.read().decode().strip()
