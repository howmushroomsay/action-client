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
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QHBoxLayout, QSizePolicy)


from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QStackedWidget)
from qfluentwidgets import (ScrollArea, FlowLayout,IconWidget,
                            SegmentedWidget, SmoothScrollArea,
                            PrimaryPushButton, CardWidget)
from qfluentwidgets import FluentIcon as FIF
from common.style_sheet import StyleSheet

from dataclasses import dataclass

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

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.view = QWidget()
        self.flowLayout = FlowLayout(self.view)
        self.__initWidget()

    def __initWidget(self):
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 5, 0, 5)

    def addCard(self, metadata):
        card = CourseCard(metadata)
        self.flowLayout.addWidget(card)
    
    # def addCard(self, courseName, courseImgPath):
    #     card = CourseCard(courseName, courseImgPath)
    #     self.flowLayout.addWidget(card)

class CourseCard(CardWidget):
    def __init__(self, metadata: Course, parent=None):
        super().__init__(parent=parent)

        self.metadata = metadata

        self.titleLabel = QLabel(metadata.courseName, self)
        self.desLabel = QLabel(metadata.courseDes, self)
        self.timeLabel = QLabel(metadata.updateTime, self)
        self.timeIcon = IconWidget(FIF.DATE_TIME, self)
        self.editBtn = PrimaryPushButton(self.tr("Edit"))
        # self.detailBtn = PrimaryPushButton(self.tr("View Detials"))
        self.imgLabel = QLabel(self)

        self.mangerLayout = QVBoxLayout(self)
        self.hearderLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottonLayout = QHBoxLayout()
        self.__initWidget()
        self.__initLayout()
        self.__initSubWidget()

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
        self.editBtn.clicked.connect(self.edit_course)
        img = QPixmap(self.metadata.icon).scaled(100, 100, Qt.KeepAspectRatioByExpanding)
        self.imgLabel.setPixmap(img)
        self.mangerLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
    def edit_course(self):
        print(f"Editing {self.metadata.courseName}")

class CardView(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.pivot = SegmentedWidget(self)
        self.stackedContainer = QStackedWidget(self)
        self.reactionCardView = CourseCardView(self)
        self.standardCardView = CourseCardView(self)

        self.layoutManager = QVBoxLayout(self)

        self.__initSubWidget()
        self.__initLayout()
        self.loadData()

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

    def loadData(self):
        # TODO 暂时不考虑分页，实现数据展示

        metadata = Course(1, "course1", "course", "course1", 
                          "D:\project\data\img\d0fcbdbe-e00a-40da-a921-46b6de0b3a03.png", 
                          1, "2021-01-01", "2021-01-01", 1, 1)
        for i in range(10):
            self.reactionCardView.addCard(metadata)
            # self.standardCardView.addCard("course{}".format(i),
                                        #   "app/resource/images/Shoko{}.jpg".format(i%4+1))

class CourseManagerInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.viewContainer = QWidget()
        self.cardView = CardView(self)
        self.containerLayout = QVBoxLayout(self.viewContainer)
        self.CourseLabel = QLabel(self.tr("Course Manager"), self)

        self.__initWidget()
        self.__initLayout()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setObjectName("CourseManagerInterface")
        self.setWidget(self.viewContainer)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        # TODO 创建新的css文件
        StyleSheet.NAVIGATION_VIEW_INTERFACE.apply(self)
    
    def __initLayout(self):
        self.viewContainer.setObjectName("CourseManegerInterfaceViewContainer")
        self.containerLayout.addWidget(self.CourseLabel)
        self.containerLayout.setContentsMargins(36, 20, 36, 12)
        self.containerLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.containerLayout.addWidget(self.cardView)
