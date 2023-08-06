#############################################################################
#                                                                           #
#           Copyright (C) LaVision GmbH.  All Rights Reserved.              #
#                                                                           #
#############################################################################

from dataclasses import dataclass


@dataclass
class Grid:
    x: int
    y: int
    z: int
