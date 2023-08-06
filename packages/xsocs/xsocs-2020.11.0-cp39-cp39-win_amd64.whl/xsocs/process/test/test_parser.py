# coding: utf-8
# /*##########################################################################
# Copyright (C) 2016 European Synchrotron Radiation Facility
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
"""
Nominal tests for the KmapSpecParser class.
"""

from __future__ import absolute_import

__authors__ = ["D. Naudet"]
__license__ = "MIT"
__date__ = "15/09/2016"

import os
import shutil
import tempfile
import unittest

from xsocs.test.utils import test_resources
from xsocs.process.merge.KmapSpecParser import KmapSpecParser


class TestParser(unittest.TestCase):
    """
    Unit tests of the parser class.
    """

    matched_files = {'test_340800_0000.edf.gz',
                     'test_341000_0000.edf.gz',
                     'test_341200_0000.edf.gz',
                     'test_341400_0000.edf.gz',
                     'test_341600_0000.edf.gz',
                     'test_341800_0000.edf.gz',
                     'test_342000_0000.edf.gz',
                     'test_342200_0000.edf.gz',
                     'test_342400_0000.edf.gz',
                     'test_342600_0000.edf.gz',
                     'test_342800_0000.edf.gz',
                     'test_343000_0000.edf.gz',
                     'test_343200_0000.edf.gz',
                     'test_343400_0000.edf.gz',
                     'test_343600_0000.edf.gz',
                     'test_343800_0000.edf.gz',
                     'test_344000_0000.edf.gz',
                     'test_344200_0000.edf.gz'}

    def setUp(self):
        self._tmpTestDir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmpTestDir)
        self._tmpTestDir = None

    def test_nominal(self):
        """
        """
        spec_resources = test_resources.getdir('spec.zip')
        spec_f = [f for f in spec_resources if f.endswith('spec/test.spec')][0]
        img_dir = os.path.dirname(
            [f for f in spec_resources if f.endswith('img/test_340800_0000.edf.gz')][0])

        spec_h5 = os.path.join(self._tmpTestDir, 'spec.h5')

        self.assertFalse(os.path.isfile(spec_h5))

        parser = KmapSpecParser(spec_f,
                                spec_h5,
                                img_dir=img_dir,
                                version=0)

        parser.parse()

        self.assertEqual(parser.status, parser.DONE)
        self.assertTrue(os.path.isfile(spec_h5))

        results = parser.results

        matched = results.matched

        self.assertEqual(len(matched), 18)

        matched_set = set([os.path.basename(matched_f['image'])
                           for matched_f in matched.values()])

        self.assertEqual(matched_set, self.matched_files)


def suite():
    loader = unittest.defaultTestLoader
    test_suite = unittest.TestSuite()
    test_suite.addTests(loader.loadTestsFromTestCase(TestParser))
    return test_suite


if __name__ == '__main__':
    unittest.main(defaultTest="suite")
