# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GridRef
                                 A QGIS plugin
 This plugin takes the coords of the map cnavas and translates to an Ordnance
 Survey Grid Reference e.g. SX4855
                              -------------------
        begin                : 2014-08-21
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Matt Travis
        email                : matt.travis1@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.gui import *
from qgis.core import *

from grid_ref_widget import OSGBWidget
import os.path
from xy_to_osgb import xy_to_osgb, osgb_to_xy


class GridRef:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'GridRef_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&GridRef')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'GridRef')
        self.toolbar.setObjectName(u'GridRef')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('GridRef', message)

    def add_action(self,
                   icon_path,
                   text,
                   callback,
                   enabled_flag=True,
                   add_to_menu=True,
                   add_to_toolbar=True,
                   status_tip=None,
                   whats_this=None,
                   shortcut=None,
                   checkable=None,
                   parent=None):
        """Add a toolbar icon to the InaSAFE toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if shortcut:
            action.setShortcut(shortcut)

        if checkable:
            action.setCheckable(True)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/GridRef/icon.png'
        self.actionRun = self.add_action(
            icon_path,
            text=self.tr(u'Grid Ref'),
            callback=self.run,
            checkable=True,
            parent=self.iface.mainWindow())

        self.add_action(
            icon_path,
            text=self.tr(u'Grid Ref Keyboard Shortcut'),
            callback=self.run_keyboard,
            add_to_menu=True,
            add_to_toolbar=False,
            parent=self.iface.mainWindow())

        precision_field = QSpinBox()
        precision_field.setToolTip("Coordinates precision")
        precision_field.setRange(2, 4)
        self.toolbar.addWidget(precision_field)

        self.widget = OSGBWidget(self.iface, self, precision_field)
        self.iface.addDockWidget(Qt.BottomDockWidgetArea, self.widget)
        self.widget.hide()

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&GridRef'),
                action)
            self.iface.removeToolBarIcon(action)

        self.iface.removeDockWidget(self.widget)

        del self.actionRun
        del self.widget

    def run(self):
        """Run method that performs all the real work"""
        self.widget.setVisible(not self.widget.isVisible())

    def run_keyboard(self):
        """ This is the function called by the action assigned to a
        keyboard shortcut.  It will determine the position of the mouse
        cursor on the canvas, determine the OS GB grid reference and
        copy the result to the clipboard.

        If the coordinate reference system is not 27700 or the coord is
        out of the expected range then a sensible error message will be
        copied to the clipboard. """

        os_ref = xy_to_osgb(self.x, self.y)
        # QMessageBox.information(None, "Info", "Grid Ref: " + os_ref)
        QApplication.clipboard().setText(os_ref)
        self.iface.messageBar().pushMessage(
            "Grid reference copied to clipboard.", duration=1)
