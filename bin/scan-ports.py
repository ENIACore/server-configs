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


def search_port() -> None:
    port = get_input("Enter port number to search for")
    if not port.isdigit():
        print_error("Invalid port number. Please enter a numeric value.")
        return

    print_step(f"Connections on Port {port}")
    output = run_ss(["-tulpn"])
    matches = [line for line in output.splitlines() if f":{port}" in line]

    if matches:
        print("\n".join(matches))
    else:
        print_warning(f"No connections found on port {port}")


def show_listening_processes() -> None:
    print_step("Processes Using Ports")
    output = run_ss(["-tulpn"])
    lines = [line for line in output.splitlines() if "LISTEN" in line]
    print("\n".join(lines) if lines else "No listening processes found")


def show_established() -> None:
    print_step("Established TCP Connections")
    output = run_ss(["-tuln"])
    lines = [line for line in output.splitlines() if "ESTAB" in line]
    print("\n".join(lines) if lines else "No established connections found")


def show_summary() -> None:
    from collections import Counter

    print_step("Port Usage Summary")

    def extract_ports(output: str) -> list[str]:
