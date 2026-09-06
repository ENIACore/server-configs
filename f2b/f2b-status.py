#!/usr/bin/env python3

import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from common import run_cmd
from formatting import print_header, print_info

JAILS = [
    "nginx-http-auth",
    "nginx-bad-request",
    "nginx-botsearch",
    "nginx-limit-req",
    "sshd",
