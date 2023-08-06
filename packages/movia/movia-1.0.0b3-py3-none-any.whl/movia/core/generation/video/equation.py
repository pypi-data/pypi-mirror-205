#!/usr/bin/env python3

"""
** Allows to generate colors from continuous mathematical functions. **
-----------------------------------------------------------------------
"""


import fractions
import math
import numbers
import typing

from sympy.core import Symbol
from sympy.core.basic import Basic
import torch

from movia.core.classes.container import ContainerInput
from movia.core.classes.frame_video import FrameVideo
from movia.core.classes.stream import Stream
from movia.core.classes.stream_video import StreamVideo
from movia.core.compilation.sympy_to_torch import _parse_expr, LambdifyHomogeneous
from movia.core.exceptions import OutOfTimeRange



class GeneratorVideoEquation(ContainerInput):
    """
    ** Generate a video stream whose channels are defened by any equations. **

    Attributes
    ----------
    colors : list[sympy.core.expr.Expr]
        The luminosity expression of the differents chanels (readonly).
    shape : tuple[int, int]
        The vertical and horizontal (i, j) resolution of the image (readonly).

    Examples
    --------
    >>> from movia.core.generation.video.equation import GeneratorVideoEquation
    >>> (stream,) = GeneratorVideoEquation(
    ...     "atan(pi*j)/pi + 1/2", # dark blue on the left and bright on the right
    ...     "sin(2pi(i-t))**2", # horizontal descending green waves
    ...     "exp(-(i**2+j**2)/(2*(1e-3+.1*t)))", # red spot in the center that grows
    ...     shape=(13, 9),
    ... ).out_streams
    >>> stream.node.colors
    [atan(pi*j)/pi + 1/2, sin(pi*(2*i - 2*t))**2, exp((-i**2 - j**2)/(0.2*t + 0.002))]
    >>> stream.snapshot(0)[..., 0] # blue at t=0
    tensor([[ 25,  33,  46,  73, 128, 182, 209, 222, 230],
            [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
            [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
            [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
            [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
            [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
            [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
            [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
            [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
            [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
            [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
            [ 25,  33,  46,  73, 128, 182, 209, 222, 230],
            [ 25,  33,  46,  73, 128, 182, 209, 222, 230]], dtype=torch.uint8)
    >>> stream.snapshot(0)[..., 1] # green at t=0
    tensor([[  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [191, 191, 191, 191, 191, 191, 191, 191, 191],
            [191, 191, 191, 191, 191, 191, 191, 191, 191],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [191, 191, 191, 191, 191, 191, 191, 191, 191],
            [191, 191, 191, 191, 191, 191, 191, 191, 191],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [191, 191, 191, 191, 191, 191, 191, 191, 191],
            [191, 191, 191, 191, 191, 191, 191, 191, 191],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [191, 191, 191, 191, 191, 191, 191, 191, 191],
            [191, 191, 191, 191, 191, 191, 191, 191, 191],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0]], dtype=torch.uint8)
    >>> stream.snapshot(0)[..., 2] # red at t=0
    tensor([[  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0, 255,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0]], dtype=torch.uint8)
    >>> stream.snapshot(1)[..., 2] # red at t=1
    tensor([[  0,   0,   1,   1,   2,   1,   1,   0,   0],
            [  0,   1,   2,   6,   8,   6,   2,   1,   0],
            [  0,   2,   8,  21,  28,  21,   8,   2,   0],
            [  1,   5,  21,  54,  74,  54,  21,   5,   1],
            [  1,   9,  43, 108, 147, 108,  43,   9,   1],
            [  2,  14,  64, 163, 222, 163,  64,  14,   2],
            [  2,  16,  74, 187, 255, 187,  74,  16,   2],
            [  2,  14,  64, 163, 222, 163,  64,  14,   2],
            [  1,   9,  43, 108, 147, 108,  43,   9,   1],
            [  1,   5,  21,  54,  74,  54,  21,   5,   1],
            [  0,   2,   8,  21,  28,  21,   8,   2,   0],
            [  0,   1,   2,   6,   8,   6,   2,   1,   0],
            [  0,   0,   1,   1,   2,   1,   1,   0,   0]], dtype=torch.uint8)
    >>>
    """

    def __init__(self,
        *colors: typing.Union[Basic, numbers.Real, str],
        shape: typing.Union[tuple[numbers.Integral, numbers.Integral], list[numbers.Integral]] = (
            720,
            720,
        ),
    ):
        """
        Parameters
        ----------
        *colors : str or sympy.Basic
            The brightness of the color channels.
            The channels are interpreted like is describe in
            ``movia.core.classes.frame_video.FrameVideo``.
            The return values will be cliped to stay in the range [0, 1].
            The value is 0 for min brightness and 1 for the max.
            If the expression gives a complex, take the real part.
            The variables that can be used in these functions are the following:

                * t : The time in seconds since the beginning of the video.
                * i : The relative position along the vertical axis (numpy convention).
                    This value evolves between -1 and 1.
                * j : The relative position along the horizontal axis (numpy convention).
                    This value evolves between -1 and 1.
        shape : tuple or list, optional
            The pixel dimensions of the generated frames.
            The convention adopted is the numpy convention (height, width)
        """
        # check
        assert all(isinstance(c, (Basic, numbers.Real, str)) for c in colors), colors
        assert 1 <= len(colors) <= 4, len(colors)
        assert isinstance(shape, (tuple, list)), shape.__class__.__name__
        assert len(shape) == 2, shape
        assert all(isinstance(s, numbers.Integral) and s > 0 for s in shape)

        # cast
        self._colors = [_parse_expr(c) for c in colors]
        self._height, self._width = int(shape[0]), int(shape[1])

        # check
        free_symbs = set(map(str, set.union(*(c.free_symbols for c in self._colors))))
        if free_symbs - {"i", "j", "t"}:
            raise ValueError(f"only i, j and t symbols are allowed, not {free_symbs}")

        # delegation
        out_streams = [_StreamVideoEquation(self)]
        super().__init__(out_streams)

    @classmethod
    def default(cls):
        return cls(0, shape=[2, 2])

    def getstate(self) -> dict:
        return {
            "colors": [str(c) for c in self.colors],
            "shape": self.shape,
        }

    def setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        keys = {"colors", "shape"}
        assert set(state) == keys, set(state)-keys
        GeneratorVideoEquation.__init__(self, *state["colors"], shape=state["shape"])

    @property
    def colors(self) -> list[Basic]:
        """
        ** The luminosity expression of the differents chanels. **
        """
        return self._colors.copy()

    @property
    def shape(self) -> list[int, int]:
        """
        ** The vertical and horizontal (i, j) resolution of the image. **
        """
        return [self._height, self._width]


class _StreamVideoEquation(StreamVideo):
    """
    ** Color field parameterized by time and position. **
    """

    is_space_continuous = True
    is_time_continuous = True

    def __init__(self, node: GeneratorVideoEquation):
        assert isinstance(node, GeneratorVideoEquation), node.__class__.__name__
        super().__init__(node)

        # compilation
        self._colors_func = None

    def _get_colors_func(self) -> typing.Callable:
        """
        ** Allows to "compile" equations at the last moment. **
        """
        if self._colors_func is None:
            self._colors_func = LambdifyHomogeneous(
                [Symbol("i"), Symbol("j"), Symbol("t")], self.node.colors
            )
        return self._colors_func

    def _snapshot(self, timestamp: fractions.Fraction) -> FrameVideo:
        # verif
        if timestamp < 0:
            raise OutOfTimeRange(f"there is no audio frame at timestamp {timestamp} (need >= 0)")

        # calculation
        i_field, j_field = torch.meshgrid(
            torch.linspace(-1, 1, self.height, dtype=torch.float64),
            torch.linspace(-1, 1, self.width, dtype=torch.float64),
            indexing="ij",
        )
        i_field, j_field = i_field.clone(), j_field.clone()
        time_field = torch.full((self.height, self.width), float(timestamp), dtype=torch.float64)
        colors = self._get_colors_func()(i_field, j_field, time_field)

        # correction + cast
        frame = FrameVideo(
            timestamp,
            torch.empty((self.height, self.width, len(self.node.colors)), dtype=torch.uint8),
        )
        for i, col in enumerate(colors):
            if col.dtype.is_complex:
                col = torch.real(col) # takes real part
            torch.nan_to_num( # replace +inf -inf and nan
                col,
                nan=127.0/255.0,
                posinf=1.0,
                neginf=0.0,
                out=col,
            )
            torch.clip(col, 0.0, 1.0, out=col)
            torch.multiply(col, 255, out=col)
            torch.round(col, out=col)
            col = col.to(dtype=torch.uint8, copy=False)
            frame[:, :, i] = col

        return frame

    @property
    def beginning(self) -> fractions.Fraction:
        return fractions.Fraction(0)

    @property
    def duration(self) -> typing.Union[fractions.Fraction, float]:
        return math.inf
