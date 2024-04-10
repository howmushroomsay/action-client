import sys
import requests
import json
# import cv2

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, 
                             QVBoxLayout, QHBoxLayout, QTableWidgetItem, 
                             QFileDialog,QSizePolicy)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, QTimer, QLocale, QTime

from qfluentwidgets import (ScrollArea, FlowLayout,IconWidget,PillPushButton,
                            SegmentedWidget, SmoothScrollArea,FluentTranslator,
                            PushButton,LineEdit,TimeEdit,ComboBox,TextEdit,
                            PrimaryPushButton, Dialog, ToolButton)
from qfluentwidgets import FluentIcon as FIF

from qfluentwidgets import (BodyLabel, PushButton, Slider, TableWidget,
                            )


class ReactionWindow(ScrollArea):
    def __init__(self, parent=None, id=None):
        super().__init__()
        self.setGeometry(100, 100, 1000, 600)
        self.id = id
        self.videoWidget = QVideoWidget()
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.openBtn = PrimaryPushButton(self.tr("Open Video"))
        self.playBtn = PrimaryPushButton(self.tr("Play"),self,FIF.PLAY)
        self.slider = Slider(Qt.Horizontal)
        self.timeLabel = BodyLabel()
        self.pointTable = TableWidget()
        self.timer = QTimer(self)
        self.sliderDragging = False

        self.courseNameLineEdit = LineEdit()
        self.courseIconLabel = BodyLabel()
        self.courseIconBtn = PrimaryPushButton(self.tr("Open Image"))

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
        self.bottomLayout = QHBoxLayout()
        self.courseLayout = QVBoxLayout()
        self.controlLayout = QHBoxLayout()
        self.addLayout = QVBoxLayout()
        self.timeLayout = QHBoxLayout()


        self.info = []
        self.actionDict = {
            "action1": 0,
            "action2": 1,
            "action3": 2,
            "action4": 3,
            "action5": 4,}
        self.icon = None

        self.__initWidget()
        self.__initLayout()
        self.__connectSignalToSlot()
        
        self.loadData(self)

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
        
        items = ["action1", "action2", "action3", "action4", "action5"]
        self.actionCombox.addItems(items)
        self.courseIconLabel.setFixedSize(160,160)
        self.actionCombox.setCurrentIndex(0)
        self.courseIconBtn.setMaximumWidth(120)
        self.submitBtn.setMaximumWidth(120)
        self.courseNameLineEdit.setMaximumWidth(120)

    def loadData(self):

        #TODO 整合所有的请求，封装到一个类中
        # 获取课程信息
        url = "http://localhost:8080/admin/course/reaction"
        # 获取课程图标

        # 获取课程视频
    def __initLayout(self):
        self.pointTable.setFixedWidth(600)
        self.videoWidget.setMinimumSize(800,600)
        self.topLayout.addWidget(self.videoWidget)
        self.topLayout.addWidget(self.pointTable)

        self.controlLayout.addWidget(self.openBtn)
        self.controlLayout.addWidget(self.playBtn)
        self.controlLayout.addWidget(self.slider)
        self.controlLayout.addWidget(self.timeLabel)

        # self.courseLayout.addWidget(self.courseIconBtn)
        self.courseLayout.addWidget(self.courseNameLineEdit)
        self.courseLayout.addWidget(self.courseIconBtn)
        self.courseLayout.addWidget(self.submitBtn)

        self.timeLayout.addWidget(self.startEdit)
        self.timeLayout.addWidget(self.getStartTimeBtn)
        self.timeLayout.addWidget(self.endEdit)
        self.timeLayout.addWidget(self.getEndTimeBtn)
        self.timeLayout.addWidget(self.addBtn)

        self.addLayout.addLayout(self.timeLayout)
        self.addLayout.addWidget(self.desTextEdit)
        # self.addLayout.

        self.bottomLayout.addWidget(self.courseIconLabel)
        self.bottomLayout.addLayout(self.courseLayout)
        self.bottomLayout.addLayout(self.addLayout)


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
    def openVideo(self):
        fileName, _ = QFileDialog.getOpenFileName(self, self.tr("Open Video"), "", "Video Files (*.mp4 *.flv *.ts *.mts *.avi *.wmv *.mov *.rmvb *.rm *.asf *.m4v *.mkv)")
        if fileName:
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.player.play()
            self.timer.start()
            self.videoPath = fileName

    def pauseVideo(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(FIF.PAUSE)
            self.player.pause()
        else:
            self.playBtn.setIcon(FIF.PLAY)
            self.player.play()
    
    def changeSlider(self, isDragging):
        self.sliderDragging = isDragging
    
    def updateTime(self):
        if not self.sliderDragging:
            current_time = self.player.position()
            duration = self.player.duration()
            self.slider.setValue(int(current_time/ (duration+0.01) * 1000))
            self.timeLabel.setText(f"""{self.formatTime(current_time // 1000)} / {self.formatTime(duration // 1000)}""")

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
        action = self.actionCombox.currentText()
        des = self.desTextEdit.toPlainText()
        if startTime >= endTime:
            self.showDialog(self.tr("Start time must be less than end time"))
            return
        # for i in range(len(self.info)):
        #     # TODO 防止时间区间重合
        #     if self.judgeTime(self.time2seconds(startTime),
        #                       self.time2seconds(endTime),
        #                       self.time2seconds(self.info[i][0]),
        #                       self.time2seconds(self.info[i][1])):
        #         self.showDialog(self.tr("The time is overlapped"))
                # return
        self.info.append([startTime, endTime, action, des])
        self.info.sort()
        self.showTable()
    
    def judgeTime(self, start1, end1, start2, end2):
        if (start1 > start2):
            start1, start2 = start2, start1
            end1, end2 = end2, end1
        return end1 < start2

    def time2seconds(self, timeString):
        minutes, seconds = map(int, timeString.split(':'))
        total_seconds = minutes * 60 + seconds
        return total_seconds

    def showTable(self):
        self.pointTable.setRowCount(len(self.info))
        for i in range(len(self.info)):
            button = PushButton(self.tr("Delete"))
            combox = ComboBox()
            combox.addItems(["action1", "action2", "action3", "action4", "action5"])
            combox.setCurrentIndex(self.actionDict[self.info[i][2]])

            button.clicked.connect(self.deleteInfo)
            self.pointTable.setItem(i, 0, QTableWidgetItem(self.info[i][0]))
            self.pointTable.setItem(i, 1, QTableWidgetItem(self.info[i][1]))
            self.pointTable.setCellWidget(i, 2, combox)
            self.pointTable.setItem(i, 3, QTableWidgetItem(self.info[i][3]))
            self.pointTable.setCellWidget(i, 4, button)

    def deleteInfo(self):
        button = self.sender()
        if button:
            index = self.pointTable.indexAt(button.pos())
            if index.isValid():
                self.info.pop(index.row())
                self.showTable()
        row = self.pointTable.currentRow()
        self.info.pop(row)
        self.showTable()

    def submit(self):
        # 上传课程封面
        url = "http://localhost:8981/admin/common/upload"
        headers = {"type": "img"}
        files = {'file', open(self.imgPath, 'rb')}
        try:
            response = requests.post(url, files=files, headers=headers)
            courseIcon = json.loads(response.text)["data"]
        except:
            self.showDialog(self.tr("Upload Image failed"))
        # 上传视频
        headers = {"type": "video"}
        files = {'file', open(self.videoPath, 'rb')}
        try:
            response = requests.post(url, files=files, headers=headers)
        except:
            self.showDialog(self.tr("Upload Video failed"))
        pass
    
    def getIcon(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 
                                                   "Open Image", 
                                                   "", 
                                                   "Image Files (*.png *.jpg *.jpeg)")
        
        if fileName:
            # 将图片设置为按钮的图标（这里假设你希望将图片作为按钮背景，如果是作为图标，则无需转换为QPixmap）
            pixmap = QPixmap(fileName).scaled(self.courseIconLabel.size(), 
                                               Qt.KeepAspectRatio, 
                                               Qt.SmoothTransformation)
            self.courseIconLabel.setPixmap(pixmap)
            self.imgPath = fileName


    def showDialog(self, msg):
        w = Dialog(self.tr("ERROR"), msg, self)
        w.setTitleBarVisible(False)
        w.exec()

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

    w = ReactionWindow()
    w.show()
    app.exec_()
