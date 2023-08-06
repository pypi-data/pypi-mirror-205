#############################################################################
#                                                                           #
#           Copyright (C) LaVision GmbH.  All Rights Reserved.              #
#                                                                           #
#############################################################################

import os

# No logging will be performed, but we still need to initialize log4cxx with a
# minimal configuration file to avoid the "no appender could be found" warning.
# Relevant on Windows. No effect on Linux (we don't use a debug logger there).
os.environ["LOG4CXX_CONFIGURATION"] = os.path.join(__path__[0], "log4cxx.xml")

from .read_buffer import read_buffer
from .write_buffer import write_buffer
from .set import read_set, write_set, is_multiset, _create_set
from .particles import read_particles, write_particles
