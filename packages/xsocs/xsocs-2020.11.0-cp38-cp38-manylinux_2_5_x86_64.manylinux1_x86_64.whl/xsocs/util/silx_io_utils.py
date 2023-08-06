# coding: utf-8
# /*##########################################################################
# Copyright (C) 2016-2020 European Synchrotron Radiation Facility
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
# ############################################################################*/
""" I/O utility functions"""

__authors__ = ["P. Knobel", "V. Valls"]
__license__ = "MIT"
__date__ = "25/09/2020"

import logging

import numpy

import h5py
import h5py.h5t


logger = logging.getLogger(__name__)


def h5py_decode_value(value, encoding="utf-8", errors="surrogateescape"):
    """Keep bytes when value cannot be decoded

    :param value: bytes or array of bytes
    :param encoding str:
    :param errors str:
    """
    try:
        if numpy.isscalar(value):
            return value.decode(encoding, errors=errors)
        str_item = [b.decode(encoding, errors=errors) for b in value.flat]
        return numpy.array(str_item, dtype=object).reshape(value.shape)
    except UnicodeDecodeError:
        return value


def h5py_encode_value(value, encoding="utf-8", errors="surrogateescape"):
    """Keep string when value cannot be encoding

    :param value: string or array of strings
    :param encoding str:
    :param errors str:
    """
    try:
        if numpy.isscalar(value):
            return value.encode(encoding, errors=errors)
        bytes_item = [s.encode(encoding, errors=errors) for s in value.flat]
        return numpy.array(bytes_item, dtype=object).reshape(value.shape)
    except UnicodeEncodeError:
        return value


class H5pyDatasetReadWrapper:
    """Wrapper to handle H5T_STRING decoding on-the-fly when reading
    a dataset. Uniform behaviour for h5py 2.x and h5py 3.x

    h5py abuses H5T_STRING with ASCII character set
    to store `bytes`: dset[()] = b"..."
    Therefore an H5T_STRING with ASCII encoding is not decoded by default.
    """

    H5PY_AUTODECODE_NONASCII = int(h5py.version.version.split(".")[0]) < 3

    def __init__(self, dset, decode_ascii=False):
        """
        :param h5py.Dataset dset:
        :param bool decode_ascii:
        """
        try:
            string_info = h5py.h5t.check_string_dtype(dset.dtype)
        except AttributeError:
            # h5py < 2.10
            try:
                idx = dset.id.get_type().get_cset()
            except AttributeError:
                # Not an H5T_STRING
                encoding = None
            else:
                encoding = ["ascii", "utf-8"][idx]
        else:
            # h5py >= 2.10
            try:
                encoding = string_info.encoding
            except AttributeError:
                # Not an H5T_STRING
                encoding = None
        if encoding == "ascii" and not decode_ascii:
            encoding = None
        if encoding != "ascii" and self.H5PY_AUTODECODE_NONASCII:
            # Decoding is already done by the h5py library
            encoding = None
        if encoding == "ascii":
            # ASCII can be decoded as UTF-8
            encoding = "utf-8"
        self._encoding = encoding
        self._dset = dset

    def __getitem__(self, args):
        value = self._dset[args]
        if self._encoding:
            return h5py_decode_value(value, encoding=self._encoding)
        else:
            return value


def h5py_read_dataset(dset, index=tuple(), decode_ascii=False):
    """Read data from dataset object. UTF-8 strings will be
    decoded while ASCII strings will only be decoded when
    `decode_ascii=True`.

    :param h5py.Dataset dset:
    :param index: slicing (all by default)
    :param bool decode_ascii:
    """
    return H5pyDatasetReadWrapper(dset, decode_ascii=decode_ascii)[index]
