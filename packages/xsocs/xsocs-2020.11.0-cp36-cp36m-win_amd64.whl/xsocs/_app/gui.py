# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2018 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/
"""xsocs main graphical user interface"""

from __future__ import absolute_import

import argparse
from multiprocessing import cpu_count

from ..gui import xsocs_main
from .. import config


def main(argv):
    """Starts main graphical user interface

    :param argv: Command line arguments
    :return: exit code
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'project_file',
        nargs=argparse.OPTIONAL,
        help='xsocs project file to open')
    parser.add_argument(
        '--numcores',
        nargs='?',
        type=int,
        default=cpu_count(),
        help='Max number of processes to use (default: %d)' % cpu_count())
    parser.add_argument(
        '--no-3d',
        action='store_true',
        help='Do not use OpenGL-based 3D visualization')

    options = parser.parse_args(argv[1:])

    if options.numcores <= 0:
        raise ValueError(
            'Number of processes to use must be strictly positive')
    config.DEFAULT_PROCESS_NUMBER = options.numcores

    config.USE_OPENGL = not options.no_3d

    if options.project_file:
        xsocs_main(projectH5File=options.project_file)
    else:
        xsocs_main()

    return 1
