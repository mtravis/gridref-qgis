# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GridRef
                                 A QGIS plugin
 This plugin takes the coords of the map cnavas and translates to an Ordnance Survey Grid Reference e.g. SX4855
                             -------------------
        begin                : 2014-08-21
        copyright            : (C) 2014 by Matt Travis
        email                : matt.travis1@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load GridRef class from file GridRef.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .grid_ref import GridRef
    return GridRef(iface)
