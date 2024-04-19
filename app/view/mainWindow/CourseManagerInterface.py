# coding:utf-8
import json
import sys
import os
import requests
import yaml

from app.common.config import isWin11
# 获取当前脚本所在路径
current_path = os.path.dirname(os.path.abspath(__file__))

# 添加上上级目录到sys.path
parent_path = os.path.abspath(os.path.join(current_path, '..'))
grandparent_path = os.path.abspath(os.path.join(parent_path, '..'))
sys.path.append(grandparent_path)

config = yaml.load(open('./app/config/ServerConfig.yaml', 'r'), 
                           Loader=yaml.FullLoader)
host = config["server"]["host"]
port = config["server"]["port"]

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QHBoxLayout, QSizePolicy)


from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QStackedWidget)
from qfluentwidgets import (ScrollArea, FlowLayout,IconWidget,
                            SegmentedWidget, SmoothScrollArea,
                            PrimaryPushButton, CardWidget, BodyLabel)
from qfluentwidgets import FluentIcon as FIF
from common.style_sheet import StyleSheet
from dataclasses import dataclass

from ReactionWindow import ReactionWindow

@dataclass
class Course:
    id: int
    courseName: str
    courseDes: str
    videoPath: str
    icon: str
    status: int
    createTime: str
    updateTime: str
    createUser: int
    updateUser: int

class CourseCardView(SmoothScrollArea):

    def __init__(self, parent=None, courseType=None):
        super().__init__(parent=parent)
        self.view = QWidget()
        self.courseType = courseType
        self.flowLayout = FlowLayout(self.view)
        self.__initWidget()
        self.loadData()

    def __initWidget(self):
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 5, 0, 5)

    def addCard(self, metadata):
        card = CourseCard(metadata, parent=self)
        self.flowLayout.addWidget(card)
    def page(self):
        # TODO
        pass
    def clearCard(self):
        self.flowLayout.removeAllWidgets()
    
    def fresh(self):
        self.clearCard()
        self.loadData()
    # def addCard(self, courseName, courseImgPath):
    #     card = CourseCard(courseName, courseImgPath)
    #     self.flowLayout.addWidget(card)
    def loadData(self):
        # TODO 暂时不考虑分页，实现数据展示
        url = "http://{}:{}/admin/course/{}/all".format(host, port, self.courseType)
        try:
            response = requests.get(url)
        except Exception as e:
            print(e)
            return
        response = json.loads(response.text)
        if response["code"] == 0:
            self.showDialog(response["msg"])
            return
        data = response["data"]
        for d in data:
            metadata = Course(d["id"], 
                            d["courseName"],
                            d["courseDes"],
                            d["videoPath"],
                            d["icon"],
                            d["status"],
                            d["createTime"],
                            d["updateTime"],
                            d["createUser"],
                            d["updateUser"])
            self.addCard(metadata)
class CourseCard(CardWidget):
    def __init__(self, metadata: Course, parent=None):
        super().__init__(parent=parent)
        self.parent_ = parent
        self.metadata = metadata

        self.titleLabel = QLabel(metadata.courseName, self)
        self.desLabel = QLabel(metadata.courseDes, self)
        self.timeLabel = QLabel(metadata.updateTime, self)
        self.timeIcon = IconWidget(FIF.DATE_TIME, self)
        self.editBtn = PrimaryPushButton(self.tr("Edit"))
        # self.detailBtn = PrimaryPushButton(self.tr("View Detials"))
        self.imgLabel = BodyLabel()

        self.mangerLayout = QVBoxLayout(self)
        self.hearderLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottonLayout = QHBoxLayout()
        self.loadData()
        self.__initWidget()
        self.__initLayout()
        self.__initSubWidget()
        self.editBtn.clicked.connect(self.editCourse)
        
    def loadData(self):
        url =  "http://{}:{}/admin/common/download/{}".format(host, port, self.metadata.icon)
        try:
            response = requests.get(url, headers={"type": "thumbnail"})
            self.icon = QPixmap()
            self.icon.loadFromData(response.content)
            self.icon = self.icon.scaled(100, 100, Qt.KeepAspectRatio, 
                                                    Qt.SmoothTransformation)
                    
        except:
            pass

    def __initWidget(self):
        self.setObjectName("CourseCard")
        # TODO css

        self.titleLabel.setObjectName("CourseCardTitleLabel")
        self.desLabel.setObjectName("CourseCardDesLabel")
        self.timeLabel.setObjectName("CourseCardTimeLabel")
        self.timeIcon.setToolTip(self.tr("update time"))

    def __initLayout(self):
        self.setFixedSize(360, 168)
        self.mangerLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | 
                                       Qt.AlignmentFlag.AlignTop)
        # self.mangerLayout.setContentsMargins(16, 12, 12, 12)
        self.topLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.hearderLayout.addWidget(self.titleLabel)
        self.hearderLayout.addWidget(self.desLabel)
        self.topLayout.addLayout(self.hearderLayout)
        self.topLayout.addWidget(self.imgLabel)
        self.mangerLayout.addLayout(self.topLayout)
        self.bottonLayout.addWidget(self.timeIcon)
        self.bottonLayout.addWidget(self.timeLabel)
        self.bottonLayout.addWidget(self.editBtn)
        self.mangerLayout.addLayout(self.bottonLayout)

    def __initSubWidget(self):
        self.desLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.imgLabel.setFixedSize(100, 100)
        self.timeIcon.setFixedSize(14, 14)
        self.editBtn.setFixedWidth(80)

        self.imgLabel.setPixmap(self.icon)
        self.mangerLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
    def editCourse(self):
        editWindow = ReactionWindow(courseId=self.metadata.id)
        editWindow.show()

class CardView(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.pivot = SegmentedWidget(self)
        self.stackedContainer = QStackedWidget(self)
        self.reactionCardView = CourseCardView(self, courseType="reaction")
        self.standardCardView = CourseCardView(self, courseType="standard")

        self.layoutManager = QVBoxLayout(self)

        self.__initSubWidget()
        self.__initLayout()
        

    def __initSubWidget(self):
        self.reactionCardView.setObjectName("ReactionCardView")
        self.standardCardView.setObjectName("StandardCardView")

        self.stackedContainer.addWidget(self.reactionCardView)
        self.pivot.addItem(
            self.reactionCardView.objectName(),
            self.tr("Reaction Course"),
            lambda: self.stackedContainer.setCurrentWidget(self.reactionCardView)
        )
        self.stackedContainer.addWidget(self.standardCardView)
        self.pivot.addItem(
            self.standardCardView.objectName(),
            self.tr("Standard Course"),
            lambda: self.stackedContainer.setCurrentWidget(self.standardCardView)
        )

        self.stackedContainer.setCurrentWidget(self.reactionCardView)
        self.pivot.setCurrentItem(self.reactionCardView.objectName())

        self.stackedContainer.currentChanged.connect(self.onCurrentIndexChanged)

    def __initLayout(self):
        self.layoutManager.addWidget(self.pivot)
        self.layoutManager.addWidget(self.stackedContainer)

    def onCurrentIndexChanged(self, index):
        widget = self.stackedContainer.widget(index)
        self.pivot.setCurrentItem(widget.objectName())
    
 


        
class CourseManagerInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.viewContainer = QWidget()
        self.cardView = CardView(self)
        self.containerLayout = QVBoxLayout(self.viewContainer)
        self.CourseLabel = QLabel(self.tr("Course Manager"), self)
        self.addBtn = PrimaryPushButton(self.tr("Add Course"), self, FIF.ADD)
        self.topLayout = QHBoxLayout()

        self.__initWidget()
        self.__initLayout()
        self.__initFun()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setObjectName("CourseManagerInterface")
        self.setWidget(self.viewContainer)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.addBtn.setMaximumWidth(150)
        # TODO 创建新的css文件
        StyleSheet.NAVIGATION_VIEW_INTERFACE.apply(self)
    
    def __initLayout(self):
        self.viewContainer.setObjectName("CourseManegerInterfaceViewContainer")

        self.topLayout.addWidget(self.CourseLabel)
        self.topLayout.addWidget(self.addBtn)
        # self.containerLayout.addWidget(self.CourseLabel)
        self.containerLayout.addLayout(self.topLayout)
        self.containerLayout.setContentsMargins(36, 20, 36, 12)
        self.containerLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.containerLayout.addWidget(self.cardView)
    
    def __initFun(self):
        self.addBtn.clicked.connect(self.addCourse)
    
    def addCourse(self):
        current = self.cardView.stackedContainer.currentIndex()
        if current == 0:
            addWindow = ReactionWindow(parent=self.cardView.reactionCardView)
            addWindow.show()

