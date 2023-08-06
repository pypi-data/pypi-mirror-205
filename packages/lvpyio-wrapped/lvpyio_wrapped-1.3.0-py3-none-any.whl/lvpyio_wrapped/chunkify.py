#############################################################################
#                                                                           #
#           Copyright (C) LaVision GmbH.  All Rights Reserved.              #
#                                                                           #
#############################################################################

def chunkify_bytes(message):
    SIZE = 2**20  # 1 MB
    parts = [message[i:(i + SIZE)] for i in range(0, len(message), SIZE)]
    return parts
