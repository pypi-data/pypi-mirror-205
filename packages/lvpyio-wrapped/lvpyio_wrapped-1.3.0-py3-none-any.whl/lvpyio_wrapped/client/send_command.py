#############################################################################
#                                                                           #
#           Copyright (C) LaVision GmbH.  All Rights Reserved.              #
#                                                                           #
#############################################################################

from typing import List
import warnings
import pickle
import zmq
from . import socket, service

CRASHED = (
    "reader unexpectedly terminated, please report a bug "
    "to python@lavision.de and restart Python"
)


def send_command(command: bytes, *args: bytes) -> List[bytes]:
    while not socket.poll(1000, zmq.POLLOUT):
        # Timeout has been reached but nothing happened.
        # The event that means "you can send data without blocking" hasn't occured.
        # Let's check if the service process is still alive:
        return_code = service.poll()
        if return_code is not None:
            # Service process has terminated.
            raise RuntimeError(f"{CRASHED}. Error code: {return_code}")
        # Service process is still alive.
        # Necessary if the previous command has been aborted with Ctrl+C:
        if socket.poll(0, zmq.POLLIN):
            _ = socket.recv()
            warnings.warn("previous command terminated abnormally")
        # Continue polling the socket.

    socket.send_multipart([command, *args])
    return recv_with_error_handling()


def recv_with_error_handling() -> List[bytes]:
    while not socket.poll(1000, zmq.POLLIN):
        # Timeout has been reached but nothing happened.
        # The event that means "you can receive data without blocking" hasn't occured.
        # Let's check if the service process is still alive:
        return_code = service.poll()
        if return_code is not None:
            # Service process has terminated.
            raise RuntimeError(f"{CRASHED}. Error code: {return_code}")
        # Service process is still alive, continue polling the socket.

    serialized_status, *data = socket.recv_multipart()
    status = pickle.loads(serialized_status)

    if isinstance(status, Exception):
        raise status
    else:  # status is a potentially empty list of warnings:
        for w in status:
            warnings.warn(w.message)

    return data
