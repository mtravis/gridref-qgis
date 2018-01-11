# -*- coding: utf-8 -*-

# Grid ref widget
# Copyright (C) 2016 Peter Petrik for Lutra Consulting
# zilolv at gmail dot com
# Lutra Consulting
# 23 Chestnut Close
# Burgess Hill
# West Sussex
# RH15 8HN

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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.gui import *
from qgis.core import *
import resources_rc
import math
from point_tool import PointTool
from grid_ref_utils import load_ui
from xy_to_osgb import xy_to_osgb, osgb_to_xy
from grid_ref_utils import (
    reproject_point_to_4326,
    reproject_point_from_4326,
    GridRefException,
    centre_on_point,
    point_from_longlat_text,
    gen_marker
)

uiWidget, qtBaseClass = load_ui('grid_ref_widget')

class OSGBWidget(qtBaseClass, uiWidget):
    def __init__(self, iface, plugin, precision_field, parent=None):
        qtBaseClass.__init__(self)
        uiWidget.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.marker = None
        self.precision_field = precision_field
        self.tool = None

        self._set_icons()
        self._add_validators()
        self._connect_signals(plugin)

    def _set_icons(self):
        self.btnClose.setIcon(QgsApplication.getThemeIcon( "/mIconClose.png"))
        self.btnClose.setIconSize(QSize( 18, 18 ))

        self.btnPointTool.setIcon(QgsApplication.getThemeIcon( "/mActionWhatsThis.svg"))
        self.btnPointTool.setIconSize(QSize( 18, 18 ))

    def _add_validators(self):
        re = QRegExp(r'''^(\s*[a-zA-Z]{2}\s*\d{1,4}\s*\d{1,4}\s*|\[out of bounds\])$''')
        self.editCoords.setValidator(QRegExpValidator(re, self))

        re = QRegExp("^\s*[-+]?[0-9]*\.?[0-9]+\s*\,\s*[-+]?[0-9]*\.?[0-9]+\s*$")
        self.editLongLat.setValidator(QRegExpValidator(re, self))

    def _connect_signals(self, plugin):
        self.btnClose.clicked.connect(plugin.actionRun.trigger)
        self.btnPointTool.clicked.connect(self.pickPoint)
        self.iface.mapCanvas().xyCoordinates.connect(self.trackCoords)
        self.editCoords.returnPressed.connect(self.setCoords)
        self.editLongLat.returnPressed.connect(self.setLongLat)
        self.precision_field.valueChanged.connect(self.change_precision)

    def _setEditCooordsOnMouseMove(self, pt):
        # dynamically determine the most sensible precision for the given scale
        log_scale = math.log(self.iface.mapCanvas().scale()) / math.log(10)
        if log_scale >= 6:
          precision = 1000
        elif log_scale >= 5:
          precision = 100
        elif log_scale >= 4:
          precision = 10
        else:
          precision = 1

        if self.tool:
            precision = self.tool.precision

        try:
            os_ref = xy_to_osgb(pt.x(), pt.y(), precision)
        except GridRefException:
            os_ref = "[out of bounds]"
        self.editCoords.setText(os_ref)

    def _setEditLongLatOnMouseMove(self, pt):
        point_4326 = reproject_point_to_4326(self.iface.mapCanvas(), pt)
        msg = "{:.2f}, {:.2f}".format(point_4326.x(), point_4326.y())
        self.editLongLat.setText(msg)

    def _add_marker(self, point):
        if self.marker:
            self._remove_marker()
        self.marker = gen_marker(self.iface.mapCanvas(), point)

    def _remove_marker(self):
        if self.marker:
            self.iface.mapCanvas().scene().removeItem(self.marker)
            self.marker = None

    def change_precision(self):
        if self.tool:
            self.tool.precision = pow(10, 5 - self.precision_field.value())

    def trackCoords(self, pt):
        self._setEditCooordsOnMouseMove(pt)
        self._setEditLongLatOnMouseMove(pt)
        self._remove_marker()

    def setCoords(self):
        try:
          x,y = osgb_to_xy(self.editCoords.text())
          point27700 = QgsPoint(x,y)
          centre_on_point(self.iface.mapCanvas(), point27700)
          self._add_marker(point27700)
        except GridRefException:
            QMessageBox.warning(
              self.iface.mapCanvas(),
              "Format",
              "The coordinates should be in format XX ### ###")

    def setLongLat(self):
        try:
          longlat = self.editLongLat.text()
          point4326 = point_from_longlat_text(longlat)
          point27700 = reproject_point_from_4326(self.iface.mapCanvas(), point4326)
          centre_on_point(self.iface.mapCanvas(), point27700)
          self._add_marker(point27700)
        except GridRefException:
            QMessageBox.warning(
              self.iface.mapCanvas(),
              "Format",
              "The coordinates should be in format ##.##, ##.##")

    def pickPoint(self):
        self.tool = PointTool(self.iface.mapCanvas(), pow(10,self.precision_field.value()))
        self.change_precision()
        self.tool.setButton(self.btnPointTool)
        self.iface.mapCanvas().setMapTool(self.tool)
