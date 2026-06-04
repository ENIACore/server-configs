#!/usr/bin/env python3

import subprocess
import sys

sys.path.insert(0, "/usr/local/sbin/_lib")
from config import (
    DOCKER_NETWORK_GATEWAY,
    DOCKER_NETWORK_NAME,
    DOCKER_NETWORK_SUBNET,
)
from formatting import (
    GREY,
    RESET,
    YELLOW,
    print_error,
    print_group_end,
    print_group_start,
    print_group_step,
    print_info,
    print_step,
    print_success,
)

