# -*- coding: utf-8 -*-

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

from qgis.gui import QgsMapTool
from qgis.core import QgsRectangle
from PyQt4.QtGui import QMessageBox, QApplication

from xy_to_osgb import xy_to_osgb
from grid_ref_utils import reproject_point_to_4326

class PointTool(QgsMapTool):
    def __init__(self, canvas, precision):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.precision = precision

    def canvasReleaseEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        bbox = QgsRectangle(4999.99,4999.69,660000.06,1225000.12)

        if bbox.contains(point):
            os_ref = xy_to_osgb(point.x(), point.y(), self.precision)
            point_4326 = reproject_point_to_4326(self.canvas, point)
            QApplication.clipboard().setText(os_ref)
            msg = "Grid Ref: {}\n\nLong,Lat: {:.2f}, {:.2f}\n\nCopied to clipboard".format(os_ref, point_4326.x(), point_4326.y())
            QMessageBox.information(None, "OS Grid Reference", msg)
        else:
            QMessageBox.information(None, "OS Grid Reference", "Point out of bounds")
