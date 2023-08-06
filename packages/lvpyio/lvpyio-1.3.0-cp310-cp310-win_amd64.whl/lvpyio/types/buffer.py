#############################################################################
#                                                                           #
#           Copyright (C) LaVision GmbH.  All Rights Reserved.              #
#                                                                           #
#############################################################################

from typing import Dict, List, Any
from dataclasses import dataclass
from .frame import Frame


@dataclass
class Buffer:
    frames: List[Frame]
    attributes: Dict[str, Any]

    def __len__(self):
        return len(self.frames)

    def __getitem__(self, index):
        return self.frames[index]

    def plot(self, frame=0, plane=0, *, show=True):
        """
        Useful to get a first impression of data in the buffer.
        Requires matplotlib.
        """
        return self[frame].plot(plane, show=show)

    def as_masked_array(self, frame=0, plane=0):
        """
        Useful to get a first impression of data in the buffer.
        Doesn't require matplotlib.
        """
        return self[frame].as_masked_array(plane)
