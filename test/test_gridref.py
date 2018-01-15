# coding=utf-8
"""Tests XY to OSGB functionality.


.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
__author__ = 'tom.chadwin@nnpa.org.uk'
__date__ = '15/01/2018'
__copyright__ = ('Copyright 2018, Tom Chadwin')

import os
import unittest

from utilities import get_qgis_app

from xy_to_osgb import xy_to_osgb
QGIS_APP = get_qgis_app()


class QGISTest(unittest.TestCase):
    """Test the QGIS Environment"""

    def test_xy_to_osgb(self):
        """Given XY returns correct OSGB coordinates"""

        osgb_gridref = xy_to_osgb(393618.933445, 564351.935939)
        expected = "NY9364"
        self.assertEqual(osgb_gridref, expected)

if __name__ == '__main__':
    unittest.main()
