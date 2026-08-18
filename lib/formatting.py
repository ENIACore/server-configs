#!/usr/bin/env python3

import getpass

# Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"
BOLD = "\033[1m"
GREY = "\033[90m"


def print_error(msg):
    print(
        f"  {BLUE}{BOLD}→{RESET}  {RED}{BOLD}[ERROR]{RESET}  {RED}{msg}{RESET}"
    )


def print_success(msg):
    print(
        f"  {BLUE}{BOLD}→{RESET}  {GREEN}{BOLD}[SUCCESS]{RESET}  {GREEN}{msg}{RESET}"
    )


def print_warning(msg):
    print(
        f"  {BLUE}{BOLD}→{RESET}  {YELLOW}{BOLD}[WARNING]{RESET}  {YELLOW}{msg}{RESET}"
    )


def print_info(msg):
    print(
        f"  {BLUE}{BOLD}→{RESET}  {BLUE}{BOLD}[INFO]{RESET}  {BLUE}{msg}{RESET}"
    )


def print_step(msg):
    print(
        f"  {BLUE}{BOLD}→{RESET}  {CYAN}{BOLD}[STEP]{RESET}  {CYAN}{msg}{RESET}"
    )


def print_header(msg):
    line = "=" * 60
    print(f"\n{MAGENTA}{BOLD}{line}{RESET}")
