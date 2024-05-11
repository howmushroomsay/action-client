# coding:utf-8
import json

import requests
import yaml
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy,
                             QSpacerItem, QAbstractItemView, QTableWidgetItem,
                             )
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (ScrollArea, BodyLabel, LineEdit,
                            SwitchButton, TableWidget, ComboBox, Dialog, PrimaryToolButton, )


class UserManagerInterface(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)
        # 获取数据
        # self.setFixedHeight(350)
        self.__initWidget()

        self.initFun()
        self.initConfig()

        self.currentPage = 1
        self.totalPage = 1
        self.pageSize = 10
        self.totalNum = 1
        self.Page()
        self.Page()
        # StyleSheet.VIEW_INTERFACE.apply(self)

    def __initWidget(self):
        self.setObjectName('userManagerInterface')
        self.view = QWidget(self)
        self.view.setObjectName('view')
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.view.setGeometry(QRect(0, 0, self.width(), 200))
        self.mainLayout = QVBoxLayout(self.view)
        topLayout = QHBoxLayout()
        label = BodyLabel()
        label.setText(self.tr("Username:"))
        topLayout.addWidget(label)
        self.usernameLineEdit = LineEdit()
        self.usernameLineEdit.setObjectName("usernameLineEdit")
        topLayout.addWidget(self.usernameLineEdit)
        self.searchBtn = PrimaryToolButton(FIF.SEARCH)
        self.searchBtn.setObjectName("searchBtn")
        topLayout.addWidget(self.searchBtn)
        topLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.flushBtn = PrimaryToolButton(FIF.SYNC)
        self.flushBtn.setObjectName("flushBtn")
        topLayout.addWidget(self.flushBtn)

        # self.statusBtn = PushButton(self.tr("Enable/Disable"))
        # self.statusBtn.setObjectName('statusBtn')
        # topLayout.addWidget(self.statusBtn)
        self.mainLayout.addLayout(topLayout)
        self.initTable()
        self.mainLayout.addWidget(self.tableWidget)
        bottomLayout = QHBoxLayout()
        bottomLayout.setSpacing(20)
        bottomLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.numLabel = BodyLabel()
        self.numLabel.setText(self.tr("1 in total"))
        bottomLayout.addWidget(self.numLabel)
        self.perPageComboBox = ComboBox()
        self.perPageComboBox.setObjectName("perPageComboBox")
        self.perPageComboBox.addItem(self.tr("10"))
        self.perPageComboBox.addItem(self.tr("20"))
        self.perPageComboBox.addItem(self.tr("50"))
        self.perPageComboBox.setCurrentIndex(0)
        bottomLayout.addWidget(self.perPageComboBox)
        self.prevBtn = PrimaryToolButton(FIF.LEFT_ARROW)
        bottomLayout.addWidget(self.prevBtn)
        self.pageLabel = BodyLabel()
        self.pageLabel.setText("1")
        bottomLayout.addWidget(self.pageLabel)
        self.nextBtn = PrimaryToolButton(FIF.RIGHT_ARROW)
        bottomLayout.addWidget(self.nextBtn)
        label = BodyLabel()
        label.setText(self.tr("Go to"))
        bottomLayout.addWidget(label)
        self.pageLineEdit = LineEdit()
        self.pageLineEdit.setFixedWidth(45)
        self.pageLineEdit.setObjectName("pageLineEdit")
        self.pageLineEdit.setText("1")
        self.pageLineEdit.setValidator(QIntValidator())
        bottomLayout.addWidget(self.pageLineEdit)
        label = BodyLabel()
        label.setText(self.tr("Page"))
        bottomLayout.addWidget(label)
        bottomLayout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.mainLayout.addLayout(bottomLayout)

    def initTable(self):
        self.tableWidget = TableWidget(self.view)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem(self.tr("Username")))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem(self.tr("Account")))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem(self.tr("Sex")))
        self.tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem(self.tr("Phone")))
        self.tableWidget.setHorizontalHeaderItem(4, QTableWidgetItem(self.tr("idNumber")))
        self.tableWidget.setHorizontalHeaderItem(5, QTableWidgetItem(self.tr("Status")))
        self.tableWidget.setHorizontalHeaderItem(6, QTableWidgetItem(self.tr("Last operation time")))
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)

    def initFun(self):
        self.flushBtn.clicked.connect(self.Page)
        self.searchBtn.clicked.connect(self.searchData)
        # self.statusBtn.clicked.connect(self.changeStatus)
        self.perPageComboBox.currentIndexChanged.connect(self.changePageSize)
        self.prevBtn.clicked.connect(self.prevPage)
        self.nextBtn.clicked.connect(self.nextPage)
        self.pageLineEdit.returnPressed.connect(self.changePage)

    def initConfig(self):
        # TODO 配置改造
        config = yaml.load(open('./app/config/ServerConfig.yaml', 'r'),
                           Loader=yaml.FullLoader)
        self.host = config["server"]["host"]
        self.port = config["server"]["port"]
        config = yaml.load(open('./app/config/ClientConfig.yaml', 'r'),
                           Loader=yaml.FullLoader)
        self.token = config["user"]["token"]

    def Page(self):
        name = self.usernameLineEdit.text()
        url = "http://{}:{}/admin/usr/page".format(self.host, self.port)
        payload = {
            "page": self.currentPage,
            "pageSize": self.pageSize
        }
        if name != "":
            payload["ame"] = name
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "token": self.token}
        try:
            response = requests.get(url, json=payload, headers=headers)
        except:
            self.showDialog(self.tr("Server Error"))
            return
        response = json.loads(response.text)
        # self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        if response["code"] == 1:
            self.totalNum = response["data"]["total"]
            self.numLabel.setText(self.tr("{} in total".format(self.totalNum)))
            self.totalPage = (self.totalNum + self.pageSize - 1) // self.pageSize
            records = response["data"]["records"]
            self.records = records
            self.tableWidget.setRowCount(len(records))
            for i in range(len(records)):
                # self.tableWidget.insertRow(self.tableWidget.rowCount())
                button = SwitchButton()
                button.setChecked(records[i]["status"] == 1)
                button.setText("Enable" if records[i]["status"] == 1 else "Disable")
                button.checkedChanged.connect(self.changeStatus)
                item = QTableWidgetItem(records[i]["name"])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, 0, item)
                item = QTableWidgetItem(records[i]["username"])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, 1, item)
                item = QTableWidgetItem(records[i]["sex"])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, 2, item)
                item = QTableWidgetItem(records[i]["phone"])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, 3, item)
                item = QTableWidgetItem(records[i]["idNumber"])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, 4, item)

                self.tableWidget.setCellWidget(i, 5, button)
                item = QTableWidgetItem(records[i]["updateTime"])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, 6, item)
            for row in range(self.tableWidget.rowCount()):
                self.tableWidget.setRowHeight(row, 50)
            # self.tableWidget.resizeRowsToContents()
        else:
            self.showDialog(response["msg"])

    def searchData(self):
        self.Page()

    def changeStatus(self):
        button = self.sender()
        if button:
            index = self.tableWidget.indexAt(button.pos())
            button.setText("Enable" if button.isChecked() else "Disable")
            if index.isValid():
                row = index.row()
                userId = self.records[row]["id"]
                status = 1 if button.isChecked() else 0
                url = "http://{}:{}/admin/usr/status/{}?id={}".format(self.host,
                                                                      self.port,
                                                                      status,
                                                                      userId)
                header = {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "token": self.token}
                # try:
                requests.post(url, headers=header)
                # except:
                #     self.showDialog(self.tr("Server Error"))
                #     return

    def changePageSize(self):
        oldPageSize = self.pageSize
        self.pageSize = int(self.perPageComboBox.currentText())
        self.currentPage = ((self.currentPage - 1) * oldPageSize // self.pageSize) + 1
        self.pageLineEdit.setText(str(self.currentPage))
        self.pageLabel.setText(str(self.currentPage))
        self.Page()
        pass

    def prevPage(self):
        if self.currentPage == 1:
            return
        else:
            self.currentPage -= 1
            self.pageLineEdit.setText(str(self.currentPage))
            self.pageLabel.setText(str(self.currentPage))
            self.Page()

    def nextPage(self):
        if self.currentPage == self.totalPage:
            return
        else:
            self.currentPage += 1
            self.pageLineEdit.setText(str(self.currentPage))
            self.pageLabel.setText(str(self.currentPage))
            self.Page()

    def changePage(self):
        page = int(self.pageLineEdit.text())

        if page < 1 or page > self.totalPage:
            return
        self.currentPage = page
        self.pageLabel.setText(str(self.currentPage))
        self.Page()

    def showDialog(self, msg):
        title = self.tr('ERROR')
        w = Dialog(title, msg, self)
        w.setTitleBarVisible(False)
        w.exec()
