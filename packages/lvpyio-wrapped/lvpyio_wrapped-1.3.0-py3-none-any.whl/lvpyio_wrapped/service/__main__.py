#############################################################################
#                                                                           #
#           Copyright (C) LaVision GmbH.  All Rights Reserved.              #
#                                                                           #
#############################################################################

import warnings
import platform
import pickle
import atexit
import sys
import os

import psutil
import zmq

from .commands import dispatch_command

context = zmq.Context()
socket = context.socket(zmq.REP)
port = int(sys.argv[1])
client_pid = int(sys.argv[2])
socket.connect(f"tcp://127.0.0.1:{port}")
this_process = psutil.Process(os.getpid())


@atexit.register
def destroy_context():
    if not context.closed:
        context.destroy(linger=0)


# If an exception occurs in this file, the following might happen:
# - If it occurs before receiving command and args from client: service will
# terminate abnormally (return code 1), traceback will be printed to stderr,
# client will raise RuntimeError.
# - If it occurs after receiving command and args from client, but before
# sending the results to client: client will reraise the Exception with correct
# message (but old traceback will be lost).
# - If it occurs after sending the results to client: it will pass silently.

while True:
    try:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            while not socket.poll(10000, zmq.POLLIN):  # 10s
                # If the client process has exited abnormally, we need to shut
                # the service down.
                parent = this_process.parent()
                if parent is None:
                    # There is no more parent. Happens on Windows.
                    sys.exit()
                elif parent.pid != client_pid:
                    # A parent exists, but it's not the client process.
                    if platform.system() == "Windows":
                        # On Windows, it means the service runs in some kind of
                        # wrapper, most likely inside a venv. Venv on Linux,
                        # on the other hand, doesn't use wrapper processes.
                        grandparent = parent.parent()
                        if grandparent is None:
                            sys.exit()
                        elif grandparent.pid != client_pid:
                            # Chains that deep can happen on Windows if e.g.
                            # lvpyio_wrapped is imported by Hy running in a venv.
                            if grandparent.parent() is None:
                                sys.exit()
                            # In theory, process chains of arbitrary length can
                            # occur, but handling that would be overkill.
                    else:
                        # On Linux, it means the client has died and another
                        # process (e.g. init) became the new parent process.
                        sys.exit()
            command, *args = socket.recv_multipart()
            results = dispatch_command(command, args)
            status = pickle.dumps(w)
            socket.send_multipart([status, *results])
            del results
            if command == b"quit":
                break
    except KeyboardInterrupt:
        if socket.poll(0, zmq.POLLOUT):
            socket.send(b'')  # the client expects us to send something
    except Exception as cant_process_command:
        try:
            status = pickle.dumps(cant_process_command)
            socket.send_multipart([status])
        except zmq.ZMQError:
            # Attempt to send exception to the client failed,
            # probably because the exception occured before recv or after send.
            # No recovery possible, no nice error reporting possible.
            # At least we can reraise it so its traceback would be printed:
            raise cant_process_command from None
