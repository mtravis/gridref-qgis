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
from xy_to_osgb import xy_to_osgb

uiWidget, qtBaseClass = load_ui('grid_ref_widget')

class OSGBWidget(qtBaseClass, uiWidget):
    def __init__(self, iface, plugin, parent=None):
        qtBaseClass.__init__(self)
        uiWidget.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface

        self.btnClose.setIcon(QgsApplication.getThemeIcon( "/mIconClose.png"))
        self.btnClose.setIconSize(QSize( 18, 18 ))

        self.btnPointTool.setIcon(QgsApplication.getThemeIcon( "/mActionWhatsThis.svg"))
        self.btnPointTool.setIconSize(QSize( 18, 18 ))

        #cw = iface.mainWindow().centralWidget()
        #cw.layout().addWidget(self, 2, 0)

        self.btnClose.clicked.connect(plugin.actionRun.trigger)
        self.btnPointTool.clicked.connect(self.pickPoint)
        iface.mapCanvas().xyCoordinates.connect(self.trackCoords)
        self.editCoords.returnPressed.connect(self.setCoords)

    def trackCoords(self, pt):
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

        try:
            os_ref = xy_to_osgb(pt.x(), pt.y(), precision)
        except KeyError:
            os_ref = "[out of bounds]"
        self.editCoords.setText(os_ref)

    def setCoords(self):

        try:
          x,y = osgb_to_xy(self.editCoords.text())

          r = self.iface.mapCanvas().extent()
          self.iface.mapCanvas().setExtent(
            QgsRectangle(
              x - r.width() / 2.0, y - r.height() / 2.0,
              x + r.width() / 2.0, y + r.height() / 2.0
            )
          )
        except Exception:
            QMessageBox.warning(
              self.iface.mapCanvas(),
              "Format",
              "The coordinates should be in format XX ### ###")

    def pickPoint(self):
        tool = PointTool(self.iface.mapCanvas())
        tool.setButton(self.btnPointTool)
        self.iface.mapCanvas().setMapTool(tool)
