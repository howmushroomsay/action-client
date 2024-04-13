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
import yaml


class ReactionWindow(ScrollArea):
    def __init__(self, parent=None, courseId=None):
        super().__init__()
        self.setGeometry(100, 100, 1000, 600)
        self.courseId = courseId
        self.videoWidget = QVideoWidget()
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # controlLayout
        self.openBtn = PrimaryPushButton(self.tr("Open Video"))
        self.playBtn = PrimaryPushButton(self.tr("Play"),self,FIF.PLAY)
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
        self.actionDict = {
            "action1": 0,
            "action2": 1,
            "action3": 2,
            "action4": 3,
            "action5": 4,}
        self.icon = None
        self.videoPath = None 
        self.iconPath = None

        self.__initWidget()
        self.__initLayout()
        self.__connectSignalToSlot()
        self.initConfig()
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
        
        items = ["action1", "action2", "action3", "action4", "action5"]
        self.actionCombox.addItems(items)
        self.courseIconLabel.setFixedSize(160,160)
        self.actionCombox.setCurrentIndex(0)
        self.courseIconBtn.setMaximumWidth(200)
        self.submitBtn.setMaximumWidth(200)
        # self.courseNameLineEdit.setMaximumWidth(200)
        self.desTextEdit.setMaximumHeight(100)

    def initConfig(self):
        config = yaml.load(open('./app/config/ServerConfig.yaml', 'r'), 
                           Loader=yaml.FullLoader)
        self.host = config["server"]["host"]
        self.port = config["server"]["port"]
    def loadData(self):

        #TODO 整合所有的请求，封装到一个类中
        # 获取课程信息
        url = "http://{}:{}/admin/course/reaction/{}".format(self.host, self.port, self.courseId)
        try:
            response = requests.get(url)
            response = json.loads(response.text)
            if response["code"] == 0:
                self.showDialog(response["msg"])
                return
            data = response["data"]
        except:
            self.showDialog(self.tr("Server Error"))
            return
        self.courseId = data["id"]
        self.courseNameLineEdit.setText(data["courseName"])
        self.courseDesTextEdit.setText(data["courseDes"])
        
        # 获取课程图标
        url =  "http://{}:{}/admin/common/download/{}".format(self.host, self.port, data["icon"])
        # try:
        response = requests.get(url, headers={"type": "image"})
        # response_ = json.loads(response.text)
        # if response_["code"] == 0:
        #     self.showDialog(response_["msg"])
        #     return
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)
        pixmap = pixmap.scaled(self.courseIconLabel.size(), 
                                               Qt.KeepAspectRatio, 
                                               Qt.SmoothTransformation)
        self.courseIconLabel.setPixmap(pixmap)
        # except:
        #     self.showDialog(self.tr("Server Error"))
        #     return
        # 获取课程视频
    def __initLayout(self):
        self.pointTable.setFixedWidth(600)
        self.videoWidget.setMinimumSize(800,600)
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
        # TODO 拖动进度条
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
        for i in range(1,len(self.info)):
            if infocopy[i][1] <= infocopy[i-1][1] or infocopy[i-1][1] >= infocopy[i][0]:
                self.showDialog(self.tr("The time is overlapped"))
                self.info.pop(-1)
                return
        self.info = infocopy
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
        if self.iconPath is not None:
            url = "http://{}:{}/admin/common/upload".format(self.host, self.port)
            headers = {"type": "img"}
            files = [('file', (self.iconPath, open(self.iconPath, 'rb'), 'image/png'))]
            try:
                response = requests.post(url, files=files, headers=headers)
                courseIcon = json.loads(response.text)["data"]
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
                response = requests.post(url, files=files, headers=headers)
                videoPath = json.loads(response.text)["data"]
            except:
                self.showDialog(self.tr("Upload Video failed"))
                return
        else:
            if self.courseId is None:
                self.showDialog(self.tr("Please upload course video"))
                return    
        # 上传课程信息
        # 校验必填项
        courseName = self.courseNameLineEdit.text()
        if courseName == "":
            self.showDialog(self.tr("Course name is required"))
            return
        

        url = "http://{}:{}/admin/course/reaction".format(self.host, self.port)
        point = []
        for i in range(len(self.info)):
            point.append({
                "startTime": self.time2seconds(self.info[i][0]),
                "endTime": self.time2seconds(self.info[i][1]),
                "action": self.actionDict[self.info[i][2]],
                "pointDes": self.info[i][3],
                })
        data = {
            "id": self.courseId,
            "courseName": self.courseNameLineEdit.text(),
            "courseDes": self.courseDesTextEdit.toPlainText(),
            "videoPath": videoPath,
            "icon": courseIcon,
            "status": 1,
            "pointList": point,
        }
        url = "http://{}:{}/admin/course/reaction".format(self.host, self.port)
        try:
            if self.courseId is not None:
                response = requests.post(url, json=data)
            else:
                response = requests.put(url, json=data)
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
            # 将图片设置为按钮的图标（这里假设你希望将图片作为按钮背景，如果是作为图标，则无需转换为QPixmap）
            pixmap = QPixmap(fileName).scaled(self.courseIconLabel.size(), 
                                               Qt.KeepAspectRatio, 
                                               Qt.SmoothTransformation)
            self.courseIconLabel.setPixmap(pixmap)
            self.iconPath = fileName


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

    w = ReactionWindow(courseId=None)
    w.show()
    app.exec_()
