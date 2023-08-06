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
"""This module contains library wide configuration.
"""

__authors__ = ["T. Vincent"]
__license__ = "MIT"
__date__ = "04/09/2018"


from multiprocessing import cpu_count


class Config(object):
    """
    Class containing shared global configuration for the silx library.
    """

    DEFAULT_PROCESS_NUMBER = cpu_count()
    """Default max number of processes to use (Use number of core by default)
    
    This value must be strictly positive.
    """

    USE_OPENGL = True
    """True to use OpenGL widgets (default), False to disable."""

    DEFAULT_HDF5_COMPRESSION = 'gzip'
    """Default HDF5 dataset compression scheme"""
