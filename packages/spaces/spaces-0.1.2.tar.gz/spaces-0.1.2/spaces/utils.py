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

def container_id() -> str:
    cpuset = Path('/proc/self/cpuset').read_text()
    return cpuset.strip().split('/')[-1]
