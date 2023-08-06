#!/usr/bin/env python3

"""
** Defines the structure of an abstract video stream. **
--------------------------------------------------------
"""

import abc
import fractions
import math
import numbers

import torch

from movia.core.classes.filter import Filter
from movia.core.classes.frame_video import FrameVideo
from movia.core.classes.stream import Stream, StreamWrapper



class StreamVideo(Stream):
    """
    ** Representation of any video stream. **

    Attributes
    ----------
    height : int
        Height of the image in pixels (readonly).
    is_space_continuous : boolean
        True if the data is continuous in the spacial domain, False if it is discrete (readonly).
    width : int
        Width of the image in pixels (readonly).
    """

    def _snapshot(self, timestamp: fractions.Fraction) -> FrameVideo:
        raise NotImplementedError

    @property
    def height(self) -> int:
        """
        ** Height of all images in the stream. **
        """
        if self.is_space_continuous and hasattr(self.node, "shape"):
            return self.node.shape[0]
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def is_space_continuous(self) -> bool:
        """
        ** True if the data is continuous in the spacial domain, False if it is discrete. **
        """
        raise NotImplementedError

    def snapshot(self, timestamp: numbers.Real, *, channels=None) -> FrameVideo:
        """
        ** Extract the closest frame to the requested date. **

        Parameters
        ----------
        timestamp : numbers.Real
            The absolute time expressed in seconds, not relative to the beginning of the video.
            For avoid the inacuracies of round, it is recomended to use fractional number.
        channels : int, optional
            Impose the numbers of channels, apply convertion if nescessary.
            For the interpretation of the layers, see ``movia.core.classes.frame_video.FrameVideo``.

        Returns
        -------
        frame : FrameVideo
            Video frame with metadata.

        Raises
        ------
        movia.core.exception.OutOfTimeRange
            If we try to get a frame out of the definition range.
            The valid range is [self.beginning, self.beginning+self.duration[..
        """
        assert isinstance(timestamp, numbers.Real), timestamp.__class__.__name__
        if math.isnan(timestamp): # default transparent video frame
            frame = FrameVideo(0, torch.zeros((self.height, self.width, 2), dtype=torch.uint8))
        else:
            frame = self._snapshot(fractions.Fraction(timestamp))
        if channels is not None:
            frame = frame.convert(channels)
        assert isinstance(frame, FrameVideo), frame.__class__.__name__
        return frame

    @property
    def type(self) -> str:
        return "video"

    @property
    def width(self) -> int:
        """
        ** Width of all images in the stream. **
        """
        if self.is_space_continuous and hasattr(self.node, "shape"):
            return self.node.shape[1]
        raise NotImplementedError


class StreamVideoWrapper(StreamWrapper, StreamVideo):
    """
    ** Allows to dynamically transfer the methods of an instanced video stream. **

    This can be very useful for implementing filters.

    Attribute
    ---------
    stream : movia.core.classes.stream_video.StreamVideo
        The video stream containing the properties to be transferred (readonly).
        This stream is one of the input streams of the parent node.
    """

    def __init__(self, node: Filter, index: numbers.Integral):
        """
        Parameters
        ----------
        filter : movia.core.classes.filter.Filter
            The parent node, transmitted to ``movia.core.classes.stream.Stream``.
        index : number.Integral
            The index of the video stream among all the input streams of the ``node``.
            0 for the first, 1 for the second ...
        """
        assert isinstance(node, Filter), node.__class__.__name__
        assert len(node.in_streams) > index, f"only {len(node.in_streams)} streams, no {index}"
        assert isinstance(node.in_streams[index], StreamVideo), "the stream must be video type"
        super().__init__(node, index)

    def _snapshot(self, timestamp: fractions.Fraction) -> FrameVideo:
        return self.stream._snapshot(timestamp)

    @property
    def height(self) -> int:
        return self.stream.height

    @property
    def is_space_continuous(self) -> bool:
        return self.stream.is_space_continuous

    @property
    def width(self) -> int:
        return self.stream.width
