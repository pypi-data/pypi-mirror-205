# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2015-2016 European Synchrotron Radiation Facility
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
"""This module miscellaneous convenient functions"""

from __future__ import absolute_import, division

__authors__ = ["D. Naudet"]
__license__ = "MIT"
__date__ = "01/03/2016"


import sys
import warnings
import numpy


# Python 2/3 compatibility
if sys.version_info[0] >= 3:
    text_type = str
else:
    text_type = unicode


def bin_centers_to_range_step(centers):
    """Convert histogram bin centers (as stored in hdf5) to bin range and step

    This assumes sorted bins of the same size.

    :param numpy.ndarray centers: 1D array of bin centers
    :return: Bin edges min, max, step
    :rtype: List[float]
    """
    centers = numpy.array(centers, copy=False)
    nbins = centers.shape[0] - 1
    min_, max_ = numpy.min(centers), numpy.max(centers)
    step = (max_ - min_) / nbins
    return min_ - step/2., max_ + step/2., step


_SQRT_2_PI = numpy.sqrt(2 * numpy.pi)


def gaussian(x, area, center, sigma):
    """Returns (a / (sqrt(2 * pi) * s)) * exp(- 0.5 * ((x - c) / s)^2)

    :param numpy.ndarray x: values for which the gaussian must be computed
    :param float area: area under curve ( amplitude * s * sqrt(2 * pi) )
    :param float center:
    :param float sigma:
    :rtype: numpy.ndarray
    """
    return ((area / (_SQRT_2_PI * sigma)) *
            numpy.exp(-0.5 * ((x - center) / sigma) ** 2))


def project(data, hits=None):
    """Sum data along each axis

    :param numpy.ndarray data: 3D histogram
    :param Union[numpy.ndarray,None] hits:
        Number of bin count of the histogram or None to ignore
    :return: Projections on each axis of the dataset
    :rtype: List[numpy.ndarray]
    """
    if hits is not None:
        tmp = hits.sum(2)
        hits0_sum = tmp.sum(1)
        hits1_sum = tmp.sum(0)
        hits2_sum = hits.sum((0, 1))
    else:
        hits0_sum = hits1_sum = hits2_sum = 1

    tmp = data.sum(2)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', RuntimeWarning)
        dim0_sum = tmp.sum(1) / hits0_sum
        dim1_sum = tmp.sum(0) / hits1_sum
        dim2_sum = data.sum((0, 1)) / hits2_sum
    # to get smth that resembles the sum rather than the mean,
    # one can here multiply element wise by the summed 2D area

    if hits is not None:
        dim0_sum[hits0_sum <= 0] = 0
        dim1_sum[hits1_sum <= 0] = 0
        dim2_sum[hits2_sum <= 0] = 0

    return dim0_sum, dim1_sum, dim2_sum
