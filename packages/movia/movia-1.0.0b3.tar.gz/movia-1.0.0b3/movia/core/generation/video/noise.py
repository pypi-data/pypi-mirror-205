#!/usr/bin/env python3

"""
** Generate a video noise signal. **
------------------------------------
"""

import fractions
import hashlib
import math
import numbers
import random
import struct
import typing

import torch

from movia.core.classes.container import ContainerInput
from movia.core.classes.frame_video import FrameVideo
from movia.core.classes.stream import Stream
from movia.core.classes.stream_video import StreamVideo
from movia.core.exceptions import OutOfTimeRange



class GeneratorVideoNoise(ContainerInput):
    """
    ** Generate a pure noise video signal. **

    Attributes
    ----------
    seed : float
        The value of the seed between 0 and 1 (readonly).
    shape : tuple[int, int]
        The vertical and horizontal (i, j) resolution of the image (readonly).

    Examples
    --------
    >>> from movia.core.generation.video.noise import GeneratorVideoNoise
    >>> stream = GeneratorVideoNoise(0, shape=(13, 9)).out_streams[0]
    >>> stream.snapshot(0)[..., 0]
    tensor([[ 11,  17, 169,  48,   9, 217, 124, 113, 195],
            [ 51,  79, 173, 237, 176, 201, 124,  23, 177],
            [167, 187,  49, 153, 107, 249, 128,  89,  51],
            [174,  30, 173,  31, 127, 146, 134,   2, 123],
            [ 19, 151,  41, 219,  95, 199, 138, 180, 188],
            [177, 165,  63,  35, 177, 109, 134, 166, 154],
            [121, 250, 175, 186,   3, 185, 254, 152,   4],
            [193, 215, 220, 140, 151, 230, 148, 159, 213],
            [114, 249, 218, 159, 148, 169, 192, 178, 154],
            [ 80, 145, 195,  94, 102,  14, 190, 252,  45],
            [ 32, 103, 243, 155,  61,   9, 116,  55, 134],
            [255, 154, 249,  56, 146, 217,   0, 102,  48],
            [ 68, 187,  91, 247, 247,  80, 113, 105,  77]], dtype=torch.uint8)
    >>>
    """

    def __init__(
        self,
        seed: numbers.Real=None,
        shape: typing.Union[tuple[numbers.Integral, numbers.Integral], list[numbers.Integral]]=(
            720,
            720,
        ),
    ):
        """
        Parameters
        ----------
        seed : numbers.Real
            The random seed to have a repeatability.
            The value must be between 0 included and 1 excluded.
            If not provided, the seed is chosen randomly.
        shape : tuple or list, optional
            The pixel dimensions of the generated frames.
            The convention adopted is the numpy convention (height, width)
        """
        # check
        if seed is None:
            seed = random.random()
        assert isinstance(seed, numbers.Real), seed.__class__.__name__
        assert 0 <= seed < 1, seed
        assert isinstance(shape, (tuple, list)), shape.__class__.__name__
        assert len(shape) == 2, shape
        assert all(isinstance(s, numbers.Integral) and s > 0 for s in shape)

        # declaration
        self._seed = float(seed)
        self._height, self._width = int(shape[0]), int(shape[1])

        # delegation
        super().__init__([_StreamVideoNoiseUniform(self)])

    @classmethod
    def default(cls):
        return cls(0, [2, 2])

    def getstate(self) -> dict:
        return {
            "seed": self.seed,
            "shape": self.shape,
        }

    @property
    def seed(self):
        """
        ** The value of the seed between 0 and 1. **
        """
        return self._seed

    def setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        keys = {"seed", "shape"}
        assert set(state) == keys, set(state) - keys
        GeneratorVideoNoise.__init__(self, seed=state["seed"], shape=state["shape"])

    @property
    def shape(self) -> list[int, int]:
        """
        ** The vertical and horizontal (i, j) resolution of the image. **
        """
        return [self._height, self._width]


class _StreamVideoNoiseUniform(StreamVideo):
    """
    ** Random video stream where each pixel follows a uniform law. **
    """

    is_space_continuous = True
    is_time_continuous = True

    def __init__(self, node: GeneratorVideoNoise):
        assert isinstance(node, GeneratorVideoNoise), node.__class__.__name__
        super().__init__(node)

    def _snapshot(self, timestamp: fractions.Fraction) -> FrameVideo:
        if timestamp < 0:
            raise OutOfTimeRange(f"there is no audio frame at timestamp {timestamp} (need >= 0)")
        return FrameVideo(
            timestamp,
            torch.randint(
                0,
                256,
                (self.height, self.width, 3),
                generator=torch.random.manual_seed(
                    int.from_bytes(
                        hashlib.md5(
                            struct.pack(
                                "dLL",
                                self.node.seed,
                                timestamp.numerator % (1 << 64),
                                timestamp.denominator % (1 << 64),
                            )
                        ).digest(),
                        byteorder="big",
                    ) % (1 << 64) # solve RuntimeError: Overflow when unpacking long
                ),
                dtype=torch.uint8
            ),
        )

    @property
    def beginning(self) -> fractions.Fraction:
        return fractions.Fraction(0)

    @property
    def duration(self) -> typing.Union[fractions.Fraction, float]:
        return math.inf
