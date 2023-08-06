#############################################################################
#                                                                           #
#           Copyright (C) LaVision GmbH.  All Rights Reserved.              #
#                                                                           #
#############################################################################

import pickle
from lvpyio.types.set_utils import guess_output_set_type
from .send_command import send_command
from ..chunkify import chunkify_bytes


class Set:
    """
    Imitates the behaviour of lvpyio.Set as closely as possible
    """
    def __init__(self, uid: bytes):
        self._uid = uid
        parts = send_command(b"metadata_from_set", uid)
        metadata = map(pickle.loads, parts)
        self.title, self.type_id, self._size, self._repr = metadata
        self.closed = False

    def __len__(self):
        return self._size

    def __repr__(self):
        return self._repr

    def __getitem__(self, i):
        """
        Load i-th buffer from the set.
        """

        if self.closed:
            raise ValueError("can't use closed set")

        if not isinstance(i, int):
            raise TypeError(f"indices must be integers, not {type(i)}")

        parts = send_command(b"buffer_from_set", self._uid, b"%d" % i)
        buffer = pickle.loads(b"".join(parts))
        return buffer

    def close(self):
        """
        Closes the set, frees the resources.
        Do not read from a closed set.
        """

        if not self.closed:
            _ = send_command(b"close_set", self._uid)
            self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def __getstate__(self):
        raise NotImplementedError("Set objects should not be pickled")


def is_multiset(path):
    """
    Determine if a set at a given path is a multi-set.
    A path should point either to a directory or to a .set file.
    Return False if set isn't a multi-set, True if set is a multi-set.
    """
    [result] = send_command(b"is_multiset", path.encode())
    return bool(result)


def read_set(path):
    """
    Read a set.

    Arguments:
    path: str -- path to set

    Returns: a Set object or a list of Set objects
    """

    kind, *uids = send_command(b"read_set", path.encode())
    if kind == b"multi-set":
        return [Set(uid) for uid in uids]
    else:  # kind == b"single set"
        return Set(uids[0])


def write_set(input, path):
    """
    Write a set to path.

    Arguments:
    input: can be a Set object, a list of Buffer objects,
           a list of ndarrays, or a list of lists of ndarrays
    path: str -- path to set

    Returns: None
    """

    type_id = guess_output_set_type(input)

    if isinstance(input, Set):
        _ = send_command(b"write_set_existing", path.encode(), input._uid)
    else:  # guess_set_type has asserted that input is a list of buffer-likes
        [uid] = send_command(b"create_set", type_id.encode(), path.encode())
        try:
            for buffer in input:
                parts = chunkify_bytes(pickle.dumps(buffer))
                _ = send_command(b"set_append_buffer", uid, *parts)
        finally:
            _ = send_command(b"close_set", uid)
