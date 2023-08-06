"""
"""

import os

import requests

from .. import utils


NODE_IP = os.environ['NODE_IP'] # Fail if not defined
BASE_URL = f"http://{NODE_IP}:8000"
CGROUP_PATH = utils.self_cgroup_device_path()


def post(path: str, **kwargs) -> requests.Response:
    return requests.post(BASE_URL + path, params={'cgroupPath': CGROUP_PATH} | kwargs)

def schedule():
    res = post('/schedule')
    if not res.ok:
        raise Exception("GPU already in use")

def release(fail: bool = False):
    res = post('/release', fail=fail)
    if not res.ok:
        raise Exception("Something went wrong .. ping @charles on Slack")
