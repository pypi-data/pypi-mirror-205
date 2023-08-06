#############################################################################
#                                                                           #
#           Copyright (C) LaVision GmbH.  All Rights Reserved.              #
#                                                                           #
#############################################################################

import numpy as np
from .buffer import Buffer
from .frame import vec2c, vec3c

IMAGE = "SET_TYPE_ID_IMAGE"
RECORDING = "SET_TYPE_ID_RECORDING"
VECTOR = "SET_TYPE_ID_VECTOR"
PARTICLE_FIELD = "ParticleField"


def guess_output_set_type(input) -> str:
    """
    Guesses the input set type for writing (e.g. by checking the first buffer).
    Performs no validation.
    Returns SET_TYPE_ID_IMAGE or SET_TYPE_ID_VECTOR.
    """
    if len(input) == 0:
        raise ValueError("set is empty")

    if type(input).__name__ == "Set":
        # can't use isinstance here: there are two Set types, one of them in
        # lvpyio.io, and this module should not depend on lvpyio.io
        if input.type_id in (IMAGE, RECORDING):
            return IMAGE
        else:
            return VECTOR
    elif isinstance(input, list):
        buffer = input[0]
        if len(buffer) == 0:
            raise ValueError("first buffer in set is empty")

        if isinstance(buffer, Buffer):
            frame = buffer[0]
            if frame.type_id == "ImageFrame":
                return IMAGE
            else:
                return VECTOR
        elif isinstance(buffer, np.ndarray):
            if buffer.dtype in (vec2c, vec3c):
                return VECTOR
            else:
                return IMAGE
        elif isinstance(buffer, list) and isinstance(buffer[0], np.ndarray):
            if buffer[0].dtype in (vec2c, vec3c):
                return VECTOR
            else:
                return IMAGE
        else:
            raise TypeError(f"expected Set, list[Buffer], list[np.ndarray] or list[list[np.ndarray]], got list[{type(buffer).__name__}]")
    else:
        raise TypeError(f"expected Set, list[Buffer], list[np.ndarray] or list[list[np.ndarray]], got {type(input).__name__}")
