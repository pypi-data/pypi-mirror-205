# File: undersampling.py
# Created Date: Wednesday December 14th 2022
# Author: Steven Atkinson (steven@atkinson.mn)

"""
Model wrapper that uses undersampling with neural super-resolution
"""

import torch.nn as nn

from ._base import BaseNet
from .wavenet import _WaveNet

class _SuperResolution(nn.Module):
    """
    Neural super-resolution upscaler
    """
    def __init__(self, in_channels, causal: bool=True):
        super().__init__()
        self._causal = causal

    @property
    def delay(self) -> int:
        """
        How much the output delays the real thing (due to non-causal SR)
        """
        assert self._causal
        return 0


class Undersampling(BaseNet):
    # TODO: delay!
    def __init__(self, undersample: int, core: BaseNet, super_resolution: _SuperResolution):
        super().__init__()
        self._undersample = undersample
        self._core = core
        self._super_resolution = super_resolution

    @property
    def delay(self):
        return self._super_resolution.delay

    @property
    def receptive_field(self) -> int:
        return super().receptive_field

    def 
