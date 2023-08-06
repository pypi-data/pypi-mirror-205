# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2017 European Synchrotron Radiation Facility
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
"""xsocs launcher"""

from __future__ import absolute_import

import logging
logging.basicConfig()
logging.getLogger('xsocs').setLevel(logging.INFO)

import sys
from silx.utils.launcher import Launcher
from xsocs import version


def main(argv=None):
    """Main entry point of xsocs"""
    if argv is None:
        argv = sys.argv

    launcher = Launcher(prog="xsocs", version=version)
    launcher.add_command("gui",
                         module_name="xsocs._app.gui",
                         description="Open xsocs main Graphical User Interface")
    launcher.add_command("concat",
                         module_name="xsocs._app.concat",
                         description="Concatenate multiple scans into one HDF5 master file")

    # Start the GUI by default
    argv = list(argv)
    if len(argv) <= 1:
        argv.append('gui')

    sys.exit(launcher.execute(argv))


if __name__ == "__main__":
    main()
