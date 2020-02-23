#!/usr/bin/env python3

# Module to provide utilities as part of the embase package

# Copyright (C) 2019, 2020 Embecosm Limited
#
# Contributor: Jeremy Bennett <jeremy.bennett@embecosm.com>
#
# This file is part of Embench.

# SPDX-License-Identifier: GPL-3.0-or-later

"""
Embase utilities module

A collection of generally useful classes and functions.
"""

import sys

# Make sure we have new enough python
def check_python_version(major, minor):
    """
    Check the python version is at least {major}.{minor}. Note that we can't
    use the logger yet, since it won't be set up.
    """
    if ((sys.version_info[0] < major)
            or ((sys.version_info[0] == major) and
                (sys.version_info[1] < minor))):
        print(f'ERROR: Requires Python {major}.{minor} or later')
        sys.exit(1)

def arglist_to_str(arglist):
    """Make arglist into a string"""
    for arg in arglist:
        if arg == arglist[0]:
            strarg = arg
        else:
            strarg = strarg + ' ' + arg

    return strarg
