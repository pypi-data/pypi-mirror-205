#############################################################################
#                                                                           #
#           Copyright (C) LaVision GmbH.  All Rights Reserved.              #
#                                                                           #
#############################################################################

import sys

SUBPROCESS_TOKEN = "lvpyio service subprocess"


def _is_service_subprocess():
    if len(sys.argv) != 4:
        return False

    first, *_, last = sys.argv

    # Usually, "-m" is the first argument to a service subprocess,
    # but in some cases, e.g. when using Hy, it can be different.
    # Checking the token is needed for the rare case when lvpyio_wrapped
    # is imported in some package's __init__ and the package is then
    # launched with -m.
    return first in ("-m", sys.executable) and last == SUBPROCESS_TOKEN


# If this is a service subprocess, don't import client functions!
# Otherwise a service subprocess would initialize the client,
# the client would start another service subprocess, and it would
# lead to processes spawning themselves recursively ad infinitum.
if not _is_service_subprocess():
    from .client.buffer import read_buffer, write_buffer
    from .client.set import read_set, write_set, is_multiset
    from .client.particles import read_particles, write_particles

    from lvpyio.types.frame import vec2c, vec3c
    from lvpyio.types.scale import Scale, Scales
    from lvpyio.types.particles import (particle_t, Track,
                                        unscale_particles, unscale_tracks)
    from lvpyio.types.component import Component
    from lvpyio.types.grid import Grid

    from lvpyio.version import __version__, _get_library_version
