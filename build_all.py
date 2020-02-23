#!/usr/bin/env python3

# Script to build all benchmarks

# Copyright (C) 2017, 2019 Embecosm Limited
#
# Contributor: Graham Markall <graham.markall@embecosm.com>
# Contributor: Jeremy Bennett <jeremy.bennett@embecosm.com>
#
# This file is part of Embench.

# SPDX-License-Identifier: GPL-3.0-or-later

"""
Build all Embench programs.
"""

# System packages
import os
import sys

# Local packages
import embase
import embuild


def main():
    """Main program to drive building of benchmarks."""
    # Parse the arguments, set up logging and then validate the
    # arguments. This will also set up the environment
    raw_args = embuild.RawArgs(os.path.abspath(os.path.dirname(__file__)))
    log = embase.Logger(raw_args.logdir(), 'build')
    cooked_args = embuild.CookedArgs(raw_args, log)
    cooked_args.log()
    arglist = cooked_args.all_args()

    # Compiler and linker
    tools = embuild.Tools(arglist, log)

    # Build the support code
    support = embuild.Support(tools, arglist, log)
    successful = support.success()
    if successful:
        log.debug(f'Compilation of support files successful')
    else:
        log.error(f'ERROR: Compilation of support files failed.')
        sys.exit(1)

    # Find and log the benchmarks
    benchmarks = embuild.Benchmark.find_all(arglist['srcdirs']['src'])
    embuild.Benchmark.log_all(benchmarks, log)

    for bench in benchmarks:
        built_bench = embuild.Benchmark(bench, support, tools, log)
        successful &= built_bench.success()

    if successful:
        log.info('All benchmarks built successfully')


# Make sure we have new enough Python and only run if this is the main package
embase.check_python_version(3, 6)
if __name__ == '__main__':
    sys.exit(main())
