#############################################################################
#                                                                           #
#           Copyright (C) LaVision GmbH.  All Rights Reserved.              #
#                                                                           #
#############################################################################

from typing import Dict, Any
from dataclasses import dataclass
import warnings
import numpy as np
from abc import ABCMeta, abstractmethod, abstractproperty

from .component import Components
from .scale import Scales
from .plot_utils import plot_image, plot_vector_field

# scaled vector data is float64 to be consistent with scaled image data
vec2c = np.dtype([("u", "f8"), ("v", "f8")])
vec3c = np.dtype([("u", "f8"), ("v", "f8"), ("w", "f8")])


@dataclass
class Frame(metaclass=ABCMeta):
    components: Components
    scales: Scales
    attributes: Dict[str, Any]

    @property
    def type_id(self):
        return type(self).__name__

    @abstractmethod
    def __len__(self):
        return NotImplemented

    def __getitem__(self, index):
        pairs = self.components.items()
        return {k: v[index] for k, v in pairs}

    def _scaled_intensity(self, values):
        # doesn't preserve dtype!
        return self.scales.i.offset + values * self.scales.i.slope

    @abstractproperty
    def shape(self):
        return NotImplemented

    @abstractmethod
    def as_masked_array(self, plane=0):
        return NotImplemented

    @abstractmethod
    def plot(self, plane=0, *, show=True):
        return NotImplemented

    @property
    def masks(self):
        try:
            return self.components['MASK'].planes
        except KeyError:
            # no mask, assuming that all vectors are valid
            # can't use nomask here because it would be all zeros, not all ones
            return [
                np.ones(self.shape, dtype=np.uint8)
                for _ in self
            ]


class ImageFrame(Frame):

    def __init__(self, *args):
        super().__init__(*args)
        attributes = self.attributes
        if "RGBFrame" in attributes and attributes["RGBFrame"] != "0":
            warnings.warn(
                "This is a Bayer pattern image, interpret it accordingly"
            )

    @property
    def shape(self):
        # we assume the same shape for all components and planes:
        return self.images[0].shape

    def __len__(self):
        return len(self.images)

    @property
    def images(self):
        try:
            return self.components['PIXEL'].planes
        except KeyError:
            raise ValueError(
                "malformed data, image frame without PIXEL component"
            )

    def as_masked_array(self, plane=0):
        return np.ma.array(
            self._scaled_intensity(self.images[plane]),
            # from DaVis convention (1 means valid)
            # to numpy convention (1 means invalid):
            mask=np.logical_not(self.masks[plane]),
            hard_mask=True
        )

    def plot(self, plane=0, *, show=True):
        return plot_image(self.as_masked_array(plane), self.scales, show=show)


class VectorFrame(Frame):

    def __init__(self, components, scales, attributes, grid, choices):
        super().__init__(components, scales, attributes)
        self.grid = grid
        self.choices = choices

    @property
    def shape(self):
        # we assume the same shape for all components and planes:
        try:
            return self.components['U0'][0].shape
        except KeyError:
            raise ValueError(
                "malformed data, vector frame without U0 component"
            )

    def __len__(self):
        # we assume the same number of planes for all components:
        try:
            return len(self.components['U0'])
        except KeyError:
            raise ValueError(
                "malformed data, vector frame without U0 component"
            )

    @property
    def enabled(self):
        try:
            return self.components['ENABLED'].planes
        except KeyError:
            # no data about enabled/disabled vectors,
            # assuming that all vectors are enabled
            return [
                np.ones(self.shape, dtype=np.uint8)
                for _ in self.components['U0']
            ]

    @property
    def active_choice(self):
        try:
            return self.components['ACTIVE_CHOICE'].planes
        except KeyError:
            # no data about active choice, assuming 0
            return [
                np.zeros(self.shape, dtype=np.int32)
                for _ in self.components['U0']
            ]

    @property
    def is_3c(self):
        return "W0" in self.components

    def _as_unscaled_masked_array(self, plane):
        result = np.ma.empty(
            self.shape,
            dtype=vec3c if self.is_3c else vec2c,
            fill_value=0
        )

        u = result["u"]
        v = result["v"]
        w = result["w"] if self.is_3c else None

        u[:] = self.components['U0'][plane]
        v[:] = self.components['V0'][plane]
        if w is not None:
            w[:] = self.components['W0'][plane]

        for i in range(1, self.choices):
            chosen = (self.active_choice[plane] == i)
            u[chosen] = self.components[f'U{i}'][plane][chosen]
            v[chosen] = self.components[f'V{i}'][plane][chosen]
            if w is not None:
                w[chosen] = self.components[f'W{i}'][plane][chosen]

        # from DaVis convention (1 means valid)
        # to numpy convention (1 means invalid):
        mask = np.logical_not(self.masks[plane] & self.enabled[plane])
        # We can't just leave arbitrary values in masked areas, or they would
        # produce overflow warnings and invalid value warnings during plotting:
        result[mask] = 0.0
        result.mask = mask
        result.harden_mask()
        return result

    def _scale_masked_array_in_place(self, arr) -> None:
        u = arr["u"]
        v = arr["v"]
        u[:] = self._scaled_intensity(u) * np.sign(self.scales.x.slope)
        v[:] = self._scaled_intensity(v) * np.sign(self.scales.y.slope)
        if self.is_3c:
            w = arr["w"]
            w[:] = self._scaled_intensity(w) * np.sign(self.scales.z.slope)

    def as_masked_array(self, plane=0):
        arr = self._as_unscaled_masked_array(plane)
        self._scale_masked_array_in_place(arr)
        return arr

    def plot(self, plane=0, *, show=True):
        unscaled = self._as_unscaled_masked_array(plane)
        scaled = unscaled.copy()
        self._scale_masked_array_in_place(scaled)
        return plot_vector_field(
            unscaled,
            scaled,
            self.is_3c,
            self.scales,
            self.grid,
            show=show
        )
