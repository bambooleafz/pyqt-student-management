# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_About(object):
    def setupUi(self, Dialog_About):
        Dialog_About.setObjectName("Dialog_About")
        Dialog_About.resize(330, 182)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog_About.sizePolicy().hasHeightForWidth())
        Dialog_About.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(11)
        Dialog_About.setFont(font)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog_About)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(Dialog_About)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.retranslateUi(Dialog_About)
        QtCore.QMetaObject.connectSlotsByName(Dialog_About)

    def retranslateUi(self, Dialog_About):
        _translate = QtCore.QCoreApplication.translate
        Dialog_About.setWindowTitle(_translate("Dialog_About", "关于"))
        self.label.setText(_translate("Dialog_About", "<html><head/><body><p>学生管理系统，基于：</p><p>------------------</p><p>Python 3.7.2</p><p>PyQt5</p><p>------------------</p><p>Icelake Works, 2022.10</p></body></html>"))
