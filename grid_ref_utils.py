# -*- coding: utf-8 -*-

# grid_ref_utils - utilities for grid_ref QGIS plugin
# Copyright (C) 2016 Peter Petrik for Lutra Consulting

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA.

from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os
from qgis.gui import *
from qgis.core import *


class GridRefException(Exception):
    pass


def reproject_point_to_4326(canvas, point):
    crsSrc = canvas.mapSettings().destinationCrs()  # 27700
    crsDest = QgsCoordinateReferenceSystem(4326)
    xform = QgsCoordinateTransform(crsSrc, crsDest)
    return xform.transform(point)


def reproject_point_from_4326(canvas, point):
    crsSrc = QgsCoordinateReferenceSystem(4326)
    crsDest = canvas.mapSettings().destinationCrs()  # 27700
    xform = QgsCoordinateTransform(crsSrc, crsDest)
    return xform.transform(point)


def gen_marker(canvas, point):
    marker = QgsVertexMarker(canvas)
    marker.setColor(QColor(255, 0, 0))
    marker.setPenWidth(2)
    marker.setCenter(point)
    return marker


def centre_on_point(canvas, point):
    rect = QgsRectangle(point, point)
    canvas.setExtent(rect)
    canvas.refresh()


def point_from_longlat_text(longlat):
    longlat = longlat.split(",")
    if len(longlat) != 2:
        raise GridRefException()

    longitude = float(longlat[0].strip())  # regex validator ensures it passes
    latitude = float(longlat[1].strip())  # regex validator ensures it passes
    if longitude > 180 or longitude < -180:
        raise GridRefException()
    if latitude > 90 or latitude < -90:
        raise GridRefException()
    return QgsPoint(longitude, latitude)


def load_ui(name):
    ui_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           'ui',
                           name + '.ui')
    return uic.loadUiType(ui_file)
