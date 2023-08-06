"""
"""

from .. import utils
from .patching import Torch

if utils.stateless_gpu():
    Torch.patch()
