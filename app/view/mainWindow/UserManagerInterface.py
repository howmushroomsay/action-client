# coding:utf-8
import json
import sys
import os
import requests
import yaml
# 获取当前脚本所在路径
current_path = os.path.dirname(os.path.abspath(__file__))

# 添加上上级目录到sys.path
parent_path = os.path.abspath(os.path.join(current_path, '..'))
grandparent_path = os.path.abspath(os.path.join(parent_path, '..'))
sys.path.append(grandparent_path)

from PyQt5.QtCore import Qt, QRectF, QRect
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPainterPath
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, 
                             QSpacerItem, QAbstractItemView, QTableWidgetItem,
                             QHeaderView)
from qfluentwidgets import (ScrollArea, FluentIcon, BodyLabel, LineEdit, 
                            PushButton, TableWidget, ComboBox, Dialog)
from common.style_sheet import StyleSheet

class UserManagerInterface(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)
        # 获取数据
        # self.setFixedHeight(350)
        self.initWidget()
        self.initFun()
        self.initConfig()
        self.currentPage = 1
        self.totalPage = 1
        self.pageSize = 10
        self.totalNum = 1
        self.Page()
    def initWidget(self):
        self.setObjectName('userManagerInterface')
        self.view = QWidget(self)
        self.view.setObjectName('view')
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.view.setGeometry(QRect(0, 0, self.width(), 200))
        self.vBoxLayout = QVBoxLayout(self.view)
        hBoxLayout1 = QHBoxLayout()
        label = BodyLabel()
        label.setText(self.tr("用户姓名:"))
        hBoxLayout1.addWidget(label)
        self.usernameLineEdit = LineEdit()
        self.usernameLineEdit.setObjectName("usernameLineEdit")
        hBoxLayout1.addWidget(self.usernameLineEdit)
        self.searchBtn = PushButton(self.tr("搜索"))
        self.searchBtn.setObjectName("searchBtn")
        hBoxLayout1.addWidget(self.searchBtn)
        hBoxLayout1.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.statusBtn = PushButton(self.tr("启用/禁用"))
        self.statusBtn.setObjectName('statusBtn')
        hBoxLayout1.addWidget(self.statusBtn)
        self.vBoxLayout.addLayout(hBoxLayout1)
        self.initTable()
        self.vBoxLayout.addWidget(self.tableWidget)
        hBoxLayout2 = QHBoxLayout()
        hBoxLayout2.setSpacing(20)
        hBoxLayout2.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.numLabel = BodyLabel()
        self.numLabel.setText(self.tr("共1条"))
        hBoxLayout2.addWidget(self.numLabel)
        self.perPageComboBox = ComboBox()
        self.perPageComboBox.setObjectName("perPageComboBox")
        self.perPageComboBox.addItem(self.tr("10"))
        self.perPageComboBox.addItem(self.tr("20"))
        self.perPageComboBox.addItem(self.tr("50"))
        self.perPageComboBox.setCurrentIndex(0)
        hBoxLayout2.addWidget(self.perPageComboBox)
        self.prevBtn = PushButton(self.tr("上一页"))
        hBoxLayout2.addWidget(self.prevBtn)
        self.pageLabel = BodyLabel()
        self.pageLabel.setText("1")
        hBoxLayout2.addWidget(self.pageLabel)
        self.nextBtn = PushButton(self.tr("下一页"))
        hBoxLayout2.addWidget(self.nextBtn)
        label = BodyLabel()
        label.setText(self.tr("前往"))
        hBoxLayout2.addWidget(label)
        self.pageLineEdit = LineEdit()
        self.pageLineEdit.setFixedWidth(45)
        self.pageLineEdit.setObjectName("pageLineEdit")
        self.pageLineEdit.setText("1")
        hBoxLayout2.addWidget(self.pageLineEdit)
        label = BodyLabel()
        label.setText(self.tr("页"))
        hBoxLayout2.addWidget(label)
        hBoxLayout2.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.vBoxLayout.addLayout(hBoxLayout2)
    
    def initTable(self):
        self.tableWidget = TableWidget(self.view)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem(self.tr("姓名")))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem(self.tr("账号")))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem(self.tr("性别")))
        self.tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem(self.tr("电话")))
        self.tableWidget.setHorizontalHeaderItem(4, QTableWidgetItem(self.tr("身份证")))
        self.tableWidget.setHorizontalHeaderItem(5, QTableWidgetItem(self.tr("账号状态")))
        self.tableWidget.setHorizontalHeaderItem(6, QTableWidgetItem(self.tr("最后操作时间")))
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        # self.tableWidget.verticalHeader().setStretchLastSection(False)
    
    def initFun(self):
        self.searchBtn.clicked.connect(self.searchData)
        self.statusBtn.clicked.connect(self.changeStatus)
        self.perPageComboBox.currentIndexChanged.connect(self.changePageSize)
        self.prevBtn.clicked.connect(self.prevPage)
        self.nextBtn.clicked.connect(self.nextPage)
        self.pageLineEdit.returnPressed.connect(self.changePage)
    
    def initConfig(self):
        config = yaml.load(open('./app/config/ServerConfig.yaml', 'r'), 
                           Loader=yaml.FullLoader)
        self.host = config["server"]["host"]
        self.port = config["server"]["port"]
        config = yaml.load(open('./app/config/ClientConfig.yaml', 'r'), 
                           Loader=yaml.FullLoader)
        self.token = config["user"]["token"]
    def Page(self, name=""):
        url = "http://{}:{}/admin/usr/page".format(self.host, self.port)
        payload = json.dumps({
            "name": name if name is not None and name != "" else None,
            "page": self.currentPage,
            "pageSize": self.pageSize
        })
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "token": self.token}
        
        response = requests.get(url, data=payload, headers=headers)
        response = json.loads(response.text)
        # self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        if (response["code"] == 1):
            self.totalNum = response["data"]["total"]
            self.totalPage = (self.totalNum + self.pageSize - 1) // self.pageSize
            for i in range(len(response["data"]["records"])):
                self.tableWidget.insertRow(self.tableWidget.rowCount())
                item = QTableWidgetItem(response["data"]["records"][i]["name"])
                item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, item)
                item = QTableWidgetItem(response["data"]["records"][i]["username"])
                item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, item)
                item = QTableWidgetItem(response["data"]["records"][i]["sex"])
                item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, item)
                item = QTableWidgetItem(response["data"]["records"][i]["phone"])
                item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, item)
                item = QTableWidgetItem(response["data"]["records"][i]["idNumber"])
                item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 4, item)
                item = QTableWidgetItem("已启用" if response["data"]["records"][i]["phone"]else "已禁用")
                item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 5, item)
                item = QTableWidgetItem(response["data"]["records"][i]["updateTime"])
                item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 6, item)
            for row in range(self.tableWidget.rowCount()):
                self.tableWidget.setRowHeight(row, 50)
            # self.tableWidget.resizeRowsToContents()
        else:
            errorMsg = response["msg"]
            self.showDialog(errorMsg)
    def searchData(self):
        name = self.usernameLineEdit.text()
        self.Page(name)

    def changeStatus(self):

        pass

    def changePageSize(self):
        oldPageSize = self.pageSize
        self.pageSize = int(self.perPageComboBox.currentText())
        self.currentPage = ((self.currentPage - 1) * oldPageSize // self.pageSize) + 1
        self.pageLineEdit.setText(str(self.currentPage))        
        self.pageLabel.setText(str(self.currentPage))
        self.Page()
        pass

    def prevPage(self):
        if (self.currentPage == 1):
            return
        else:
            self.currentPage -= 1
            self.pageLineEdit.setText(str(self.currentPage))
            self.pageLabel.setText(str(self.currentPage))
            self.Page()

    def nextPage(self):
        if (self.currentPage == self.totalPage):
            return
        else:
            self.currentPage += 1
            self.pageLineEdit.setText(str(self.currentPage))
            self.pageLabel.setText(str(self.currentPage))
            self.Page()
    def changePage(self):
        if (self.currentPage == self.totalPage):
            return
        else:
            self.currentPage = int(self.pageLineEdit.text())
            self.Page()
    def showDialog(self, msg):
        title = '错误'
        w = Dialog(title, msg, self)
        w.setTitleBarVisible(False)
        w.exec()