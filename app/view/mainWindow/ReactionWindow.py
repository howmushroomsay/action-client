import json
import sys

import yaml
from PyQt5.QtCore import Qt, QUrl, QTimer, QLocale, QTime
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QTableWidgetItem,
                             QFileDialog, QSizePolicy)
from qfluentwidgets import (BodyLabel, PushButton, Slider, TableWidget,
                            )
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (ScrollArea, FluentTranslator,
                            LineEdit, TimeEdit, ComboBox, TextEdit,
                            PrimaryPushButton, Dialog)

from app.net.admin import HttpClientUtils, adminConfig


class ReactionWindow(ScrollArea):
    def __init__(self, parent=None, courseId=None):
        super().__init__()
        self.parent_ = parent
        self.setGeometry(100, 100, 1000, 600)
        self.courseId = courseId
        self.videoWidget = QVideoWidget()
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # controlLayout
        self.openBtn = PrimaryPushButton(self.tr("Open Video"))
        self.playBtn = PrimaryPushButton(self.tr("Play"), self, FIF.PLAY)
        self.slider = Slider(Qt.Horizontal)
        self.timeLabel = BodyLabel()
        self.pointTable = TableWidget()
        self.timer = QTimer(self)
        self.sliderDragging = False

        self.courseNameLabel = BodyLabel(self.tr("Course Name :"))
        self.courseNameLineEdit = LineEdit()
        self.courseIconLabel = BodyLabel()
        self.courseIconBtn = PrimaryPushButton(self.tr("Choose Icon"))
        self.courseDesTextEdit = TextEdit()

        self.startEdit = TimeEdit()
        self.endEdit = TimeEdit()
        self.getStartTimeBtn = PushButton(self.tr("Get Time"))
        self.getEndTimeBtn = PushButton(self.tr("Get Time"))
        self.actionCombox = ComboBox()
        self.desTextEdit = TextEdit()
        self.addBtn = PrimaryPushButton(self.tr("Add"))
        self.submitBtn = PrimaryPushButton(self.tr("Submit"))

        self.mainLayout = QVBoxLayout(self)
        self.topLayout = QHBoxLayout()
        self.pointLayout = QVBoxLayout()
        self.timeLayout = QHBoxLayout()
        self.controlLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout()
        self.iconLayout = QVBoxLayout()
        self.infoLayout = QVBoxLayout()
        self.nameLayout = QHBoxLayout()

        self.info = []

        # TODO 从服务端拉取，更新动作种类
        self.actionList = ["action1", "action2", "action3", "action4", "action5", ]
        self.videoPath = None
        self.iconPath = None

        self.__initWidget()
        self.__initLayout()
        self.__connectSignalToSlot()
        if self.courseId is not None:
            self.loadData()

    def __initWidget(self):
        self.videoWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.player.setVideoOutput(self.videoWidget)

        self.slider.setRange(0, 1000)
        self.startEdit.setDisplayFormat("mm:ss")
        self.endEdit.setDisplayFormat("mm:ss")
        self.pointTable.horizontalHeader().setVisible(True)
        self.pointTable.horizontalHeader().setStretchLastSection(True)
        self.pointTable.verticalHeader().setVisible(False)
        self.pointTable.setColumnCount(5)
        self.pointTable.setHorizontalHeaderLabels([self.tr("Start Time"),
                                                   self.tr("End Time"),
                                                   self.tr("Action"),
                                                   self.tr("Description"),
                                                   self.tr("Ops")])

        self.actionCombox.addItems(self.actionList)
        self.courseIconLabel.setFixedSize(160, 160)
        self.actionCombox.setCurrentIndex(0)
        self.courseIconBtn.setMaximumWidth(200)
        self.submitBtn.setMaximumWidth(200)
        # self.courseNameLineEdit.setMaximumWidth(200)
        self.desTextEdit.setMaximumHeight(100)


    def loadData(self):

        # TODO 整合所有的请求，封装到一个类中
        # 获取课程信息
        url = f"http://{adminConfig.host}:{adminConfig.port}/admin/course/reaction/{self.courseId}"
        try:
            response = HttpClientUtils.doGetWithToken(url)
            response = json.loads(response.text)
            if response["code"] == 0:
                self.showDialog(response["msg"])
                return
            data = response["data"]
        except Exception as e:
            print(e)
            self.showDialog(self.tr("Server Error"))
            return

        self.courseNameLineEdit.setText(data["courseName"])
        self.courseDesTextEdit.setText(data["courseDes"])
        # 设置检查点
        points = data["points"]
        for point in points:
            self.info.append([self.seconds2time(point["startTime"]),
                              self.seconds2time(point["endTime"]),
                              point["action"],
                              point["pointDes"]])
        # 获取课程图标
        url = f"http://{adminConfig.host}:{adminConfig.port}/admin/common/download/{data['icon']}"
        try:
            response = HttpClientUtils.doGetWithToken(url, headers={"type": "thumbnail"})
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            pixmap = pixmap.scaled(self.courseIconLabel.size(),
                                   Qt.KeepAspectRatio,
                                   Qt.SmoothTransformation)
            self.courseIconLabel.setPixmap(pixmap)
        except:
            self.showDialog(self.tr("Server Error"))
            return
        # 获取课程视频
        url = f"http://{adminConfig.host}:{adminConfig.port}/admin/common/download/{data['videoPath']}"
        # TODO 使用配置指定文件路径
        try:
            response = HttpClientUtils.doGetWithToken(url, headers={"type": "video"})
            with open("app/temp/course.mp4", 'wb') as f:
                f.write(response.content)
            self.openVideo(fileName="app/temp/course.mp4", flag=False)
        except Exception as e:
            print(e)
            self.showDialog(self.tr("Server Error"))
            return
        self.showTable()

    def __initLayout(self):
        self.pointTable.setFixedWidth(600)
        self.videoWidget.setMinimumSize(800, 600)
        self.topLayout.addWidget(self.videoWidget)
        # self.topLayout.addWidget(self.pointTable)

        self.pointLayout.addWidget(self.pointTable)
        self.timeLayout.addWidget(self.startEdit)
        self.timeLayout.addWidget(self.getStartTimeBtn)
        self.timeLayout.addWidget(self.endEdit)
        self.timeLayout.addWidget(self.getEndTimeBtn)
        self.timeLayout.addWidget(self.actionCombox)
        self.timeLayout.addWidget(self.addBtn)
        self.pointLayout.addLayout(self.timeLayout)
        self.pointLayout.addWidget(self.desTextEdit)
        self.topLayout.addLayout(self.pointLayout)

        self.controlLayout.addWidget(self.openBtn)
        self.controlLayout.addWidget(self.playBtn)
        self.controlLayout.addWidget(self.slider)
        self.controlLayout.addWidget(self.timeLabel)

        self.iconLayout.addWidget(self.courseIconLabel)
        self.iconLayout.addWidget(self.courseIconBtn)
        self.bottomLayout.addLayout(self.iconLayout)

        self.nameLayout.addWidget(self.courseNameLabel)
        self.nameLayout.addWidget(self.courseNameLineEdit)
        self.infoLayout.addLayout(self.nameLayout)
        self.infoLayout.addWidget(self.courseDesTextEdit)
        self.infoLayout.addWidget(self.submitBtn)
        self.bottomLayout.addLayout(self.infoLayout)

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.controlLayout)
        self.mainLayout.addLayout(self.bottomLayout)

    def __connectSignalToSlot(self):
        self.openBtn.clicked.connect(self.openVideo)
        self.playBtn.clicked.connect(self.pauseVideo)

        self.slider.sliderPressed.connect(lambda: self.changeSlider(True))
        self.slider.sliderReleased.connect(lambda: self.changeSlider(False))

        self.timer.timeout.connect(self.updateTime)

        self.getStartTimeBtn.clicked.connect(self.getTime)
        self.getEndTimeBtn.clicked.connect(self.getTime)
        self.addBtn.clicked.connect(self.addPoint)
        self.submitBtn.clicked.connect(self.submit)
        self.courseIconBtn.clicked.connect(self.getIcon)

    def openVideo(self, clicked=False, fileName=None, flag=True):
        if fileName is None:
            fileName, _ = QFileDialog.getOpenFileName(self, self.tr("Open Video"), "",
                                                      "Video Files (*.mp4 *.flv *.ts *.mts *.avi *.wmv *.mov *.rmvb *.rm *.asf *.m4v *.mkv)")
        if fileName:
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.player.play()
            self.timer.start()
            if flag:
                self.videoPath = fileName

    def pauseVideo(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(FIF.PAUSE)
            self.player.pause()
        else:
            self.playBtn.setIcon(FIF.PLAY)
            self.player.play()

    def changeSlider(self, isDragging):
        # TODO 拖动进度条
        self.sliderDragging = isDragging

    def updateTime(self):
        if not self.sliderDragging:
            currentTime = self.player.position()
            duration = self.player.duration()
            self.slider.setValue(int(currentTime / (duration + 0.01) * 1000))
            self.timeLabel.setText(f"""{self.formatTime(currentTime // 1000)} / {self.formatTime(duration // 1000)}""")

    def formatTime(self, seconds):
        minutes = int(seconds) // 60
        seconds %= 60
        return f"{minutes:02}:{seconds:02}"

    def getTime(self):
        seconds = self.player.position() // 1000
        minutes = seconds // 60
        seconds %= 60
        if self.sender() == self.getStartTimeBtn:
            self.startEdit.setTime(QTime(0, minutes, seconds))
        else:
            self.endEdit.setTime(QTime(0, minutes, seconds))

    def addPoint(self):
        startTime = self.startEdit.time().toString("mm:ss")
        endTime = self.endEdit.time().toString("mm:ss")
        action = self.actionCombox.currentIndex()
        des = self.desTextEdit.toPlainText()
        if startTime >= endTime:
            self.showDialog(self.tr("Start time must be less than end time"))
            return

        for i in range(len(self.info)):
            if self.info[i][0] == startTime:
                self.showDialog(self.tr("The start time is overlapped"))
                return
            if self.info[i][0] == endTime:
                self.showDialog(self.tr("The end time is overlapped"))
                return
        self.info.append([startTime, endTime, action, des])
        # self.info.sort()
        infocopy = self.info[:]
        infocopy.sort()
        for i in range(1, len(self.info)):
            if infocopy[i][1] <= infocopy[i - 1][1] or infocopy[i - 1][1] >= infocopy[i][0]:
                self.showDialog(self.tr("The time is overlapped"))
                self.info.pop(-1)
                return
        self.info = infocopy
        self.showTable()

    @staticmethod
    def time2seconds(timeString):
        minutes, seconds = map(int, timeString.split(':'))
        totalSeconds = minutes * 60 + seconds
        return totalSeconds

    @staticmethod
    def seconds2time(second):
        minutes, second = divmod(second, 60)
        return f"{minutes:02d}:{second:02d}"

    def showTable(self):
        self.pointTable.setRowCount(len(self.info))
        for i in range(len(self.info)):
            button = PushButton(self.tr("Delete"))
            combox = ComboBox()
            combox.addItems(self.actionList)
            combox.setCurrentIndex(int(self.info[i][2]))

            button.clicked.connect(self.deletePoint)
            item = QTableWidgetItem(str(self.info[i][0]))
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.pointTable.setItem(i, 0, item)
            item = QTableWidgetItem(str(self.info[i][1]))
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.pointTable.setItem(i, 1, item)
            self.pointTable.setCellWidget(i, 2, combox)
            self.pointTable.setItem(i, 3, QTableWidgetItem(str(self.info[i][3])))
            self.pointTable.setCellWidget(i, 4, button)

    def deletePoint(self):
        button = self.sender()
        if button:
            index = self.pointTable.indexAt(button.pos())
            if index.isValid():
                self.info.pop(index.row())
                self.showTable()

        # row = self.pointTable.currentRow()
        # self.info.pop(row)
        # self.showTable()

    def submit(self):
        courseName = self.courseNameLineEdit.text().strip()
        # 校验必填项
        if courseName == "":
            self.showDialog(self.tr("Course name is required"))
            return
        if len(self.info) == 0:
            self.showDialog(self.tr("Please add at least one point"))
            return
        url = f"http://{adminConfig.host}:{adminConfig.port}/admin/common/upload"
        # 上传课程封面
        if self.iconPath is not None:

            headers = {"type": "thumbnail"}
            files = [('file', (self.iconPath, open(self.iconPath, 'rb'), 'image/png'))]
            try:
                response = HttpClientUtils.doPostWithToken(url, files=files, headers=headers)
                self.iconPath = json.loads(response.text)["data"]
            except:
                self.showDialog(self.tr("Upload Image failed"))
                return
        else:
            if self.courseId is None:
                self.showDialog(self.tr("Please upload course icon"))
                return

        # 上传视频
        if self.videoPath is not None:
            headers = {"type": "video"}
            files = [('file', (self.videoPath, open(self.videoPath, 'rb'), 'application/octet-stream'))]
            try:
                response = HttpClientUtils.doPostWithToken(url, files=files, headers=headers)
                self.videoPath = json.loads(response.text)["data"]
            except:
                self.showDialog(self.tr("Upload Video failed"))
                return
        else:
            if self.courseId is None:
                self.showDialog(self.tr("Please upload course video"))
                return
                # 上传课程信息

        url = f"http://{adminConfig.host}:{adminConfig.port}/admin/course/reaction"
        point = []
        for i in range(len(self.info)):
            point.append({
                "startTime": self.time2seconds(self.info[i][0]),
                "endTime": self.time2seconds(self.info[i][1]),
                "action": self.info[i][2],
                "pointDes": self.info[i][3],
            })
        data = {
            "id": self.courseId,
            "courseName": self.courseNameLineEdit.text(),
            "courseDes": self.courseDesTextEdit.toPlainText(),
            "status": 1,
            "pointList": point,
        }
        if self.videoPath is not None:
            data["videoPath"] = self.videoPath
        if self.iconPath is not None:
            data["icon"] = self.iconPath
        try:
            if self.courseId is not None:
                response = HttpClientUtils.doPutWithToken(url, data=data)
            else:
                response = HttpClientUtils.doPostWithToken(url, data=data)
            statusCode = json.loads(response.text)["code"]
            if statusCode != 1:
                self.showDialog(self.tr(json.loads(response.text)["msg"]))
                return
        except:
            self.showDialog(self.tr("Upload Info failed"))
            return

    def getIcon(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Open Image",
                                                  "",
                                                  "Image Files (*.png *.jpg *.jpeg)")

        if fileName:
            pixmap = QPixmap(fileName).scaled(self.courseIconLabel.size(),
                                              Qt.KeepAspectRatio,
                                              Qt.SmoothTransformation)
            self.courseIconLabel.setPixmap(pixmap)
            self.iconPath = fileName

    def showDialog(self, msg):
        w = Dialog(self.tr("ERROR"), msg, self)
        w.setTitleBarVisible(False)
        w.exec()

    def closeEvent(self, event):
        if self.parent_ is not None:
            self.parent_.fresh()
        event.accept()


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    # Internationalization
    translator = FluentTranslator(QLocale())
    app.installTranslator(translator)

    w = ReactionWindow(courseId=None)
    w.show()
    app.exec_()
