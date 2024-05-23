# coding:utf-8
import json
import time
from dataclasses import dataclass

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QLabel, QHBoxLayout, QSizePolicy)
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QStackedWidget)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (ScrollArea, FlowLayout, IconWidget,
                            SegmentedWidget, SmoothScrollArea,
                            PrimaryPushButton, CardWidget, BodyLabel)

from app.common.style_sheet import StyleSheet
from app.net.admin import adminConfig, HttpClientUtils
from .ReactionWindow import ReactionWindow
from .StandardWindow import StandardWindow


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
        card = CourseCard(metadata, parent=self, isStandard=self.courseType == 'standard')
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
        url = "http://{}:{}/admin/course/{}/all".format(adminConfig.host, adminConfig.port, self.courseType)
        try:
            response = HttpClientUtils.doGetWithToken(url)
        except Exception as e:
            print(e)
            return
        if response.status_code != 200:
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

    def showDialog(self, msg):
        pass


class CourseCard(CardWidget):
    def __init__(self, metadata: Course, parent=None, isStandard=False):
        super().__init__(parent=parent)
        self.icon = None
        self.parent_ = parent
        self.metadata = metadata
        self.isStandard = isStandard
        self.titleLabel = QLabel(metadata.courseName, self)
        self.desLabel = QLabel(metadata.courseDes, self)
        self.timeLabel = QLabel(metadata.updateTime, self)
        self.timeIcon = IconWidget(FIF.DATE_TIME, self)
        self.editBtn = PrimaryPushButton(self.tr("Edit"))
        # self.detailBtn = PrimaryPushButton(self.tr("View Details"))
        self.imgLabel = BodyLabel()

        self.mangerLayout = QVBoxLayout(self)
        self.heardLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout()
        self.loadData()
        self.__initWidget()
        self.__initLayout()
        self.__initSubWidget()
        self.editBtn.clicked.connect(self.editCourse)

    def loadData(self):
        url = f"http://{adminConfig.host}:{adminConfig.port}/admin/common/download/{self.metadata.icon}"
        try:
            response = HttpClientUtils.doGetWithToken(url, headers={"type": "thumbnail"})
            self.icon = QPixmap()
            self.icon.loadFromData(response.content)
            self.icon = self.icon.scaled(100, 100, Qt.KeepAspectRatio,
                                         Qt.SmoothTransformation)

        except Exception as e:
            print(e)

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
        self.heardLayout.addWidget(self.titleLabel)
        self.heardLayout.addWidget(self.desLabel)
        self.topLayout.addLayout(self.heardLayout)
        self.topLayout.addWidget(self.imgLabel)
        self.mangerLayout.addLayout(self.topLayout)
        self.bottomLayout.addWidget(self.timeIcon)
        self.bottomLayout.addWidget(self.timeLabel)
        self.bottomLayout.addWidget(self.editBtn)
        self.mangerLayout.addLayout(self.bottomLayout)

    def __initSubWidget(self):
        self.desLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.imgLabel.setFixedSize(100, 100)
        self.timeIcon.setFixedSize(14, 14)
        self.editBtn.setFixedWidth(80)

        self.imgLabel.setPixmap(self.icon)
        self.mangerLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

    def editCourse(self):
        if self.isStandard:
            editWindow = StandardWindow(course_id=self.metadata.id)
        else:
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
        self.viewContainer.setObjectName("CourseManagerInterfaceViewContainer")

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
            self.addWindow = ReactionWindow(parent=self.cardView.reactionCardView)

        elif current == 1:
            self.addWindow = StandardWindow(parent=self.cardView.standardCardView)
        self.addWindow.show()

