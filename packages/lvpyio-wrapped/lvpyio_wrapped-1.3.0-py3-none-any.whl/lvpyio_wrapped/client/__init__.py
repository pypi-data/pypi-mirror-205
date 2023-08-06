#############################################################################
#                                                                           #
#           Copyright (C) LaVision GmbH.  All Rights Reserved.              #
#                                                                           #
#############################################################################

import subprocess
import atexit
import sys
import os
import zmq
from .. import SUBPROCESS_TOKEN

context = zmq.Context()


@atexit.register
def destroy_context():
    if not context.closed:
        context.destroy(linger=0)


socket = context.socket(zmq.REQ)
socket.setsockopt(zmq.TCP_KEEPALIVE, 1)
socket.setsockopt(zmq.TCP_KEEPALIVE_IDLE, 300)
socket.setsockopt(zmq.TCP_KEEPALIVE_INTVL, 30)
port = socket.bind_to_random_port("tcp://127.0.0.1")
python = sys.executable
pid = os.getpid()
service = subprocess.Popen(
    [
        python, "-m", "lvpyio_wrapped.service",
        str(port), str(pid), SUBPROCESS_TOKEN
    ]
)


@atexit.register
def terminate_service():
    if service.poll() is None:
        try:
            # Give the service a chance to quit gracefully:
            socket.send_multipart([b"quit"], zmq.NOBLOCK)
            if socket.poll(2000):
                socket.recv_multipart()
        except Exception:
            pass  # exit handlers print traceback by default, we suppress it
        finally:
            # If it fails, terminate forcefully. Examples of how it can fail:
            # - Service has not started, socket.send raises zmq.error.Again
            # (e.g. when you import lvpyio_wrapped and quit immediately)
            # - Service had an error and doesn't respond, socket.poll times out
            service.terminate()
            service.wait()
