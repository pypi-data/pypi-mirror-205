"""
"""

import requests

from .. import utils


BASE_URL = 'http://172.17.0.1:8000'
CONTAINER_ID = utils.container_id()


def post(path: str, **kwargs) -> requests.Response:
    return requests.post(BASE_URL + path, params={'containerId': CONTAINER_ID} | kwargs)

def schedule():
    res = post('/schedule')
    if not res.ok:
        raise Exception("GPU already in use")

def release(fail: bool = False):
    res = post('/release', fail=fail)
    if not res.ok:
        raise Exception("Something went wrong .. ping @charles on Slack")
