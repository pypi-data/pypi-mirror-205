#!/usr/bin/python
# coding: utf8
# /*##########################################################################
#
# Copyright (c) 2015-2017 European Synchrotron Radiation Facility
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

from __future__ import absolute_import

__authors__ = ["D. Naudet"]
__date__ = "01/01/2017"
__license__ = "MIT"


import numpy

from ....util import gaussian


class Plotter(object):
    """Base class for fit result plotting"""

    def plotFit(self, plot, x, params, background):
        """Update a plot to display fit/COM results

        :param plot: PlotWidget to update
        :param numpy.ndarray x: X values
        :param List[float] params: Parameters of the fit/COM
        :param Union[None,numpy.ndarray] background:
           The background estimation or None if no background
        """
        raise NotImplementedError('Not implemented')

    def getPlotTitle(self):
        """Returns the title to use for the plot

        :rtype: str
        """
        raise NotImplementedError('Not implemented')


class GaussianPlotter(Plotter):
    """Plot gaussian fit results"""

    def plotFit(self, plot, x, params, background):
        for peakName, peak in params.items():
            height = peak.get('Area')
            position = peak.get('Center')
            width = peak.get('Sigma')

            gaussian_params = [height, position, width]

            if numpy.all(numpy.isfinite(gaussian_params)):
                fitted = gaussian(x, *gaussian_params)
                if background is not None:
                    fitted += background
                plot.addCurve(x,
                              fitted,
                              legend='{0}'.format(peakName),
                              color='red')

    def getPlotTitle(self):
        return 'Gaussian'


class CentroidPlotter(Plotter):
    """Plot center-of-mass/Max results"""

    def plotFit(self, plot, x, params, background):
        for peakName, peak in params.items():
            center = peak.get('COM')
            xmax = peak.get('Pos_max')

            if numpy.isfinite(center):
                plot.addXMarker(center, legend='center of mass', text="com")
                plot.addXMarker(xmax,
                                legend='maximum position',
                                text="max",
                                color="gray")

    def getPlotTitle(self):
        return 'Center Of Mass'
