#############################################################################
#                                                                           #
#           Copyright (C) LaVision GmbH.  All Rights Reserved.              #
#                                                                           #
#############################################################################

from typing import Dict, Set
import numpy as np
from ..types.buffer import Buffer
from ..types.component import Component
from ..types.frame import Frame, ImageFrame, VectorFrame
from .validate_attributes import validate_attributes
from .validate_common import scalar_types


def map_component_to_dtype(buffer: Buffer) -> Dict[str, np.dtype]:
    result = {}
    for frame in buffer:
        for name, component in frame.components.items():
            if not isinstance(component, Component):
                raise TypeError(f"expected Component, got {type(component).__name__}")
            if name not in result:
                dtype = component.dtype
                if name in ("MASK", "ENABLED"):
                    if dtype != np.dtype("uint8"):
                        raise TypeError(f"component {name} should have dtype uint8")
                else:
                    if dtype not in scalar_types:
                        raise TypeError(f"component {name} has dtype {dtype}, expected one of {scalar_types}")
                result[name] = dtype
            else:
                old = result[name]
                new = component.dtype
                if old != new:
                    raise TypeError(f"component {name} has dtype {old} in some frames and {new} in others")
    return result


def validate_frame(frame: Frame):
    validate_attributes(frame.attributes)

    depths = [len(component) for component in frame.components.values()]
    if len(set(depths)) != 1:
        raise ValueError(f"expected all components to have same number of planes, got {depths}")
    # no 0 check needed, already done before

    shapes = [component.shape for component in frame.components.values()]
    if len(set(shapes)) != 1:
        raise ValueError(f"expected all components to have same shape, got {shapes}")

    for name, component in frame.components.items():
        dtypes = [plane.dtype for plane in component]
        if len(set(dtypes)) != 1:
            raise TypeError(f"expected all planes in component {name} to have same dtype, got {dtypes}")

        shapes = [plane.shape for plane in component]
        if len(set(shapes)) != 1:
            raise ValueError(f"expected all planes in component {name} to have same shape, got {shapes}")

        for plane in component:
            if not isinstance(plane, np.ndarray):
                raise TypeError(f"a plane in component {name} has type {type(plane).__name__}, expected np.ndarray")


def validate_scalar_fields(names: Set[str]):
    for name in names:
        if name[:3] != "TS:":
            raise ValueError(f"invalid component name {name}, did you mean TS:{name}?")


def validate_image_buffer(buffer: Buffer, component_to_dtype: Dict[str, np.dtype]):
    for frame in buffer:
        if not isinstance(frame, ImageFrame):
            raise TypeError(f"expected ImageFrame, got {type(input).__name__}")

    if "PIXEL" not in component_to_dtype:
        raise ValueError("image frame has no PIXEL component")

    validate_scalar_fields(set(component_to_dtype) - {"PIXEL", "MASK"})


def validate_vector_buffer(buffer: Buffer, component_to_dtype: Dict[str, np.dtype]):
    for frame in buffer:
        if not isinstance(frame, VectorFrame):
            raise TypeError(f"expected VectorFrame, got {type(input).__name__}")

    choices_list = [frame.choices for frame in buffer]
    if len(set(choices_list)) != 1:
        raise ValueError(f"expected all frames to have same number of choices, got {choices_list}")
    choices = choices_list[0]
    if choices not in (1, 2, 3, 4):
        raise ValueError(f"vector frame expected to have 1, 2, 3 or 4 choices, got {choices}")

    # same for all buffers, safe to assume, no need to validate:
    is_3c = buffer[0].is_3c

    prefixes = "UVW" if is_3c else "UV"
    main_components = [f"{c}{i}" for c in prefixes for i in range(choices)]

    for name in main_components:
        if name not in component_to_dtype:
            raise ValueError(f"vector frame has {choices} choices but no {name} component")
        else:
            dtype = component_to_dtype[name]
            if dtype != np.float32:
                raise TypeError(f"vector frame component {name} expected to have dtype float32, got {dtype}")

    usual_components = {*main_components, "MASK", "ENABLED", "ACTIVE_CHOICE"}
    scalar_fields = set(component_to_dtype) - usual_components
    validate_scalar_fields(scalar_fields)


def validate_buffer(buffer: Buffer) -> None:
    if len(buffer) == 0:
        raise ValueError("buffer has no frames")

    shapes = [frame.shape for frame in buffer]
    if len(set(shapes)) != 1:
        raise ValueError(f"expected all frames to have same shape, got {shapes}")
    shape = shapes[0]
    if len(shape) != 2 or 0 in shape:
        raise ValueError(f"frame has invalid shape {shape}, expected 2 dimensions")

    validate_attributes(buffer.attributes)

    depths = [len(frame) for frame in buffer]
    if len(set(depths)) != 1:
        raise ValueError(f"expected all frames to have same number of planes, got {depths}")
    if depths[0] == 0:
        raise ValueError("frame has no planes")

    component_names = [tuple(sorted(frame.components.keys())) for frame in buffer]
    if len(set(component_names)) != 1:  # then it is at least 2
        a, b, *_ = component_names
        diff = set(a).symmetric_difference(set(b))
        raise ValueError(f"some frames have {diff} components and some don't")

    type_ids = [frame.type_id for frame in buffer]
    if len(set(type_ids)) != 1:
        raise TypeError(f"expected all frames to have same type, got {type_ids}")
    type_id = type_ids[0]

    component_to_dtype = map_component_to_dtype(buffer)

    if type_id == "ImageFrame":
        validate_image_buffer(buffer, component_to_dtype)
    elif type_id == "VectorFrame":
        validate_vector_buffer(buffer, component_to_dtype)
    else:
        raise TypeError(f"unknown frame type: {type_id}")

    for frame in buffer:
        validate_frame(frame)
