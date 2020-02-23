#!/usr/bin/env python3

# Module to handle benchmarks as part of the embuild package

# Copyright (C) 2019, 2020 Embecosm Limited
#
# Contributor: Jeremy Bennett <jeremy.bennett@embecosm.com>
#
# This file is part of Embench.

# SPDX-License-Identifier: GPL-3.0-or-later

"""
Module to handle benchmarks and support.

This includes the associated support code.
"""

import os


class Support:
    """A class to handle support code.

    This class turns support code into binary code that can subsequently be
    linked in to create an executable benchmark.
    """
    def __compile_support(self):
        """Compile the general support files."""
        res, objs = self.__tools.compile_files(
            ['beebsc.c', 'main.c'],
            self.__cooked['srcdirs']['support'],
            self.__cooked['bindirs']['support']
        )
        self.__support_objs = self.__tools.create_link_abs_input_list(
            objs, self.__cooked['bindirs']['support']
        )
        return res

    def __compile_dummies(self):
        """Compile any dummy libraries"""
        # Create a list of dummy source file namesxs
        dlist = list()
        for dlib in self.__cooked['libs']['dummy']:
            dlist.append('dummy-' + dlib + '.c')

        self.__dummy_objs = list()
        srcdir = self.__cooked['srcdirs']['support']
        bindir = self.__cooked['bindirs']['support']
        if dlist:
            res, objs = self.__tools.compile_files(dlist, srcdir, bindir)
            self.__dummy_objs.extend(
                self.__tools.create_link_abs_input_list(objs, bindir)
            )
            return res

        return True

    def __compile_config(self):
        """Compile code provided in configuration directories
        """
        self.__config_objs = list()
        succeeded = True
        for kind in ['arch', 'chip', 'board']:
            srcdir = self.__cooked['srcdirs'][kind]
            bindir = self.__cooked['bindirs'][kind]

            # Compile all the source files (if any)
            res, objs = self.__tools.compile_dir(srcdir, bindir)

            succeeded &= res
            self.__config_objs.extend(
                self.__tools.create_link_abs_input_list(objs, bindir)
            )

        return succeeded

    def __init__(self, tools, cooked_args, log):
        """From the raw arguments we create a set of binaries."""
        self.__tools = tools
        self.__cooked = cooked_args
        self.__log = log

        # Cumulative record of whether we have compiled everything
        # successfully.
        self.__succeeded = True

        # Compile all the support files.
        self.__succeeded &= self.__compile_support()
        self.__succeeded &= self.__compile_dummies()
        self.__succeeded &= self.__compile_config()

    def success(self):
        """Accessor for the success or otherwise of compilation."""
        return self.__succeeded

    def support_objs(self):
        """Accessor for the compiled support objects."""
        return self.__support_objs

    def dummy_objs(self):
        """Accessor for the compiled dummy library objects."""
        return self.__dummy_objs

    def config_objs(self):
        """Accessor for the compiled configuration objects."""
        return self.__config_objs


class Benchmark:
    """Class to handle a benchmark, including compiling and linking it."""
    def __init__(self, bench, support, tools, log):
        """Create an executable for the given benchmark."""
        self.__bench = bench
        self.__support = support
        self.__tools = tools

        # Build and link
        self.__succeeded, objs = self.__tools.compile_benchmark(bench)
        if self.__succeeded:
            log.debug(f'Compilation of benchmark "{bench}" successful')
            self.__succeeded = self.__tools.link_benchmark(bench, objs, support)
            if self.__succeeded:
                log.debug(f'Linking of benchmark "{bench}" successful')
                log.info(f'{bench}')

    def success(self):
        """Accessor for if we succeeded in building a benchmark"""
        return self.__succeeded

    @staticmethod
    def find_all(benchdir):
        """Statis method to enumerate all the benchmarks in the supplied
        directory in alphabetical order. A benchmark is any sub-directory -
        files are silently ignored.

        Return the sorted list of benchmarks.

        """
        benchmarks = list()

        for bench in os.listdir(benchdir):
            abs_b = os.path.join(benchdir, bench)
            if os.path.isdir(abs_b):
                benchmarks.append(bench)

        benchmarks.sort()

        return benchmarks

    @staticmethod
    def log_all(benchmarks, log):
        """Static method to record all the benchmarks in the log"""
        log.debug('Benchmarks')
        log.debug('==========')

        for bench in benchmarks:
            log.debug(bench)

        log.debug('')
