# Make file for Embench presentations

# Copyright (C) 2020 Embecosm Limited <www.embecosm.com>
# Contributor: Jeremy Bennett <jeremy.bennett@embecosm.com>
# SPDX-License-Identifier: GPL-3.0-or-later

DIRS = generic

.PHONY: all
all:
	for d in ${DIRS} ;                   \
	do                                   \
	    cd $$d ;                         \
	    make SPHINXOPTS=-Wn slides ;     \
	    make html ;                      \
            cd .. ;                          \
	done

.PHONY: clean
clean:
	for d in ${DIRS} ;                   \
	do                                   \
	    cd $$d ;                         \
	    make clean  ;                    \
            cd .. ;                          \
	done
