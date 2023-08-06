"""
"""
from __future__ import annotations

from typing import Callable


class Torch:

    backup: dict[str, Callable] | None = None

    @staticmethod
    def _cuda_init_raise():
        raise RuntimeError(
            "CUDA must not be initialized in the main process "
            "on Spaces with Stateless GPU environment.\n"
            "You can look at this Stacktrace to find out "
            "which part of your code triggered a CUDA init"
        )

    @staticmethod
    def patch():
        try:
            import torch # type: ignore
        except ImportError:
            return
        Torch.backup = {
            'is_available': torch.cuda.is_available,
            'cuda_init': torch._C._cuda_init # type: ignore
        }
        torch.cuda.is_available = lambda: True
        torch._C._cuda_init = Torch._cuda_init_raise # type: ignore

    @staticmethod
    def unpatch():
        try:
            import torch # type: ignore
        except ImportError:
            return
        if Torch.backup is None:
            return
        torch.cuda.is_available = Torch.backup['is_available']
        torch._C._cuda_init = Torch.backup['cuda_init'] # type: ignore
