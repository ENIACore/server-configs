#!/usr/bin/env python3

import argparse
import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from checks import ensure_packages, require_dir, require_file
from common import run_cmd
from config import CF_CONFIG_PATH, require_config_value
from formatting import print_header, print_step, print_success, print_warning

CF_INI_FILE = CF_CONFIG_PATH / "cloudflare.ini"
CF_PROPAGATION_SECONDS = 60


def main():
    print_header("CREATING DNS CERTIFICATE")

    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", "-d", action="store_true")
    args = parser.parse_args()

    require_dir(str(CF_CONFIG_PATH), "Cloudflare config directory")
    require_file(
        str(CF_INI_FILE), "Cloudflare ini file with dns_cloudflare_api_token"
    )

    root_domain = require_config_value("ROOT_DOMAIN")
    wildcard_domain = require_config_value("WILDCARD_DOMAIN")

    if args.dry_run:
        print_warning("Dry-run mode — no certificate will be issued")
        print_step(
            f"Testing SSL certificate creation for {root_domain} and {wildcard_domain}..."
        )
    else:
        print_step(
            f"Creating SSL certificate for {root_domain} and {wildcard_domain}..."
        )

    certbot_cmd = (
        f"sudo certbot certonly"
        f" --dns-cloudflare"
        f" --dns-cloudflare-credentials {CF_INI_FILE}"
        f" --dns-cloudflare-propagation-seconds {CF_PROPAGATION_SECONDS}"
