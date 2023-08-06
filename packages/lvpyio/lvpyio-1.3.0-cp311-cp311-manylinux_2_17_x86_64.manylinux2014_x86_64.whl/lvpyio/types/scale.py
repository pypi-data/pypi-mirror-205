#############################################################################
#                                                                           #
#           Copyright (C) LaVision GmbH.  All Rights Reserved.              #
#                                                                           #
#############################################################################

from dataclasses import dataclass


@dataclass
class Scale:
    slope: float = 1.0
    offset: float = 0.0
    unit: str = ""
    description: str = ""

    def label(self):
        return f"{self.description} [{self.unit}]"


@dataclass
class Scales:
    x: Scale
    y: Scale
    z: Scale
    i: Scale
