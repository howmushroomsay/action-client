# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\project\python\action-sys\admin\window\login\resource\ui\SignUPWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(420, 500)
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(70, 50, 288, 360))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.signUpBtn = PrimaryPushButton(self.layoutWidget)
        self.signUpBtn.setObjectName("signUpBtn")
        self.gridLayout.addWidget(self.signUpBtn, 1, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.BodyLabel_8 = BodyLabel(self.layoutWidget)
        self.BodyLabel_8.setMaximumSize(QtCore.QSize(80, 16777215))
        self.BodyLabel_8.setObjectName("BodyLabel_8")
        self.horizontalLayout_8.addWidget(self.BodyLabel_8)
        self.nameLineEdit = LineEdit(self.layoutWidget)
        self.nameLineEdit.setMinimumSize(QtCore.QSize(200, 33))
        self.nameLineEdit.setMaximumSize(QtCore.QSize(200, 33))
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.horizontalLayout_8.addWidget(self.nameLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.BodyLabel_7 = BodyLabel(self.layoutWidget)
        self.BodyLabel_7.setMaximumSize(QtCore.QSize(80, 16777215))
        self.BodyLabel_7.setObjectName("BodyLabel_7")
        self.horizontalLayout_7.addWidget(self.BodyLabel_7)
        self.sexComboBox = ComboBox(self.layoutWidget)
        self.sexComboBox.setMinimumSize(QtCore.QSize(200, 0))
        self.sexComboBox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.sexComboBox.setText("")
        self.sexComboBox.setObjectName("sexComboBox")
        self.horizontalLayout_7.addWidget(self.sexComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.BodyLabel_2 = BodyLabel(self.layoutWidget)
        self.BodyLabel_2.setMaximumSize(QtCore.QSize(80, 16777215))
        self.BodyLabel_2.setObjectName("BodyLabel_2")
        self.horizontalLayout_2.addWidget(self.BodyLabel_2)
        self.usernameLineEdit = LineEdit(self.layoutWidget)
        self.usernameLineEdit.setMinimumSize(QtCore.QSize(200, 33))
        self.usernameLineEdit.setMaximumSize(QtCore.QSize(200, 33))
        self.usernameLineEdit.setObjectName("usernameLineEdit")
        self.horizontalLayout_2.addWidget(self.usernameLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.BodyLabel_3 = BodyLabel(self.layoutWidget)
        self.BodyLabel_3.setMaximumSize(QtCore.QSize(80, 16777215))
        self.BodyLabel_3.setObjectName("BodyLabel_3")
        self.horizontalLayout_3.addWidget(self.BodyLabel_3)
        self.passwordLineEdit = LineEdit(self.layoutWidget)
        self.passwordLineEdit.setMaximumSize(QtCore.QSize(200, 33))
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLineEdit.setPlaceholderText("")
        self.passwordLineEdit.setClearButtonEnabled(True)
        self.passwordLineEdit.setObjectName("passwordLineEdit")
        self.horizontalLayout_3.addWidget(self.passwordLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.BodyLabel_6 = BodyLabel(self.layoutWidget)
        self.BodyLabel_6.setMaximumSize(QtCore.QSize(80, 16777215))
        self.BodyLabel_6.setObjectName("BodyLabel_6")
        self.horizontalLayout_6.addWidget(self.BodyLabel_6)
        self.passwordLineEdit_2 = LineEdit(self.layoutWidget)
        self.passwordLineEdit_2.setMaximumSize(QtCore.QSize(200, 33))
        self.passwordLineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordLineEdit_2.setPlaceholderText("")
        self.passwordLineEdit_2.setClearButtonEnabled(True)
        self.passwordLineEdit_2.setObjectName("passwordLineEdit_2")
        self.horizontalLayout_6.addWidget(self.passwordLineEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.BodyLabel_4 = BodyLabel(self.layoutWidget)
        self.BodyLabel_4.setMaximumSize(QtCore.QSize(80, 16777215))
        self.BodyLabel_4.setObjectName("BodyLabel_4")
        self.horizontalLayout_4.addWidget(self.BodyLabel_4)
        self.phoneLineEdit = LineEdit(self.layoutWidget)
        self.phoneLineEdit.setMinimumSize(QtCore.QSize(200, 33))
        self.phoneLineEdit.setMaximumSize(QtCore.QSize(200, 33))
        self.phoneLineEdit.setObjectName("phoneLineEdit")
        self.horizontalLayout_4.addWidget(self.phoneLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.BodyLabel_5 = BodyLabel(self.layoutWidget)
        self.BodyLabel_5.setMaximumSize(QtCore.QSize(80, 16777215))
        self.BodyLabel_5.setObjectName("BodyLabel_5")
        self.horizontalLayout_5.addWidget(self.BodyLabel_5)
        self.idNumberLineEdit = LineEdit(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.idNumberLineEdit.sizePolicy().hasHeightForWidth())
        self.idNumberLineEdit.setSizePolicy(sizePolicy)
        self.idNumberLineEdit.setMinimumSize(QtCore.QSize(200, 33))
        self.idNumberLineEdit.setMaximumSize(QtCore.QSize(200, 33))
        self.idNumberLineEdit.setObjectName("idNumberLineEdit")
        self.horizontalLayout_5.addWidget(self.idNumberLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.backBtn = PrimaryPushButton(self.layoutWidget)
        self.backBtn.setObjectName("backBtn")
        self.gridLayout.addWidget(self.backBtn, 2, 0, 1, 1)
        self.BodyLabel = BodyLabel(Form)
        self.BodyLabel.setGeometry(QtCore.QRect(0, 0, 441, 491))
        self.BodyLabel.setText("")
        self.BodyLabel.setPixmap(QtGui.QPixmap(":/images/background.jpg"))
        self.BodyLabel.setObjectName("BodyLabel")
        self.BodyLabel.raise_()
        self.layoutWidget.raise_()

        self.translateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def translateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.signUpBtn.setText(_translate("Form", "注册"))
        self.BodyLabel_8.setText(_translate("Form", "昵称："))
        self.BodyLabel_7.setText(_translate("Form", "性别："))
        self.BodyLabel_2.setText(_translate("Form", "用户名："))
        self.BodyLabel_3.setText(_translate("Form", "密码："))
        self.BodyLabel_6.setText(_translate("Form", "确认密码："))
        self.BodyLabel_4.setText(_translate("Form", "电话："))
        self.BodyLabel_5.setText(_translate("Form", "身份证："))
        self.backBtn.setText(_translate("Form", "返回"))
from qfluentwidgets import BodyLabel, ComboBox, LineEdit, PrimaryPushButton
import resource_rc
