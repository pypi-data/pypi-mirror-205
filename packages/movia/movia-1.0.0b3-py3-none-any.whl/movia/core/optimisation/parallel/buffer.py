#!/usr/bin/env python3

"""
** Buffer management in threading loop. **
------------------------------------------
"""

import os
import threading
import typing
import queue



class _ImapThread(threading.Thread):
    """
    ** Manage exception and autostart. **
    """

    def __init__(self, *args, func=None, arg=None, **kwargs):
        self.func = func
        self.arg = arg

        self.result = None
        self.exception = False

        super().__init__(*args, **kwargs)
        self.start()

    def run(self):
        try:
            self.result = self.func(self.arg)
        except Exception as err:
            self.exception = True
            self.result = err

    def get(self):
        """
        ** Return the result. **
        """
        self.join()
        if self.exception:
            raise self.result
        return self.result


def imap(func: typing.Callable, iterable: typing.Iterable, maxsize: int=None):
    """
    ** Same as multiprocessing.pool.ThreadPool.imap but with a limited output buffer. **

    Parameters
    ----------
    func : callable
        The function to evaluate in an over thread.
    iterable : iterable
        The parameters to give a the function.
    maxsize : int, default=os.cpu_count()
        The size of the buffer.

    Examples
    --------
    >>> from movia.core.optimisation.parallel.buffer import imap
    >>> for _ in imap(print, range(4), maxsize=2):
    ...     print("hello")
    ...
    0
    1
    hello
    2
    hello
    3
    hello
    hello
    >>>
    """
    assert callable(func), func.__class__.__name__
    assert hasattr(iterable, "__iter__"), iterable.__class__.__name__
    if maxsize is None:
        maxsize = os.cpu_count()
    assert isinstance(maxsize, int), maxsize.__class__.__name__
    assert maxsize >= 1, maxsize # avoid infinite blocking

    buff = queue.Queue()
    queue_size = 0
    for arg in iterable:
        buff.put(_ImapThread(func=func, arg=arg, daemon=True))
        queue_size += 1
        if queue_size < maxsize:
            continue
        yield buff.get().get()
        queue_size -= 1
    for _ in range(queue_size):
        yield buff.get().get()
