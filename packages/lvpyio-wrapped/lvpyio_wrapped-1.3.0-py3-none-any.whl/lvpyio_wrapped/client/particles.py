#############################################################################
#                                                                           #
#           Copyright (C) LaVision GmbH.  All Rights Reserved.              #
#                                                                           #
#############################################################################

import pickle
from lvpyio.types.particles import Type
from .send_command import send_command
from ..chunkify import chunkify_bytes


class _ParticleFieldBase:
    def __init__(self, uid: bytes, metadata):
        self._uid = uid
        self.attributes, self.bounds, self.scales, self.track_count, self.scalar_scales, self._block_count, self._repr = metadata
        self.closed = False

    def __getitem__(self, block_index):

        if self.closed:
            raise ValueError("can't use closed set")

        if not isinstance(block_index, int):
            raise TypeError(f"indices must be integers, not {type(block_index)}")

        parts = send_command(b"block_from_particles", self._uid, b"%d" % block_index)
        return pickle.loads(b"".join(parts))

    def times(self):
        parts = send_command(b"times_from_particles", self._uid)
        return pickle.loads(b"".join(parts))

    def tracks(self):
        parts = send_command(b"tracks_from_particles", self._uid)
        return pickle.loads(b"".join(parts))

    def single_track(self, index):
        parts = send_command(b"track_from_particles", self._uid, b"%d" % index)
        return pickle.loads(b"".join(parts))

    @property
    def type_id(self):
        return Type(self._pulses_per_block)

    def __len__(self):
        return self._block_count

    def __repr__(self):
        return self._repr

    def close(self):
        """
        Closes the particle field set, frees the resources.
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
        raise NotImplementedError("Particle fields should not be pickled")


class TimeResolvedParticleField(_ParticleFieldBase):
    _pulses_per_block = 1


class DoublePulseParticleField(_ParticleFieldBase):
    _pulses_per_block = 2


class FourPulseParticleField(_ParticleFieldBase):
    _pulses_per_block = 4


def read_particles(path):
    """
    Read a particle field.

    Arguments:
    path: str -- path to set containing a particle field

    Returns: a TimeResolvedParticleField object,
             or a DoublePulseParticleField object,
             or a FourPulseParticleField object
    """

    # we don't support particle field multisets, so we can, unlike in Set class, load metadata immediately
    [pulses_per_block], uid, *pickled_metadata = send_command(b"read_particles", path.encode())
    metadata = map(pickle.loads, pickled_metadata)
    if pulses_per_block == 1:
        return TimeResolvedParticleField(uid, metadata)
    elif pulses_per_block == 2:
        return DoublePulseParticleField(uid, metadata)
    else:  # pulses_per_block == 4
        return FourPulseParticleField(uid, metadata)


def write_particles(input, path):
    """
    Write a particle field.
    Argumens:
    input -- output of `read_particles` or a user-defined dict
    path: str -- where the particle field should be written

    Returns: None
    """

    if isinstance(input, _ParticleFieldBase):
        _ = send_command(b"write_particles_existing", path.encode(), input._uid)
    else:
        parts = chunkify_bytes(pickle.dumps(input))
        _ = send_command(b"write_particles_fresh", path.encode(), *parts)
