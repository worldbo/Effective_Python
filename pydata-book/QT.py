# -*- coding: utf-8 -*-
# author__ = 'world_bo@163.com'
# Form implementation generated from reading ui file 'f:\python\world_bo.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


class Ui_World_bo(object):
    def setupUi(self, World_bo):
        World_bo.setObjectName("World_bo")
        World_bo.resize(566, 441)
        self.buttonBox = QtWidgets.QDialogButtonBox(World_bo)
        self.buttonBox.setGeometry(QtCore.QRect(140, 340, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.checkBox = QtWidgets.QCheckBox(World_bo)
        self.checkBox.setGeometry(QtCore.QRect(130, 90, 71, 16))
        self.checkBox.setObjectName("checkBox")

        self.retranslateUi(World_bo)
        self.buttonBox.accepted.connect(World_bo.accept)
        self.buttonBox.rejected.connect(World_bo.reject)
        QtCore.QMetaObject.connectSlotsByName(World_bo)

    def retranslateUi(self, World_bo):
        _translate = QtCore.QCoreApplication.translate
        World_bo.setWindowTitle(_translate("World_bo", "Wolrd_bo"))
        self.checkBox.setText(_translate("World_bo", "选择日期"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    md = Ui_World_bo()
    md.show()
    sys.exit(app.exec_())
