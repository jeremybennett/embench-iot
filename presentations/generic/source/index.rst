
.. Template originally created by hieroglyph-quickstart on Sat Apr 30
   21:13:03 2016.

   Copyright (C) 2020 Embecosm Limited <www.embecosm.com>
   Contributor: Jeremy Bennett <jeremy.bennett@embecosm.com>
   SPDX-License-Identifier: CC-BY-SA-4.0


Embench
=======

| Speaker name
| Affiliation

.. note::

   Substitute speaker's name and affiliation

History
-------

* Use good ideas and avoid mistakes of the past
* Learn from features of widely quoted benchmarks:

.. role:: green

.. role:: red

.. list-table::
   :widths: 20 16 16 16 16 16
   :header-rows: 1
   :class: small-table

   * -
     - Linpack
     - Dhrystone
     - SPEC CPU
     - CoreMark
     - MLPerf 0.5
   * - *Year*
     - 1977
     - 1984
     - 1989
     - 2009
     - 2018
   * - *Initial target*
     - HPC
     - Sys. prog
     - Unix server
     - Embedded
     - ML server
   * - *Quality reputation*
     - :red:`Low`
     - :red:`Low`
     - :green:`High`
     - :red:`Low`
     - :red:`Low`
   * - *Free?*
     - |tick|
     - |tick|
     - |cross|
     - |tick|
     - |tick|
   * - *Easy to port*
     - |tick|
     - |tick|
     - |tick|
     - |tick|
     -
   * - *Revision freq*
     - None since 1991
     - None since 1998
     - :green:`3 years`
     - Never
     - 1 year (planned)
   * - *# programs*
     - 1
     - 1
     - :green:`10-23`
     - 1
     - :green:`7`
   * - *Organization*
     - |tick|
     - |cross|
     - |tick|
     - |tick|
     - |tick|
   * - *Summary score*
     - FLOPS
     - Speed ratio (S.R.)
     - :green:`Geomean`, S.R.
     - S.R.
     - S.R. + :green:`Std. Dev.`
   * - *Developer*
     - Academia
     - Academia
     - :green:`Acad. + Industry`
     - Academia
     - :green:`Acad. + Industry`

.. |tick| image:: tick.png
.. |cross| image:: cross.png

.. note::

   We show in green what we consider are strong characteristics

   * High reputation
   * Free
   * Easy to port
   * Frequently revised
   * Lots of programs
   * Use of geometric mean and standard deviation
   * Developed by both academia and industry

.. nextslide::

* Use good ideas and avoid mistakes of the past
* Learn from features of *less* widely quoted benchmarks:

.. list-table::
   :widths: 20 20 20 20 20
   :header-rows: 1
   :class: small-table

   * -
     - EEMBC
     - MiBench
     - BEEBS
     - TACLeBench
   * - *Year*
     - 1997
     - 2001
     - 2013
     - 2016
   * - *Initial target*
     - Embedded
     - Embedded
     - Compiler
     - Worst case execution
   * - *Quality reputation*
     - ?
     - ?
     - ?
     - ?
   * - *Free?*
     - |cross|
     - |tick|
     - |tick|
     - |tick|
   * - *Easy to port*
     - |cross|
     - |tick|
     - |tick|
     - |tick|
   * - *Revision freq*
     - Rare
     - Never
     - :green:`2 years`
     - Never
   * - *# programs*
     - 41
     - 36
     - 80
     - 52
   * - *Organization*
     - |tick|
     - |cross|
     - |cross|
     - |cross|
   * - *Summary score*
     - |cross|
     - |cross|
     - |cross|
     - |cross|
   * - *Developer*
     - Industry
     - Academia
     - :green:`Acad. + Industry`
     - Academia

7 Lessons for Embench
---------------------

1. Embench must be free
2. Embench must be easy to port and run
3. Embench must be a suite of *real* programs
4. Embench must have a supporting organization to maintain it
5. Embench must report a single summarizing score
6. Embench should summarize using geometric mean and standard deviation
7. Embench must involve both academia and industry

The Plan
--------

* **Jan - Jun 2019:** Small group created the initial version

  - Dave Patterson, Jeremy Bennett, Palmer Dabbelt, Cesare Garlati
  - mostly face-to-face

* **Jun 2019 - Feb 2020:** Wider group open to all

  - under FOSSi with mailing list and monthly conference call

* **Feb 2020:** Launch Embench 0.5 at Embedded World

* **Dec 2020:** Target date for Embench 1.0 release

Current Status
--------------

* Set of 19 benchmarks for deeply embedded computers

  - up to 64KB ROM + RAM
  - need BlueTooth LE and ECDSA programs for completeness

* Early benchmark for context switching in RISC-V

  - also needs benchmark for interrupt latency

* Initial Python build and benchmark scripts

  - tested with simulators and real hardware

  - tested with Arm Cortex M, RISC-V and ARC-em

* Need to widen to other architectures


Baseline Data
-------------

.. list-table::
   :widths: 12 22 10 8 8 8 8 8 8 8
   :header-rows: 1
   :class: baseline-table

   * - Name
     - Comments
     - Orig Source
     - CLOC
     - code size
     - data size
     - time (ms)
     - branch
     - memory
     - compute
   * - ``aha-mont64``
     - Montgomery multiplication
     - AHA
     - 162
     - 1,052
     - 0
     - 4,000
     - low
     - low
     - high
   * - ``crc32``
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
   * - ``cubic``
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
   * - ``edn``
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
   * - ``huffbench``
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
   * - ``matmult-int``
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
   * - ``minver``
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
   * - ``nbody``
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
   * - ``nettle-aes``
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
   * - ``nettle-sha256``
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
   * - ``nsichneu``
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
   * - ``picojpeg``
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
   * - ``qrduino``
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
   * - ``sglib-condensed``
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
   * - ``slre``
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
   * - ``st``
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
   * - ``statemate``
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
   * - ``ud``
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
   * - ``wikisort``
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 

