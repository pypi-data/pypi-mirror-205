#############################################################################
#                                                                           #
#           Copyright (C) LaVision GmbH.  All Rights Reserved.              #
#                                                                           #
#############################################################################

from typing import List
import numpy as np
from lvpyio.types.frame import vec2c, vec3c

array_dtypes = {
    np.dtype("uint16"),
    np.dtype("int32"),
    np.dtype("single"),
    np.dtype("double"),
    vec2c,
    vec3c
}


def validate_shape(shape: tuple) -> None:
    if len(shape) not in (2, 3) or 0 in shape:
        raise ValueError(
            f"array has invalid shape {shape}, expected 2 or 3 dimensions"
        )


def validate_dtype(dtype: np.dtype) -> None:
    if dtype not in array_dtypes:
        raise TypeError(
            f"array has invalid dtype {dtype}, expected one of {array_dtypes}"
        )


def validate_array(array: np.ndarray) -> None:
    if not isinstance(array, np.ndarray):
        raise TypeError(f"expected np.ndarray, got {type(array).__name__}")

    validate_shape(array.shape)
    validate_dtype(array.dtype)


def validate_array_list(arrays: List[np.ndarray]) -> None:
    if len(arrays) == 0:
        raise ValueError("input is empty")

    for array in arrays:
        if not isinstance(array, np.ndarray):
            raise TypeError(f"expected np.ndarray, got {type(array).__name__}")

    shapes = [array.shape for array in arrays]
    if len(set(shapes)) != 1:
        raise ValueError(
            f"expected all arrays to be of same shape, got {shapes}"
        )
    validate_shape(shapes[0])

    dtypes = [array.dtype for array in arrays]
    if len(set(dtypes)) != 1:
        raise TypeError(
            f"expected all arrays to be of same dtype, got {dtypes}"
        )
    validate_dtype(dtypes[0])
