# -*- coding: utf-8 -*-
"""QGIS unit tests for QgsPalLabeling: label rendering to screen canvas

From build dir: ctest -R PyQgsPalLabelingCanvas -V
Set the following env variables when manually running tests:
  PAL_SUITE to run specific tests (define in __main__)
  PAL_VERBOSE to output individual test summary
  PAL_CONTROL_IMAGE to trigger building of new control images
  PAL_REPORT to open any failed image check reports in web browser

.. note:: This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""

__author__ = 'Larry Shaffer'
__date__ = '07/09/2013'
__copyright__ = 'Copyright 2013, The QGIS Project'
# This will get replaced with a git SHA1 when you do a git archive
__revision__ = '$Format:%H$'

import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *

from utilities import (
    unittest,
    expectedFailure,
)

from test_qgspallabeling_base import TestQgsPalLabeling, runSuite
from test_qgspallabeling_tests import (
    TestPointBase,
    suiteTests
)


class TestCanvasBase(TestQgsPalLabeling):

    layer = None
    """:type: QgsVectorLayer"""

    @classmethod
    def setUpClass(cls):
        if not cls._BaseSetup:
            TestQgsPalLabeling.setUpClass()

    @classmethod
    def tearDownClass(cls):
        TestQgsPalLabeling.tearDownClass()
        cls.removeMapLayer(cls.layer)
        cls.layer = None

    def setUp(self):
        """Run before each test."""
        super(TestCanvasBase, self).setUp()
        self._Mismatches.clear()

    def checkTest(self, **kwargs):
        self.lyr.writeToLayer(self.layer)
        self.saveControlImage()
        self.assertTrue(*self.renderCheck())


class TestCanvasBasePoint(TestCanvasBase):

    @classmethod
    def setUpClass(cls):
        TestCanvasBase.setUpClass()
        cls.layer = TestQgsPalLabeling.loadFeatureLayer('point')


class TestCanvasPoint(TestCanvasBasePoint, TestPointBase):

    def setUp(self):
        """Run before each test."""
        super(TestCanvasPoint, self).setUp()
        self.configTest('pal_canvas', 'sp')
    

if __name__ == '__main__':
    # NOTE: unless PAL_SUITE env var is set all test class methods will be run
    # SEE: test_qgspallabeling_tests.suiteTests() to define suite
    suite = (
        ['TestCanvasPoint.' + t for t in suiteTests()['sp_suite']]
    )
    res = runSuite(sys.modules[__name__], suite)
    sys.exit(not res.wasSuccessful())
