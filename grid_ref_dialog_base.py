# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'grid_ref_dialog_base.ui'
#
# Created: Fri Aug 22 07:16:24 2014
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_OSGBGridRef(object):
    def setupUi(self, OSGBGridRef):
        OSGBGridRef.setObjectName(_fromUtf8("OSGBGridRef"))
        OSGBGridRef.resize(184, 69)
        self.pushButton = QtGui.QPushButton(OSGBGridRef)
        self.pushButton.setGeometry(QtCore.QRect(50, 20, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))

        self.retranslateUi(OSGBGridRef)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("pressed()")), OSGBGridRef.accept)
        QtCore.QMetaObject.connectSlotsByName(OSGBGridRef)

    def retranslateUi(self, OSGBGridRef):
        OSGBGridRef.setWindowTitle(QtGui.QApplication.translate("OSGBGridRef", "OSGB Grid Ref", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("OSGBGridRef", "Get OS Ref", None, QtGui.QApplication.UnicodeUTF8))

