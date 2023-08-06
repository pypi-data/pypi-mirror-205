#!/usr/bin/env python3

"""
** Allows you to combine overlapping streams. **
------------------------------------------------
"""

import fractions
import math
import typing

import torch

from movia.core.classes.filter import Filter
from movia.core.classes.frame_audio import FrameAudio
from movia.core.classes.frame_video import FrameVideo
from movia.core.classes.node import Node
from movia.core.classes.stream import Stream
from movia.core.classes.stream_audio import StreamAudio
from movia.core.classes.stream_video import StreamVideo
from movia.core.exceptions import OutOfTimeRange



class FilterAdd(Filter):
    """
    ** Combine the stream in once by additing the overlapping slices. **

    Examples
    --------
    >>> from movia.core.filters.basic.add import FilterAdd
    >>> from movia.core.filters.basic.translate import FilterTranslate
    >>> from movia.core.generation.audio.noise import GeneratorAudioNoise
    >>> from movia.core.generation.video.equation import GeneratorVideoEquation
    >>>
    >>> (s_audio_0,) = GeneratorAudioNoise(0).out_streams
    >>> (s_audio_1,) = FilterTranslate(GeneratorAudioNoise(.5).out_streams, 10).out_streams
    >>> (s_add_audio,) = FilterAdd([s_audio_0, s_audio_1]).out_streams
    >>> (s_video_0,) = GeneratorVideoEquation("i", "1/2", shape=(2, 2)).out_streams
    >>> (s_video_1,) = FilterTranslate(
    ...     GeneratorVideoEquation("j", "1/2", shape=(2, 2)).out_streams, 10
    ... ).out_streams
    >>> (s_add_video,) = FilterAdd([s_video_0, s_video_1]).out_streams
    >>>
    >>> s_audio_0.snapshot(8, 1, 5)
    FrameAudio(Fraction(8, 1), 1, [[ 0.51332252  0.6962532  -0.3611679  -0.62504067  0.82771811]
                                   [ 0.22561401 -0.41682793  0.53702945  0.27432338  0.54749512]],
                                  dtype=torch.float64)
    >>> s_audio_1.snapshot(10, 1, 3)
    FrameAudio(Fraction(10, 1), 1, [[-0.48753882  0.45331555 -0.94927975]
                                    [-0.64931847 -0.13948568  0.4026663 ]],
                                   dtype=torch.float64)
    >>> s_add_audio.snapshot(8, 1, 5)
    FrameAudio(Fraction(8, 1), 1, [[ 0.51332252  0.6962532  -0.84870671 -0.17172512 -0.12156164]
                                   [ 0.22561401 -0.41682793 -0.11228902  0.1348377   0.95016141]],
                                  dtype=torch.float64)
    >>>
    >>> s_video_0.snapshot(10)
    FrameVideo(Fraction(10, 1), [[[  0 128]
                                  [  0 128]]
    <BLANKLINE>
                                 [[255 128]
                                  [255 128]]])
    >>> s_video_1.snapshot(10)
    FrameVideo(Fraction(10, 1), [[[  0 128]
                                  [255 128]]
    <BLANKLINE>
                                 [[  0 128]
                                  [255 128]]])
    >>> s_add_video.snapshot(10)
    FrameVideo(Fraction(10, 1), [[[  0   0   0 192]
                                  [ 85  85  85 192]]
    <BLANKLINE>
                                 [[170 170 170 192]
                                  [255 255 255 192]]])
    >>>
    """

    def __init__(self, in_streams: typing.Iterable[Stream]):
        """
        Parameters
        ----------
        in_streams : typing.Iterable[Stream]
            Forwarded to ``movia.core.classes.filter.Filter``.
            About the overlaping portions, if the stream is an audio stream,
            a simple addition is performed but if the stream is a video stream,
            the frames are combined like a superposition of semi-transparent windows.
        """
        super().__init__(in_streams, in_streams)
        if not self.in_streams:
            return
        kind = {s.type for s in self.in_streams}
        assert len(kind) == 1, f"impossible to add different type of streams {kind}"
        kind = kind.pop()
        if kind == "audio":
            super().__init__(self.in_streams, [_StreamAudioAdd(self)])
        elif kind == "video":
            super().__init__(self.in_streams, [_StreamVideoAdd(self)])
        else:
            raise NotImplementedError(f"not yet supported {kind}")

    @classmethod
    def default(cls):
        return cls([])

    def getstate(self) -> dict:
        return {}

    def setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        assert state == {}
        FilterAdd.__init__(self, in_streams)


class _StreamVideoAdd(StreamVideo):
    """
    ** Concatenate and mix the video streams. **
    """

    def __init__(self, node: Node):
        """
        Parameters
        ----------
        node : movia.core.filters.basic.add.FilterAdd
            The node containing the StreamVideo to mix.
        """
        assert isinstance(node, FilterAdd), node.__class__.__name__
        assert node.in_streams, "requires at least 1 video stream to add"
        super().__init__(node)

    def _snapshot(self, timestamp: fractions.Fraction) -> FrameVideo:
        # selection of the concerned streams
        if not (
            streams := [
                s for s in self.node.in_streams if s.beginning <= timestamp < s.beginning+s.duration
            ]
        ):
            if timestamp < self.beginning or timestamp >= self.beginning + self.duration:
                raise OutOfTimeRange(
                    f"stream start {self.beginning} and end {self.beginning + self.duration}, "
                    f"no stream at timestamp {timestamp}"
                )
            return FrameVideo(
                timestamp, torch.zeros((self.height, self.width, 2), dtype=torch.uint8)
            )

        # optimisation case one stream
        if len(streams) == 1: # optimisation avoid casting
            return streams.pop(0)._snapshot(timestamp)

        # initialisation final frame
        if len(dim := {(s.height, s.width) for s in streams}) != 1:
            raise RuntimeError(
                f"impossible to combine frames of different shape {dim} at timestamp {timestamp}"
            )

        # general combinaison of the frames
        for i, stream in enumerate(streams):
            frame_ = stream.snapshot(timestamp)
            if frame_.channels in {1, 3}: # if no alpha chanels
                if i == 0:
                    return frame_
                frame_ = frame_.convert(channels=3)
                frame_ = frame_.to(torch.float32)
                alpha_1 = frame[..., 3].unsqueeze(2)
                frame = frame[..., :3]
                frame = frame*alpha_1 + frame_*(255-alpha_1)
                frame /= 255
                return FrameVideo(timestamp, torch.round(frame, out=frame).to(torch.uint8))

            if i == 0:
                frame = torch.zeros((*dim.pop(), 4), dtype=torch.float32) # transparent frame
            frame_ = frame_.convert(channels=4)
            frame_ = frame_.to(torch.float32)
            # compute new colors
            alpha_1 = frame[..., 3].unsqueeze(2)
            alpha_2 = frame_[..., 3].unsqueeze(2)
            coef_1 = 255 * alpha_1
            coef_2 = (255 - alpha_1) * alpha_2
            frame_[..., :3] *= coef_2
            frame[..., :3] *= coef_1
            frame[..., :3] += frame_[..., :3]
            coef_1 += coef_2
            denom = coef_1 # no copy
            del coef_1, coef_2, frame_
            denom[torch.eq(denom, 0)] = torch.nan # avoid div by 0
            frame[..., :3] /= denom
            frame[..., :3] = torch.nan_to_num(frame[..., :3], nan=0.0, out=frame[..., :3])
            # compute alpha
            alpha_1 = alpha_1.squeeze(2)
            alpha_2 = alpha_2.squeeze(2)
            alpha_1 -= 255
            alpha_2 -= 255
            frame[..., 3] = alpha_1 * alpha_2
            del alpha_1, alpha_2
            frame[..., 3] /= -255
            frame[..., 3] += 255
            # stop if future calculs will be useless (no transparent frame)
            if (torch.eq(frame[..., 3], 255)).all(): # optimisation avoid multiplication by 0
                frame = frame[..., :3]
                break
        return FrameVideo(timestamp, torch.round(frame, out=frame).to(torch.uint8))

    @property
    def beginning(self) -> fractions.Fraction:
        return min(s.beginning for s in self.node.in_streams)

    @property
    def duration(self) -> typing.Union[fractions.Fraction, float]:
        end = max(s.beginning + s.duration for s in self.node.in_streams)
        return end - self.beginning

    @property
    def height(self) -> int:
        if len(height := {s.height for s in self.node.in_streams}) != 1:
            raise AttributeError(f"combined streams do not have same height {height}")
        return height.pop()

    @property
    def is_space_continuous(self) -> bool:
        if len(val := {s.is_space_continuous for s in self.in_streams}) != 1:
            raise AttributeError("combined streams are both space continuous and discrete")
        return val.pop()

    @property
    def is_time_continuous(self) -> bool:
        if len(val := {s.is_time_continuous for s in self.in_streams}) != 1:
            raise AttributeError("combined streams are both time continuous and discrete")
        return val.pop()

    @property
    def width(self) -> int:
        if len(width := {s.width for s in self.node.in_streams}) != 1:
            raise AttributeError(f"combined streams do not have same width {width}")
        return width.pop()


class _StreamAudioAdd(StreamAudio):
    """
    ** Concatenate and add the audio streams.**
    """

    def __init__(self, node: Node):
        """
        Parameters
        ----------
        node : movia.core.filters.basic.add.FilterAdd
            The node containing the StreamAudio to add.
        """
        assert isinstance(node, FilterAdd), node.__class__.__name__
        assert node.in_streams, "requires at least 1 audio stream to add"
        super().__init__(node)

    def _snapshot(self, timestamp: fractions.Fraction, rate: int, samples: int) -> FrameAudio:
        # selection of the concerned streams
        end = timestamp + fractions.Fraction(samples, rate) # apparition of last sample
        if timestamp < self.beginning or end > self.beginning + self.duration:
            raise OutOfTimeRange(
                f"stream start {self.beginning} and end {self.beginning + self.duration}, "
                f"no stream at timestamp {timestamp} to {timestamp} + {samples}/{rate}"
            )
        streams = [
            s for s in self.node.in_streams
            if end > s.beginning and timestamp < s.beginning + s.duration
        ]

        # slices selection
        slices = [
            (
                max(s.beginning, timestamp),
                min(s.beginning+s.duration, end)
            )
            for s in streams
        ]
        slices = [(start, math.floor(rate*(end_-start))) for start, end_ in slices]
        slices = [
            (stream, start, samples)
            for stream, (start, samples) in zip(streams, slices)
            if samples > 0
        ]

        # frames portion recuperations
        frames = [stream._snapshot(start, rate, samples) for stream, start, samples in slices]
        if len(channels := {frame.channels for frame in frames}) > 1:
            raise RuntimeError(
                f"impossible to combine frames of different channels {channels} "
                f"at timestamp {timestamp} to {timestamp} + {samples}/{rate}"
            )
        channels = channels.pop() if channels else 1

        # create the new empty audio frame
        dtypes = {frame.dtype for frame in frames}
        dtypes = sorted(
            dtypes, key=lambda t: {torch.float16: 2, torch.float32: 1, torch.float64: 0}[t]
        ) + [torch.float32] # if slice = []
        frame = FrameAudio(
            timestamp, rate, torch.full((channels, samples), torch.nan, dtype=dtypes[0])
        )

        # frames addition
        for frame_ in frames:
            start = math.floor(rate * (frame_.time-timestamp))
            part = frame[:, start:start+frame_.samples]
            part = torch.where(torch.isnan(part), frame_, part+frame_)
            frame[:, start:start+frame_.samples] = part
        return frame

    @property
    def beginning(self) -> fractions.Fraction:
        return min(s.beginning for s in self.node.in_streams)

    @property
    def channels(self) -> int:
        if len(channels := {s.channels for s in self.node.in_streams}) != 1:
            raise AttributeError(f"add streams do not have same channels {channels}")
        return channels.pop()

    @property
    def duration(self) -> typing.Union[fractions.Fraction, float]:
        end = max(s.beginning + s.duration for s in self.node.in_streams)
        return end - self.beginning

    @property
    def is_time_continuous(self) -> bool:
        if len(val := {s.is_time_continuous for s in self.in_streams}) != 1:
            raise AttributeError("combined streams are both time continuous and discrete")
        return val.pop()
