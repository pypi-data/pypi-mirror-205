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

from __future__ import absolute_import

__authors__ = ["D. Naudet"]
__license__ = "MIT"
__date__ = "15/09/2016"


from collections import namedtuple

from silx.gui import qt as Qt

from silx.gui.widgets.RangeSlider import RangeSlider
from ..widgets.Input import StyledLineEdit


RangeSliderState = namedtuple('RangeSliderState', ['left', 'right',
                                                   'leftIndex', 'rightIndex'])


class RoiAxisWidget(Qt.QWidget):
    """
    Widget with a double slider and two line edit displaying the slider range.

    :param label: text displayed above the slider.
    :param kwargs:
    """

    sigSliderMoved = Qt.Signal(object)
    """Signal triggered when the slider values has changed."""

    def __init__(self, label=None, **kwargs):
        super(RoiAxisWidget, self).__init__(**kwargs)

        layout = Qt.QGridLayout(self)
        self.__label = Qt.QLabel()
        self.__label.setFrameStyle(Qt.QFrame.NoFrame | Qt.QFrame.Plain)
        self.__label.setText(label)
        self.__slider = RangeSlider()

        self.__leftEdit = StyledLineEdit(nChar=7)
        leftEditValidator = Qt.QDoubleValidator(self.__leftEdit)
        leftEditValidator.setDecimals(6)
        self.__leftEdit.setValidator(leftEditValidator)
        self.__leftEdit.editingFinished.connect(self.__leftEditingFinished)

        self.__rightEdit = StyledLineEdit(nChar=7)
        rightEditValidator = Qt.QDoubleValidator(self.__rightEdit)
        rightEditValidator.setDecimals(6)
        self.__rightEdit.setValidator(rightEditValidator)
        self.__rightEdit.editingFinished.connect(self.__rightEditingFinished)

        layout.addWidget(self.__label, 0, 0)
        layout.addWidget(self.__slider, 0, 1, 1, 2)
        layout.addWidget(self.__leftEdit, 1, 1)
        layout.addWidget(self.__rightEdit, 1, 2)

        layout.setColumnStretch(3, 1)

        self.__slider.sigValueChanged.connect(self.__sliderValueChanged)

    def slider(self):
        """The RangeSlider instance of this widget.

        :rtype: RangeSlider
        """
        return self.__slider

    def text(self):
        """Returns label text

        :rtype: str
        """
        return self.__label.text()

    def setText(self, text):
        """Set the text of the label

        :param str text:
        """
        self.__label.setText(text)

    def getSliderState(self):
        """Returns current slider state

        :rtype: RangeSliderState
        """
        firstValue, secondValue = self.slider().getValues()
        firstPos, secondPos = self.slider().getPositions()
        state = RangeSliderState(left=firstValue,
                                 right=secondValue,
                                 leftIndex=firstPos,
                                 rightIndex=secondPos)
        return state

    def __leftEditingFinished(self):
        """Handle left line edit editing finished"""
        self.__slider.setFirstValue(float(self.__leftEdit.text()))

    def __rightEditingFinished(self):
        """Handle right line edit editing finished"""
        self.__slider.setSecondValue(float(self.__rightEdit.text()))

    def __sliderValueChanged(self, first, second):
        """Slot triggered when one of the slider is moved.

        Updates the line edits and emits sigSliderMoved.

        :param float first:
        :param float second:
        """
        self.__leftEdit.setText('{0:6g}'.format(first))
        self.__rightEdit.setText('{0:6g}'.format(second))
        self.sigSliderMoved.emit(self.getSliderState())
