#############################################################################
#                                                                           #
#           Copyright (C) LaVision GmbH.  All Rights Reserved.              #
#                                                                           #
#############################################################################

from typing import Any, Dict
import numpy as np
from ..types.particles import Type, particle_t
from .validate_attributes import validate_attributes


def validate_times(times) -> Type:
    if not isinstance(times, np.ndarray):
        raise TypeError(f"`times` expected to be a numpy array, is a {type(times).__name__}")

    if times.dtype != np.float64:
        raise TypeError(f"`times` expected to have dtype float64, has dtype {times.dtype}")

    if times.size == 0:
        raise ValueError("`times` should not be empty")

    if times.ndim == 1:
        return Type(1)
    elif times.ndim == 2:
        pulse_count = times.shape[1]
        if pulse_count in (2, 4):
            return Type(pulse_count)
        else:
            raise ValueError(f"`times` expected to have 2 or 4 pulses per multi-pulse, has {pulse_count}")
    else:
        raise ValueError(f"`times` expected to be a 1D or 2D array, is a {times.ndim}D array")


def validate_particles_without_track(particles, type_id, scalars):
    if type_id.value == 1:
        for i, step in enumerate(particles):
            if not isinstance(step, np.ndarray):
                raise TypeError(f"`particles` expected to contain arrays, contains {type(step).__name__}")
            if step.ndim != 1:
                raise TypeError(f"`particles` expected to contain 1D arrays, contains a {step.ndim}D array")
            if step.dtype != particle_t:
                raise TypeError(f"`particles` expected to contain arrays with dtype particle_t, contains an array with dtype {step.dtype}")
            for name, data in scalars.items():
                if data[i].shape != step.shape:
                    raise ValueError(f"malformed scalar data for scalar {name}: expected shape {step.shape}, got {data[i].shape}")
    else:
        for i, multi_pulse in enumerate(particles):
            pulse_count = type_id.value
            if not isinstance(multi_pulse, tuple):
                raise TypeError(f"`particles` expected to contain {pulse_count}-tuples, contains a {type(multi_pulse).__name__}")
            if len(multi_pulse) != pulse_count:
                raise ValueError(f"`particles` expected to contain {pulse_count}-tuples, contains a {len(multi_pulse)}-tuple")
            for j, pulse in enumerate(multi_pulse):
                if not isinstance(pulse, np.ndarray):
                    raise TypeError(f"`particles` expected to contain tuples of arrays, contains a tuple with {type(pulse).__name__}")
                if pulse.ndim != 1:
                    raise TypeError(f"`particles` expected to contain tuples of 1D arrays, contains a tuple with a {pulse.ndim}D array")
                if pulse.dtype != particle_t:
                    raise TypeError(f"`particles` expected to contain tuples of arrays with dtype particle_t, contains a tuple with an array with dtype {pulse.dtype}")
                for name, data in scalars.items():
                    if data[i][j].shape != pulse.shape:
                        raise ValueError(f"malformed scalar data for scalar {name}: expected shape {pulse.shape}, got {data[i][j].shape}")


def validate_tracks(tracks, type_id, times_length, scalar_scales):
    for track in tracks:
        if len(track) < 2:
            raise ValueError(f"track too short, has length {len(track)}")
        start = track.start
        if type_id.value == 1:
            if not isinstance(start, int):
                raise TypeError(f"track.start for time-resolved data expected to be int, has type {type(start).__name__}")
            if start < 0:
                raise ValueError(f"track.start should be positive, is {start}")
            if start >= times_length - 1:  # -1 because otherwise the track would have length 1
                raise ValueError(f"track.start is out of bounds: {start} >= {times_length - 1}")
            if start + len(track) > times_length:
                raise ValueError(f"track is too long to fit in the particle field: {track}")
        elif type_id.value == 2:
            if not isinstance(start, int):
                raise TypeError(f"track.start for 2-pulse data expected to be int, has type {type(start).__name__}")
            if start < 0:
                raise ValueError(f"track.start should be positive, is {start}")
            if start >= times_length:
                raise ValueError(f"track.start is out of bounds: {start} >= {times_length}")
            if len(track) != 2:
                raise ValueError(f"track in 2-pulse data expected to have length 2, has length {len(track)}")
        else:  # type_id.value == 4
            if not isinstance(start, tuple):
                raise TypeError(f"track.start for 4-pulse data expected to be a tuple of two ints, has type {type(start).__name__}")
            if len(start) != 2:
                raise TypeError(f"track.start for 4-pulse data expected to be a tuple of two ints, has length {len(start)}")
            i, j = start
            if not isinstance(i, int) or not isinstance(j, int):
                raise TypeError(f"track.start for 4-pulse data expected to be a tuple of two ints, contains {type(i).__name__} and {type(j).__name__}")
            if i < 0 or j < 0:
                raise ValueError(f"indices in track.start should be positive, {start} found")
            if i >= times_length:
                raise ValueError(f"first index in track.start is out of bounds: {i} >= {times_length}")
            if j >= 3:
                raise ValueError(f"second index in track.start should be <=2, is {j}")
            if j + len(track) > 4:
                raise ValueError(f"track is too long to fit in the multi-pulse: {track}")

        particles = track.particles
        if not isinstance(particles, np.ndarray):
            raise TypeError(f"track.particles expected to be a numpy array, is a {type(particles).__name__}")
        if particles.ndim != 1:
            raise ValueError(f"track.particles expected to be a 1D array, is a {particles.ndim}D array")
        if particles.dtype != particle_t:
            raise TypeError(f"track.particles expected to have dtype particle_t, has dtype {particles.dtype}")

        if track.scalars.keys() != scalar_scales.keys():
            raise ValueError(f"mismatching scalar names: {set(track.scalars.keys())} and {set(scalar_scales.keys())}")
        for name, data in track.scalars.items():
            if data.shape != track.particles.shape:
                raise ValueError(f"malformed scalar data for scalar {name}: expected shape {track.particles.shape}, got {data.shape}")


def validate_custom_particle_field(field: Dict[str, Any]):

    allowed_keys = {
        "times", "particles", "tracks", "scales",
        "attributes", "bounds", "scalar_scales",
        "scalars"
    }
    for key in field:
        if key not in allowed_keys:
            raise ValueError(f"unknown key `{key}` in custom particle field")

    if "times" not in field:
        raise ValueError("custom particle field must contain `times`")

    if "tracks" in field and "particles" in field:
        raise ValueError("custom particle fields with both `tracks` and `particles` are not allowed")

    if "tracks" not in field and "particles" not in field:
        raise ValueError("custom particle fields with neither `tracks` nor `particles` are not allowed")

    times = field["times"]
    type_id = validate_times(times)

    if "particles" in field:
        particles = field["particles"]
        if len(particles) != len(times):
            raise ValueError("`times` and `particles` should be of same length")

        if "scalars" in field and "scalar_scales" not in field:
            raise ValueError("custom particle field with IPR data contains `scalars` but no `scalar_scales`")
        if "scalar_scales" in field and "scalars" not in field:
            raise ValueError("custom particle field with IPR data contains `scalar_scales` but no `scalars`")
        scalar_scales = field.get("scalar_scales", {})
        scalars = field.get("scalars", {})
        if scalar_scales.keys() != scalars.keys():
            raise ValueError(f"mismatching scalar names: {set(scalar_scales.keys())} and {set(scalars.keys())}")

        validate_particles_without_track(particles, type_id, scalars)

    if "tracks" in field:
        validate_tracks(field["tracks"], type_id, len(times), field.get("scalar_scales", {}))
        if "scalars" in field:
            raise ValueError("custom particle field with tracks can't contain a `scalars` key, use tracks to store scalars")

    if "attributes" in field:
        validate_attributes(field["attributes"])
