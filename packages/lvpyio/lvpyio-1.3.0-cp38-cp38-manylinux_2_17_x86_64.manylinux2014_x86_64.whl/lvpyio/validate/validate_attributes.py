#############################################################################
#                                                                           #
#           Copyright (C) LaVision GmbH.  All Rights Reserved.              #
#                                                                           #
#############################################################################

from typing import Any, Dict, Union
import numpy as np
from .validate_common import scalar_types


def validate_attribute_plane(plane: np.ndarray, name: str):
    if plane.dtype not in scalar_types:
        raise TypeError(f"attribute plane {name} has invalid dtype {plane.dtype}, expected one of {scalar_types}")
    if len(plane.shape) != 2 or 0 in plane.shape:
        raise ValueError(f"attribute plane {name} has invalid shape {plane.shape}, expected 2 dimensions")


def validate_attribute_name(name: str):
    if isinstance(name, str):
        try:
            name.encode("latin-1")
        except UnicodeEncodeError:
            raise ValueError(f"attribute name should be encodable as latin-1, got {name}")
    else:
        raise TypeError(f"attribute name should be str, got {type(name).__name__}")


def validate_attribute_value(value: Union[str, np.ndarray], name: str):
    if isinstance(value, str):
        pass
    elif isinstance(value, np.ndarray):
        validate_attribute_plane(value, name)
    else:
        raise TypeError(f"attribute value should be str or np.ndarray, got {type(value).__name__}")


def validate_attributes(attributes: Dict[str, Any]):
    for name, value in attributes.items():
        validate_attribute_name(name)
        validate_attribute_value(value, name)
