#############################################################################
#                                                                           #
#           Copyright (C) LaVision GmbH.  All Rights Reserved.              #
#                                                                           #
#############################################################################

from typing import List
import pickle

from lvpyio.io import (
    read_buffer, write_buffer,
    read_set, write_set, is_multiset, _create_set,
    read_particles, write_particles
)
from ..chunkify import chunkify_bytes

# `sets` manages both buffer-based sets and particle fields
sets, uid = {}, -1


def dispatch_command(command: bytes, args: List[bytes]) -> List[bytes]:

    global uid

    if command == b"read_buffer":
        path = args[0].decode()
        buffer = read_buffer(path)
        return chunkify_bytes(pickle.dumps(buffer))

    elif command == b"write_buffer":
        path = args[0].decode()
        buffer = pickle.loads(b"".join(args[1:]))
        write_buffer(buffer, path)
        return []

    elif command == b"read_particles":
        path = args[0].decode()
        pf = read_particles(path)
        uid += 1
        sets[uid] = pf
        pulses_per_block = bytes([pf.type_id.value])  # b'\x01', '\x02', '\x04'
        metadata = [pickle.dumps(x) for x in (pf.attributes, pf.bounds, pf.scales, pf.track_count, pf.scalar_scales, len(pf), repr(pf))]
        return [pulses_per_block, b"%d" % uid, *metadata]

    elif command == b"write_particles_existing":
        path = args[0].decode()
        set_id = int(args[1])
        write_particles(sets[set_id], path)
        return []

    elif command == b"write_particles_fresh":
        path = args[0].decode()
        pf = pickle.loads(b"".join(args[1:]))
        write_particles(pf, path)
        return []

    elif command == b"times_from_particles":
        set_id = int(args[0])
        times = sets[set_id].times()
        return chunkify_bytes(pickle.dumps(times))

    elif command == b"block_from_particles":
        set_id, block_index = map(int, args)
        block = sets[set_id][block_index]
        return chunkify_bytes(pickle.dumps(block))

    elif command == b"tracks_from_particles":
        set_id = int(args[0])
        tracks = sets[set_id].tracks()
        return chunkify_bytes(pickle.dumps(tracks))

    elif command == b"track_from_particles":
        set_id, index = map(int, args)
        track = sets[set_id].single_track(index)
        return chunkify_bytes(pickle.dumps(track))

    elif command == b"is_multiset":
        path = args[0].decode()
        return [b'\x00' if is_multiset(path) else b'']

    elif command == b"read_set":
        path = args[0].decode()
        s = read_set(path)
        if isinstance(s, list):
            uids = []
            for subset in s:
                uid += 1
                uids.append(b"%d" % uid)
                sets[uid] = subset
            return [b"multi-set", *uids]
        else:
            uid += 1
            sets[uid] = s
            return [b"single set", b"%d" % uid]

    elif command == b"metadata_from_set":
        set_id = int(args[0])
        s = sets[set_id]
        return [pickle.dumps(x) for x in (s.title, s.type_id, len(s), repr(s))]

    elif command == b"buffer_from_set":
        set_id, buffer_index = map(int, args)
        buffer = sets[set_id][buffer_index]
        return chunkify_bytes(pickle.dumps(buffer))

    elif command == b"write_set_existing":
        path = args[0].decode()
        source_set_id = int(args[1])
        write_set(sets[source_set_id], path)
        return []

    elif command == b"create_set":
        type_id, path = [arg.decode() for arg in args]
        s = _create_set(path, type_id)
        uid += 1
        sets[uid] = s
        return [b"%d" % uid]

    elif command == b"set_append_buffer":
        set_id = int(args[0])
        buffer = pickle.loads(b"".join(args[1:]))
        sets[set_id]._append(buffer)
        return []

    # this command is the same for buffer-based sets and particle field sets:
    elif command == b"close_set":
        set_id = int(args[0])
        sets[set_id].close()
        del sets[set_id]
        return []

    elif command == b"quit":
        for s in sets.values():
            s.close()
        return []

    else:  # should only happen during development, when we add new commands:
        raise ValueError(f"unknown command {command!r} with args {args}")
