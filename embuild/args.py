#!/usr/bin/env python3

# Module to handle arguments as part of the embuild package

# Copyright (C) 2019, 2020 Embecosm Limited
#
# Contributor: Jeremy Bennett <jeremy.bennett@embecosm.com>
#
# This file is part of Embench.

# SPDX-License-Identifier: GPL-3.0-or-later

"""
Module to handle argument parsing.

We break this into two stages.

- an initial parse to get the raw arguments, so the log file can be set up

- a post processing phase to validate and sanitize the arguments.
"""


import argparse
import os
import re
import shutil
import sys


class RawArgs:
    """A class to handle argument parsing

    All this class does is parse the args, and construct a log directory.
    """
    def __parse_raw(self):
        """Private method to create and run the raw parse of the arguments.

        Returns an argument namespace with the parsed arguments.
        """
        # Create a parser
        parser = argparse.ArgumentParser(description='Build all the benchmarks')

        # Add the arguments
        parser.add_argument(
            '--builddir',
            default='bd',
            help='Directory in which to build benchmarks and support code',
        )
        parser.add_argument(
            '--logdir',
            default='logs',
            help='Directory in which to store logs',
        )
        parser.add_argument(
            '--arch',
            default='arm32',
            help='The architecture for which to build',
        )
        parser.add_argument(
            '--chip',
            default='generic',
            help='The chip for which to build',
        )
        parser.add_argument(
            '--board',
            default='generic',
            help='The board for which to build',
        )
        parser.add_argument('--cc', default='cc', help='C compiler to use')
        # Linker will be set to the same as 'cc' unless explicitly set on the
        # command line.
        parser.add_argument('--ld', help='Linker to use')
        parser.add_argument(
            '--cflags', default='', help='Additional C compiler flags to use'
        )
        parser.add_argument(
            '--ldflags', default='', help='Additional linker flags to use'
        )
        parser.add_argument(
            '--env',
            help=('additional environment variables, '
                  'format <V>=<val> [,<V>=<value>]...'),
        )
        parser.add_argument(
            '--cc-define1-pattern',
            default='-D{0}',
            help='Pattern to define constant for compiler',
        )
        parser.add_argument(
            '--cc-define2-pattern',
            default='-D{0}={1}',
            help='Pattern to define constant to a specific value for compiler',
        )
        parser.add_argument(
            '--cc-incdir-pattern',
            default='-I{0}',
            help='Pattern to specify include directory for the compiler',
        )
        parser.add_argument(
            '--cc-input-pattern',
            default='{0}',
            help='Pattern to specify compiler input file',
        )
        parser.add_argument(
            '--cc-output-pattern',
            default='-o {0}',
            help='Pattern to specify compiler output file',
        )
        parser.add_argument(
            '--ld-input-pattern',
            default='{0}',
            help='Pattern to specify linker input file',
        )
        parser.add_argument(
            '--ld-output-pattern',
            default='-o {0}',
            help='Pattern to specify linker output file',
        )
        parser.add_argument(
            '--user-libs', default='', help='Additional libraries to use'
        )
        parser.add_argument(
            '--dummy-libs', default='', help='Dummy libraries to build and link'
        )
        parser.add_argument(
            '--cpu-mhz', default=1, type=int, help='Processor clock speed in MHz'
        )
        parser.add_argument(
            '--warmup-heat',
            type=int,
            default=1,
            help='Number of warmup loops to execute before benchmark',
        )
        parser.add_argument(
            '-v', '--verbose', action='store_true', help='More messages'
        )
        parser.add_argument(
            '--clean', action='store_true', help='Rebuild everything'
        )
        parser.add_argument(
            '--timeout',
            type=int,
            default=5,
            help='Timeout in seconds for the compiler and linker invocations'
        )

        # Parse the command line
        self.__raw = parser.parse_args()

    def __init__(self, rootdir):
        """Parse the raw arguments. The goal is to get enough information we
        can set up logging. We need to know the root directory, since
        ultimately relative file arguments will be based on this.

        At this stage we have no log set up.
        """
        self.__rootdir = rootdir
        self.__parse_raw()

    def logdir(self):
        """Extract the log directory, create it if necessary and make sure it is
        writable. This means dealing with relative v absolute directory
        names. Any errors here are going to go straight to the console as
        exceptions.
        """
        # Sort out absolutism
        logdir = self.__raw.logdir
        if not os.path.isabs(logdir):
            logdir = os.path.join(self.__rootdir, logdir)

        # Create the directory if necessary and maks sure we can write it.
        if not os.path.isdir(logdir):
            try:
                os.makedirs(logdir)
            except PermissionError:
                raise PermissionError(
                    f'Unable to create log directory {logdir}'
                )

        if not os.access(logdir, os.W_OK):
            raise PermissionError(
                f'Unable to write to log directory {logdir}'
            )

        return logdir

    def rootdir(self):
        """Accessor for the root directory."""
        return self.__rootdir

    def raw_args(self):
        """Accessor for the raw arguments."""
        return self.__raw

class CookedArgs:
    """The main argument class

    This class takes the raw parsed arguments and combines them into values
    useful for a program.
    """
    def __set_defaults(self, rootdir):
        """Set up default argument values. These are one of two types.

        1. Those which need more processing after initializing with default
           values.  In many cases the default is zero, None or an empty list
           or dictionary.

        2. Those which are straight copies of the argument, in which case we
           just transcribe the value.

        We need the root directory, since this is the base from which others
        are constructed.
        """
        self.__cooked = {
            # Log directory
            'logdir' : None,
            # Source directories
            'srcdirs' : {
                'root' : rootdir,
                'src' : os.path.join(rootdir, 'src'),         # Benchmarks
                'support' : os.path.join(rootdir, 'support'), # Support code
                'arch' : None,          # Architecture specific config
                'chip' : None,          # Chip specific config
                'board' : None,         # Board specific config
            },
            # Build directories
            'bindirs' : {
                'root' : None,
                'src' : None,		# Benchmarks
                'support' : None,       # Support code
                'arch' : None,          # Architecture specific config
                'chip' : None,          # Chip specific config
                'board' : None,         # Board specific config
            },
            'tools' : {
                'cc' : self.__raw.cc,
                'ld' : self.__raw.ld,
            },
            'flags' : {
                'cflags' : self.__raw.cflags.split(sep=' '),
                'ldflags' : self.__raw.ldflags.split(sep=' '),
            },
            # Patterns for constructing arguments to tools
            'patterns' : {
                'cc_define1' : self.__raw.cc_define1_pattern,
                'cc_define2' : self.__raw.cc_define2_pattern,
                'cc_incdir' : self.__raw.cc_incdir_pattern,
                'cc_input' : self.__raw.cc_input_pattern,
                'cc_output' : self.__raw.cc_output_pattern,
                'ld_input' : self.__raw.ld_input_pattern,
                'ld_output' : self.__raw.ld_output_pattern,
            },
            'libs' : {
                'user' : self.__raw.user_libs.split(sep=' '),
                'dummy' : self.__raw.dummy_libs.split(sep=' '),
            },
            'cpu_mhz' : self.__raw.cpu_mhz,
            'warmup_heat' : self.__raw.warmup_heat,
            'timeout' : self.__raw.timeout,
            'verbose' : self.__raw.verbose,
        }

    def __isreadable(self, absdir, kind):
        """Check that the supplied directory is readable. If so, return the
        directory name, otherwise exit with an error message, based on the
        value of 'kind'.
        """
        if os.access(absdir, os.R_OK):
            return absdir

        self.__log.error(
            f'ERROR: Unable to read {kind} config directory "{absdir}": '
            f'exiting'
        )
        sys.exit(1)

    def __validate_confdirs(self):
        """Set up the configuration directories.

        We don't need to set up the src and support directories, since they
        have fixed values.
        """
        srcdirs = self.__cooked['srcdirs']
        confdir = os.path.join(srcdirs['root'], 'config')

        # Config directories constructed from command line arguments and made
        # absolute.
        srcdirs['arch'] = self.__isreadable(
            os.path.join(confdir, self.__raw.arch), 'architecture'
        )
        srcdirs['chip'] = self.__isreadable(
            os.path.join(srcdirs['arch'], 'chips', self.__raw.chip), 'chip'
        )
        srcdirs['board'] = self.__isreadable(
            os.path.join(srcdirs['arch'], 'boards', self.__raw.board), 'board'
        )

    def __create_bindir(self, rel_dir):
        """Create a writable build directory. Return the name of the directory
        in the event of successs.

        The rel_dir is relative to the root build directory. We return the
        absolute directory as result. As a special case if rel_dir is None,
        then we are creating the root build directory itself.
        """
        if rel_dir:
            abs_dir = os.path.join(self.__cooked['bindirs']['root'], rel_dir)
        else:
            # Special case for root directory
            abs_dir = self.__cooked['bindirs']['root']

        if not os.path.isdir(abs_dir):
            try:
                os.makedirs(abs_dir)
            except PermissionError:
                self.__log.error(
                    f'ERROR: Unable to create build directory {abs_dir}: exiting'
                )
                sys.exit(1)

        if not os.access(abs_dir, os.W_OK):
            self.__log.error(
                f'ERROR: Unable to write to build directory {abs_dir}, exiting'
            )
            sys.exit(1)

        return abs_dir

    def __create_root_bindir(self):
        """Create the root of all build directories."""
        # The root build directory.
        root_bindir = self.__raw.builddir
        if not os.path.isabs(root_bindir):
            root_bindir = os.path.join(
                self.__cooked['srcdirs']['root'], root_bindir
            )

        # Clean
        if os.path.isdir(root_bindir) and self.__raw.clean:
            try:
                shutil.rmtree(root_bindir)
            except PermissionError:
                self.__log.error(
                    f'ERROR: Unable to clean build directory "{root_bindir}: '
                    + 'exiting'
                )
                sys.exit(1)

        # Create the root directory
        self.__cooked['bindirs']['root'] = root_bindir
        return self.__create_bindir(None)

    def __init_bindirs(self):
        """Initialize all the binary directories.

        We set these up for the src and support directories as well as the
        config directories. They follow the same hierarchy as the source
        directories, but sitting under the argument supplied to the --builddir
        argument.
        """
        # The root directory. This has its own setup, because it is affected
        # by the --clean option.
        bindirs = self.__cooked['bindirs']
        bindirs['root'] = self.__create_root_bindir()

        # Source needs a subdiretory for every benchmark
        bindirs['src'] = self.__create_bindir('src')
        for sdir in os.listdir(self.__cooked['srcdirs']['src']):
            self.__create_bindir(os.path.join('src', sdir))

        # Straight directory for support and each config category
        bindirs['support'] = self.__create_bindir('support')
        bindirs['arch'] = self.__create_bindir(
            os.path.join('config', self.__raw.arch)
        )
        bindirs['chip'] = self.__create_bindir(
            os.path.join('config', self.__raw.arch, 'chips', self.__raw.chip)
        )
        bindirs['board'] = self.__create_bindir(
            os.path.join('config', self.__raw.arch, 'boards', self.__raw.board)
        )

    def __set_params(self):
        """Determine all remaining parameters.

        The user can override default values from the command line only.  We then
        add some extra parameters constructed from the other arguments
        """
        # Linker should match compiler if it hasn't been set by now
        if not self.__cooked['tools']['ld']:
            self.__cooked['tools']['ld'] = self.__cooked['tools']['cc']

        # Add internal flags.  These are include directories for the support,
        # architecture, chip and board directories, and definitions for CPU
        # MHz and warmup cycles.
        srcdirs = self.__cooked['srcdirs']
        cflags = self.__cooked['flags']['cflags']
        pat = self.__cooked['patterns']['cc_incdir']
        for dirname in ['support', 'board', 'chip', 'arch']:
            cflags.extend(pat.format(srcdirs[dirname]).split(sep=' '))

        pat = self.__cooked['patterns']['cc_define2']
        for flag in ['cpu_mhz', 'warmup_heat']:
            cflags.extend(
                pat.format(flag.upper(), self.__cooked[flag]).split(sep=' ')
            )

    def __set_environ(self):
        """Add additional environment variables, if any"""
        if self.__raw.env:
            envlist = self.__raw.env.split(',')
            for envarg in envlist:
                var, val = envarg.split('=', 1)
                os.environ[var] = val

    def __validate_tools(self):
        """Check the compiler and linker are available."""
        for tool_kind in ['cc', 'ld']:
            tool = self.__cooked['tools'][tool_kind]
            if not shutil.which(tool):
                self.__log.error(
                    f'ERROR: Compiler {tool} not found on path: exiting'
                )
                sys.exit(1)

    def __init__(self, rawArgs, log):
        """Constructor just records the raw arguments and the log, then goes
        about cooking the arguments.

        The result is a dictionary of processed arguments. Note that this can
        be called multiple times - after the first time, it will just return
        the result from the first call.

        """
        self.__raw = rawArgs.raw_args()
        self.__log = log

        # Start with some default values
        self.__set_defaults(rawArgs.rootdir())

        # Make sure we have the config directories
        self.__validate_confdirs()

        # Create (and possibly clean) the binary directories
        self.__init_bindirs()

        # Finalize all parameters.
        self.__set_params()

        # Set the environment. Need to do this before validating the tools.
        self.__set_environ()

        # Check the tools work
        self.__validate_tools()

    def all_args(self):
        """Accessor for the list of cooked arguments."""
        return self.__cooked

    def log_raw(self):
        """
        Record the raw argument values
        """
        self.__log.debug('Supplied raw arguments')
        self.__log.debug('======================')

        for arg in vars(self.__raw):
            realarg = re.sub('_', '-', arg)
            val = getattr(self.__raw, arg)
            self.__log.debug(f'--{realarg:20}: {val}')

        self.__log.debug('')

    def log_cooked(self):
        """
        Record the cooked argument values.
        """
        self.__log.debug('Supplied cooked arguments')
        self.__log.debug('=========================')

        self.__log.debug('Source directories:')
        for sdir, val in self.__cooked['srcdirs'].items():
            self.__log.debug(f'  {sdir}: {val}')

        self.__log.debug('Build directories:')
        for bdir, val in self.__cooked['bindirs'].items():
            self.__log.debug(f'  {bdir}: {val}')

        self.__log.debug('Tools:')
        for tool, val in self.__cooked['tools'].items():
            self.__log.debug(f'  {tool}: {val}')

        self.__log.debug('Flags:')
        for flag, val in self.__cooked['flags'].items():
            self.__log.debug(f'  {flag}: {val}')

        self.__log.debug('Patterns:')
        for pat, val in self.__cooked['patterns'].items():
            self.__log.debug(f'  {pat}: {val}')

        self.__log.debug('Libraries:')
        for lib, val in self.__cooked['libs'].items():
            self.__log.debug(f'  {lib}: {val}')

        self.__log.debug('Misc:')
        for field in ['cpu_mhz', 'warmup_heat', 'timeout', 'verbose']:
            self.__log.debug(f'  {field}: {self.__cooked[field]}')

        self.__log.debug('')

    def log(self):
        """
        Convenience method to log both raw and cooked args
        """
        self.log_raw()
        self.log_cooked()
