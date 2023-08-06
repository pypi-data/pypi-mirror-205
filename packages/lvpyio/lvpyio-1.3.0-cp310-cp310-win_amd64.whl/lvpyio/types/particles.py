#############################################################################
#                                                                           #
#           Copyright (C) LaVision GmbH.  All Rights Reserved.              #
#                                                                           #
#############################################################################

from typing import Any, Dict, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import numpy as np

particle_t = np.dtype([
    ("x", "f4"),
    ("y", "f4"),
    ("z", "f4"),
    ("intensity", "f4")
])

particle_with_track_t = np.dtype([
    ("track_id", "u8"),
    ("particle", particle_t)
])

scalar_with_track_t = np.dtype([
    ("track_id", "u8"),
    ("scalar", "f4")
])


@dataclass(init=False)
class _SnapshotWithTracks:
    particles: np.ndarray  # array of particle_with_track_t
    scalars: Dict[str, np.ndarray]  # dict from str to array of scalar_with_track_t

    _track_id_to_particle_index: Dict[int, int]

    def __init__(self, particles, scalars):
        self.particles = particles
        self.scalars = scalars

        # sort particles and scalars by track_id:
        self.particles.sort(order="track_id")
        for scalar in self.scalars.values():
            scalar.sort(order="track_id")

        self._track_id_to_particle_index = {}
        for particle_index, (track_id, _) in enumerate(particles):
            self._track_id_to_particle_index[track_id] = particle_index

    def _base_repr(self):
        with_track_count = len(self.particles)
        if with_track_count == 1:
            with_track_repr = "1 particle with track"
        else:
            with_track_repr = f"{with_track_count} particles with track"

        without_track_repr = "0 particles without track"

        scalar_count = len(self.scalars)
        if scalar_count == 1:
            scalars_repr = "1 scalar"
        else:
            scalars_repr = f"{scalar_count} scalars"

        return f"{with_track_repr}, {without_track_repr}, {scalars_repr}"

    def __repr__(self):
        return f"TimeStep({self._base_repr()})"

    def particle_for_track(self, track_id) -> Tuple[float, float, float, float]:
        index = self._track_id_to_particle_index[track_id]
        _, particle = self.particles[index]
        return particle


@dataclass
class _IPRSnapshot:
    particles: np.ndarray  # array of particle_t
    scalars: Dict[str, np.ndarray]  # dict from str to array of float32

    def _base_repr(self):
        with_track_repr = "0 particles with track"

        without_track_count = len(self.particles)
        if without_track_count == 1:
            without_track_repr = "1 particle without track"
        else:
            without_track_repr = f"{without_track_count} particles without track"

        scalar_count = len(self.scalars)
        if scalar_count == 1:
            scalars_repr = "1 scalar"
        else:
            scalars_repr = f"{scalar_count} scalars"

        return f"{with_track_repr}, {without_track_repr}, {scalars_repr}"

    def __repr__(self):
        return f"TimeStep({self._base_repr()})"


class PulseWithTracks(_SnapshotWithTracks):
    def __repr__(self):
        return f"Pulse({self._base_repr()})"


class IPRPulse(_IPRSnapshot):
    def __repr__(self):
        return f"Pulse({self._base_repr()})"


class TimeStepWithTracks(_SnapshotWithTracks):
    def __init__(self, particles, scalars, attributes):
        super().__init__(particles, scalars)
        self.attributes = attributes


class IPRTimeStep(_IPRSnapshot):
    def __init__(self, particles, scalars, attributes):
        super().__init__(particles, scalars)
        self.attributes = attributes


_Pulses = Union[
    Tuple[IPRPulse, IPRPulse],
    Tuple[IPRPulse, IPRPulse, IPRPulse, IPRPulse],
    Tuple[PulseWithTracks, PulseWithTracks],
    Tuple[PulseWithTracks, PulseWithTracks, PulseWithTracks, PulseWithTracks]
]


@dataclass
class MultiPulse:
    _pulses: _Pulses
    attributes: Dict[str, Any]

    def __repr__(self):
        base_reprs = ('(' + p._base_repr() + ')' for p in self._pulses)
        return f"MultiPulse({', '.join(base_reprs)})"

    def __len__(self):
        return len(self._pulses)

    def __getitem__(self, index):
        return self._pulses[index]


@dataclass
class Track:
    start: Union[int, Tuple[int, int]]
    particles: np.ndarray  # array of particle_t
    scalars: Dict[str, np.ndarray] = field(default_factory=lambda: {})  # from str to array of floats

    def __repr__(self):

        particle_count = len(self.particles)
        if particle_count == 1:
            particles_repr = "1 particle"
        else:
            particles_repr = f"{particle_count} particles"

        scalar_count = len(self.scalars)
        if scalar_count == 1:
            scalars_repr = "1 scalar"
        else:
            scalars_repr = f"{scalar_count} scalars"

        return f"Track(start={self.start}, {particles_repr}, {scalars_repr})"

    def __len__(self):
        return len(self.particles)


class Type(Enum):
    TIME_RESOLVED = 1
    DOUBLE_PULSE = 2
    FOUR_PULSE = 4


def unscale_particles(array, scales) -> None:
    array["x"] -= scales.x.offset
    array["x"] /= scales.x.slope
    array["y"] -= scales.y.offset
    array["y"] /= scales.y.slope
    array["z"] -= scales.z.offset
    array["z"] /= scales.z.slope
    array["intensity"] -= scales.i.offset
    array["intensity"] /= scales.i.slope


def unscale_tracks(tracks, scales) -> None:
    for track in tracks:
        unscale_particles(track.particles, scales)
