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
    ]:
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.read().decode().strip()
        except Exception:
            continue


def _get_record_id(zone_id: str, name: str, api_key: str) -> str:
    resp = _cf_request(
        "GET",
        f"/zones/{zone_id}/dns_records?name={name}&type=A",
        api_key,
    )
    results = resp.get("result") or []
    return results[0].get("id", "") if results else ""


def _update_record(
    zone_id: str,
    record_id: str,
    name: str,
    ip: str,
    proxied: bool,
    api_key: str,
) -> bool:
    resp = _cf_request(
        "PUT",
        f"/zones/{zone_id}/dns_records/{record_id}",
        api_key,
        {
            "type": "A",
            "name": name,
            "content": ip,
            "ttl": 1,
            "proxied": proxied,
        },
    )
    return bool(resp.get("success"))

