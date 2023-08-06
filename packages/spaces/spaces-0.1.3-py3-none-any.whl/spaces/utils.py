"""
"""

from pathlib import Path


def in_spaces() -> bool:
    # TODO
    return True


def stateless_gpu() -> bool:
    if not in_spaces():
        return False
    # TODO
    return True

def self_cgroup_device_path() -> str:
    cgroup_content = Path('/proc/self/cgroup').read_text()
    return cgroup_content.strip().split('5:devices:')[1].split('\n')[0]
