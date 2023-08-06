#############################################################################
#                                                                           #
#           Copyright (C) LaVision GmbH.  All Rights Reserved.              #
#                                                                           #
#############################################################################

import pickle
from .send_command import send_command
from ..chunkify import chunkify_bytes


def read_buffer(path):
    """
    Read a buffer.

    Arguments:
    path: str -- path to buffer

    Returns: a Buffer object.
    """

    parts = send_command(b"read_buffer", path.encode())
    return pickle.loads(b"".join(parts))


def write_buffer(buffer, path):
    """
    Write a buffer.
    If the file already exists, it will be overwritten without warning.

    Arguments:
    buffer: can be a Buffer object, a ndarray or a list of ndarray
    path: str -- path to buffer.

    Returns: None
    """

    parts = chunkify_bytes(pickle.dumps(buffer))
    _ = send_command(b"write_buffer", path.encode(), *parts)
