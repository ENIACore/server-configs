#!/usr/bin/env python3

import json
import sys
import urllib.error
import urllib.request

sys.path.insert(0, "/usr/local/sbin/_lib")
from checks import require_server_user
from common import ensure_dir
from config import require_config_value
from formatting import print_error, print_header
from logger import init_logger, log

CF_LOG_FILE = "dns.log"
CF_LOG_MAX_LINES = 100
CF_API_BASE = "https://api.cloudflare.com/client/v4"


def _cf_request(
    method: str, path: str, api_key: str, data: dict | None = None
) -> dict:
    body = json.dumps(data).encode() if data else None
    headers = {"Authorization": f"Bearer {api_key}"}
    if data:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(
        f"{CF_API_BASE}{path}", data=body, headers=headers, method=method
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode())


def _get_public_ipv4() -> str:
    for url in [
        "https://api.ipify.org",
        "https://icanhazip.com",
        "https://ifconfig.me",
