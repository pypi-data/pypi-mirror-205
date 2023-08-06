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
"""Useful functions for HDF5 files"""

import numpy
import h5py
from ..util import text_type


def str_to_h5_utf8(text):
    """Convert text to the appropriate unicode type

    :param Union[str,List[str]] text:
    :return: Input converted to a format appropriate for h5py
    :rtype: numpy.ndarray
    """
    return numpy.array(text, dtype=h5py.special_dtype(vlen=text_type))


def find_NX_class(group, nx_class):
    """Yield name of items in group of nx_class NX_class

    :param h5py.Group group:
    :param str nx_class:
    :rtype: Iterable[str]
    """
    for key, item in group.items():
        cls = item.attrs.get('NX_class', '')
        if hasattr(cls, 'decode'):
            cls = cls.decode()
        if cls == nx_class:
            yield key
