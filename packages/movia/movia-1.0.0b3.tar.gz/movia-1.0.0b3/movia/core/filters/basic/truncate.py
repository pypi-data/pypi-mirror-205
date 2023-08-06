#!/usr/bin/env python3

"""
** Allows you to temporarily limit a sequence. **
-------------------------------------------------
"""



import fractions
import math
import numbers
import typing

from movia.core.classes.meta_filter import MetaFilter
from movia.core.classes.node import Node
from movia.core.classes.stream import Stream
from movia.core.filters.basic.cut import FilterCut
from movia.core.filters.basic.identity import FilterIdentity



class FilterTruncate(MetaFilter):
    """
    ** Shortens the duration of a stream. **

    It is a particular case of ``movia.core.filters.basic.cut.FilterCut``.

    Attributes
    ----------
    duration_max : typing.Union[fractions.Fraction, float]:
        The maximum duration beyond which the flows do not return anything (readonly).

    Examples
    --------
    >>> from movia.core.exceptions import OutOfTimeRange
    >>> from movia.core.filters.basic.truncate import FilterTruncate
    >>> from movia.core.generation.audio.noise import GeneratorAudioNoise
    >>> from movia.core.generation.video.noise import GeneratorVideoNoise
    >>>
    >>> (s_base_audio,) = GeneratorAudioNoise(0).out_streams
    >>> (s_base_video,) = GeneratorVideoNoise(0, (2, 2)).out_streams
    >>> s_trunc_audio, s_trunc_video = FilterTruncate([s_base_audio, s_base_video], 10).out_streams
    >>>
    >>> _ = s_trunc_audio.snapshot(0, 1, 10) # [0, 10[
    >>> try:
    ...     s_trunc_audio.snapshot(9, 1, 2) # [9, 11[
    ... except OutOfTimeRange as err:
    ...     print(err)
    ...
    the stream has been truncated under 0 and over 10 seconds, eval from 9 to length 2/1
    >>>
    >>> _ = s_trunc_video.snapshot(0)
    >>> try:
    ...     s_trunc_video.snapshot(10)
    ... except OutOfTimeRange as err:
    ...     print(err)
    ...
    the stream has been truncated under 0 and over 10 seconds, evaluation at 10 seconds
    >>>
    """

    def __init__(self, in_streams: typing.Iterable[Stream], duration_max: numbers.Real):
        """
        Parameters
        ----------
        in_streams : typing.Iterable[Stream]
            Forwarded to ``movia.core.classes.filter.Filter``.
        duration_max : numbers.Real
            The maximal duration of the new stream.
        """
        assert isinstance(duration_max, numbers.Real), duration_max.__class__.__name__
        assert math.isfinite(duration_max), duration_max
        self._duration_max = duration_max
        super().__init__(in_streams)

    def _compile(self, in_streams: tuple[Stream]) -> Node:
        trunc_streams = FilterCut(in_streams, self._duration_max).out_streams[:len(in_streams)]
        return FilterIdentity(trunc_streams)

    @classmethod
    def default(cls):
        return cls([], 10)

    @property
    def duration_max(self) -> fractions.Fraction:
        """
        ** The maximum duration beyond which the flows do not return anything. **
        """
        return fractions.Fraction(self._duration_max)

    def getstate(self) -> dict:
        return {"duration_max": str(self.duration_max)}

    def setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        assert set(state) == {"duration_max"}, set(state)-{"duration_max"}
        FilterTruncate.__init__(self, in_streams, fractions.Fraction(state["duration_max"]))
