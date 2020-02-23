#!/usr/bin/env python3

# Initialization of the embase package

# Copyright (C) 2020 Embecosm Limited
#
# Contributor: Jeremy Bennett <jeremy.bennett@embecosm.com>
#
# This file is part of Embench.

# SPDX-License-Identifier: GPL-3.0-or-later

"""
Import the classes from the embase package. Only the classes we expose to the
outside world.
"""

from embase.logger import Logger
from embase.utils import check_python_version
from embase.utils import arglist_to_str
