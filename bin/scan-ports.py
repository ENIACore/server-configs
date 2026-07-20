#!/usr/bin/env python3
import subprocess
import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from formatting import (
    get_input,
    print_error,
    print_header,
    print_info,
    print_step,
    print_warning,
)


def run_ss(args: list[str]) -> str:
    result = subprocess.run(
        ["sudo", "ss"] + args,
        capture_output=True,
        text=True,
    )
    return result.stdout


def show_all_ports() -> None:
    print_step("All Listening Ports (TCP & UDP)")
    print(run_ss(["-tulpn"]))


def show_tcp_ports() -> None:
    print_step("TCP Listening Ports")
    print(run_ss(["-tlpn"]))


def show_udp_ports() -> None:
    print_step("UDP Listening Ports")
    print(run_ss(["-ulpn"]))

