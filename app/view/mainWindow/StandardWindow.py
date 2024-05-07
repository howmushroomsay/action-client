import json
import sys

import httpx
import numpy as np
from PyQt5.QtCore import Qt, QUrl, QTimer, QLocale
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QTableWidgetItem,
                             QFileDialog, QSizePolicy, QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from qfluentwidgets import (BodyLabel, PushButton, Slider, TableWidget,
                            )
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (ScrollArea, FluentTranslator,
                            LineEdit, TextEdit,
                            PrimaryPushButton, Dialog, PrimaryToolButton)

from app.net.admin import adminConfig


class SkeletonWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.conn = [(0, 1), (1, 2), (2, 3), (3, 7), (0, 4), (4, 5),
                     (5, 6), (6, 8), (9, 10), (11, 12), (11, 13),
                     (13, 15), (15, 17), (15, 19), (15, 21), (17, 19),
                     (12, 14), (14, 16), (16, 18), (16, 20), (16, 22),
                     (18, 20), (11, 23), (12, 24), (23, 24), (23, 25),
                     (24, 26), (25, 27), (26, 28), (27, 29), (28, 30),
                     (29, 31), (30, 32), (27, 31), (28, 32)]
        self.part = [[8, 6, 5, 4, 0, 1, 2, 3, 7], [10, 9],
                     [22, 16, 20, 18, 16, 14, 12, 11, 13, 15, 17, 19, 15, 21],
                     [12, 24, 26, 28, 32, 30, 28],
                     [11, 23, 25, 27, 31, 29, 27],
                     [24, 23]]

        self.__initFig()

    def __initFig(self):
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.layout().addWidget(self.canvas)
        self.ax = self.fig.add_subplot(projection='3d')

    def drawSkeleton(self, skeleton):
        self.ax.cla()
        self.ax.set_xlim3d([-2, 2])
        self.ax.set_ylim3d([-2, 2])
        self.ax.set_zlim3d([-1, 3])

        # self.ax.view_init(0, -90)

        x = 2 * skeleton[:, 0]
        y = -2 * skeleton[:, 1] + 0.5
        z = 2 * skeleton[:, 2]
        for part in self.part:
            x_plot = x[part]
            y_plot = y[part]
            z_plot = z[part]
            self.ax.plot(x_plot, y_plot, z_plot, color='b',
                         marker='o', markerfacecolor='r')
        self.canvas.draw()


class StandardWindow(ScrollArea):
    def __init__(self, parent=None, course_id=None):
        super().__init__()
        self.skeleton = None
        self.parent_ = parent
        self.setGeometry(100, 100, 1000, 600)
        self.courseId = course_id

        self.mainLayout = QVBoxLayout(self)
        self.topLayout = QHBoxLayout()
        self.sliderLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout()

        # topLayout
        self.videoWidget = QVideoWidget()
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.keyFrameTable = TableWidget()
        self.skeletonLayout = QVBoxLayout()
        self.skeletonWidget = SkeletonWidget()
        self.keyFrameDesTextEdit = TextEdit()
        self.addBtn = PrimaryPushButton(self.tr("Add KeyFrame"), self, FIF.ADD)

        # sliderLayout
        self.openBtn = PrimaryToolButton(FIF.FOLDER, self)
        self.playBtn = PrimaryToolButton(FIF.PLAY, self)
        self.slider = Slider(Qt.Horizontal)
        self.timeLabel = BodyLabel()

        # bottomLayout
        self.iconLayout = QVBoxLayout()
        self.courseIconLabel = BodyLabel()
        self.courseIconBtn = PrimaryPushButton(self.tr("Choose Icon"))
        self.importantSkeletonLabel = BodyLabel()
        self.infoLayout = QVBoxLayout()
        self.courseNameLayout = QHBoxLayout()
        self.courseNameLabel = BodyLabel(self.tr("Course Name :"))
        self.courseNameLineEdit = LineEdit()
        self.courseDesTextEdit = TextEdit()
        self.functionLayout = QHBoxLayout()
        self.generateBtn = PrimaryPushButton(self.tr("Generate Skeleton"))
        self.submitBtn = PrimaryPushButton(self.tr("Submit"))

        self.__initWidget()
        self.__initLayout()

        self.__connectSignalToSlot()

        self.sliderDragging = False

        self.videoPath = None
        self.iconPath = None
        self.needSkeleton = False

        self.keyFrame = []
        self.info = []

    def __initWidget(self):
        self.videoWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.player.setVideoOutput(self.videoWidget)

        self.slider.setRange(0, 1000)
        self.keyFrameTable.horizontalHeader().setVisible(True)
        self.keyFrameTable.horizontalHeader().setStretchLastSection(True)
        self.keyFrameTable.verticalHeader().setVisible(False)
        self.keyFrameTable.setColumnCount(3)
        self.keyFrameTable.setHorizontalHeaderLabels([self.tr("Time"),
                                                      self.tr("Description"),
                                                      self.tr("Ops")])

        self.courseIconLabel.setFixedSize(200, 200)
        self.importantSkeletonLabel.setFixedSize(200, 200)
        self.generateBtn.setMaximumWidth(200)
        self.submitBtn.setMaximumWidth(200)

        self.skeletonWidget.setMaximumWidth(300)
        self.keyFrameDesTextEdit.setMaximumSize(300, 50)
        self.keyFrameTable.setMaximumWidth(400)

    def __initLayout(self):
        self.skeletonLayout.addWidget(self.skeletonWidget)
        self.skeletonLayout.addWidget(self.keyFrameDesTextEdit)
        self.skeletonLayout.addWidget(self.addBtn)
        self.topLayout.addWidget(self.videoWidget)
        self.topLayout.addLayout(self.skeletonLayout)
        self.topLayout.addWidget(self.keyFrameTable)

        self.sliderLayout.addWidget(self.openBtn)
        self.sliderLayout.addWidget(self.playBtn)
        self.sliderLayout.addWidget(self.slider)
        self.sliderLayout.addWidget(self.timeLabel)

        self.iconLayout.addWidget(self.courseIconLabel)
        self.iconLayout.addWidget(self.courseIconBtn)
        self.bottomLayout.addLayout(self.iconLayout)
        self.bottomLayout.addWidget(self.importantSkeletonLabel)
        self.courseNameLayout.addWidget(self.courseNameLabel)
        self.courseNameLayout.addWidget(self.courseNameLineEdit)
        self.functionLayout.addWidget(self.generateBtn)
        self.functionLayout.addWidget(self.submitBtn)
        self.infoLayout.addLayout(self.courseNameLayout)
        self.infoLayout.addWidget(self.courseDesTextEdit)
        self.infoLayout.addLayout(self.functionLayout)
        self.bottomLayout.addLayout(self.infoLayout)

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.sliderLayout)
        self.mainLayout.addLayout(self.bottomLayout)

    def __connectSignalToSlot(self):
        self.addBtn.clicked.connect(self.addKeyFrame)
        self.openBtn.clicked.connect(self.openVideo)
        self.playBtn.clicked.connect(self.pauseVideo)

        self.slider.sliderPressed.connect(lambda: self.changeSlider(True))
        self.slider.sliderReleased.connect(lambda: self.changeSlider(False))

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTime)

        self.courseIconBtn.clicked.connect(self.getIcon)
        self.generateBtn.clicked.connect(self.generateSkeleton)
        self.submitBtn.clicked.connect(self.submit)

    def addKeyFrame(self):
        if self.videoPath is None:
            self.showDialog(self.tr("Please open video file first!"))
            return
        if self.needSkeleton:
            self.showDialog(self.tr("Please generate skeleton first!"))
            return
        current_time = self.player.position()
        duration = self.player.duration()
        current_frame = int(current_time / duration * self.skeleton.shape[0]) - 1
        print(current_frame, self.keyFrame)
        if current_frame not in self.keyFrame:
            self.keyFrame.append(current_frame)
            info = [self.formatTime(current_time // 1000) + ":{}".format(current_time % 1000),
                    self.keyFrameDesTextEdit.toPlainText(),
                    self.skeleton[current_frame]]
            self.info.append(info)
            self.keyFrame.sort()
            self.info.sort()
            self.showTable()

    def openVideo(self, clicked=False, fileName=None, flag=True):
        if fileName is None:
            fileName, _ = QFileDialog.getOpenFileName(self, self.tr("Open Video"),
                                                      "",
                                                      "Video Files (*.mp4 *.flv *.ts *.mts *.avi *.wmv *.mov *.rmvb "
                                                      "*.rm *.asf *.m4v *.mkv)")
        if fileName:
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.player.play()
            self.timer.start(100)
            if flag:
                self.videoPath = fileName
                self.needSkeleton = True

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
        if self.player.state() != QMediaPlayer.PlayingState:
            return
        current = self.player.position()
        duration = self.player.duration()
        if not self.sliderDragging:
            self.slider.setValue(int(current / (duration + 0.01) * 1000))
            self.timeLabel.setText(
                f"""{self.formatTime(current // 1000)} / {self.formatTime(duration // 1000)}""")

        if not self.needSkeleton:
            currentFrame = int(current / duration * self.skeleton.shape[0]) - 1
            self.skeletonWidget.drawSkeleton(self.skeleton[currentFrame])

    @staticmethod
    def formatTime(seconds):
        minutes = int(seconds) // 60
        seconds %= 60
        return f"{minutes:02}:{seconds:02}"

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

    def generateSkeleton(self):
        if self.videoPath is None:
            self.showDialog(self.tr("Please open video file first!"))
            return

        if not self.needSkeleton:
            self.showDialog(self.tr("You have already generated the skeleton"))
            return

        url = "http://192.168.3.137:8080/pose/video"
        files = {"file": open(self.videoPath, "rb")}
        response = httpx.post(url, files=files, timeout=None)
        skeleton = np.array(response.text.strip().split(" "), dtype=float)
        self.skeleton = skeleton.reshape((-1, 33, 4))
        self.needSkeleton = False

    def submit(self):
        courseName = self.courseNameLineEdit.text().strip()
        # 校验必填项
        if courseName == "":
            self.showDialog(self.tr("Course name is required"))
            return
        url = f"http://{adminConfig.host}:{adminConfig.port}/admin/common/upload"
        # 上传课程封面
        if self.iconPath is not None:

            headers = {"type": "thumbnail"}
            files = [('file', (self.iconPath, open(self.iconPath, 'rb'), 'image/png'))]
            try:
                response = httpx.post(url, files=files, headers=headers)
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
                response = httpx.post(url, files=files, headers=headers)
                self.videoPath = json.loads(response.text)["data"]
            except:
                self.showDialog(self.tr("Upload Video failed"))
                return
        else:
            if self.courseId is None:
                self.showDialog(self.tr("Please upload course video"))
                return

                # 上传骨架文件

        #上传课程信息
        url = f"http://{adminConfig.host}:{adminConfig.port}/admin/course/standard"
        keyFrame = []
        for i in range(len(self.info)):
            keyFrame.append({
                "time": self.keyFrame[i],
                "keyFrameDes": self.info[i][2],
                "skeleton": self.info[i][1],
            })
        data = {
            "id": self.courseId,
            "courseName": courseName,
            "courseDes": self.courseDesTextEdit.toPlainText(),
            "keyFrameList": keyFrame,
        }
        if self.videoPath is not None:
            data["videoPath"] = self.videoPath
        if self.iconPath is not None:
            data["icon"] = self.iconPath

        try:
            if self.courseId is not None:
                response = httpx.put(url, json=data)
            else:
                response = httpx.post(url, json=data)
            statusCode = json.loads(response.text)["code"]
            if statusCode != 1:
                self.showDialog(self.tr(json.loads(response.text)["msg"]))
                return
        except:
            self.showDialog(self.tr("Upload Info failed"))
            return

    def showTable(self):
        self.keyFrameTable.setRowCount(len(self.info))
        for i in range(len(self.info)):
            button = PushButton(self.tr("Delete"))
            button.clicked.connect(self.deleteKeyFrame)

            item = QTableWidgetItem(str(self.info[i][0]))
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.keyFrameTable.setItem(i, 0, item)
            item = QTableWidgetItem(str(self.info[i][1]))
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.keyFrameTable.setItem(i, 1, item)
            self.keyFrameTable.setCellWidget(i, 2, button)

    def deleteKeyFrame(self):
        # print(self.keyFrame)
        button = self.sender()
        if button:
            index = self.keyFrameTable.indexAt(button.pos())

            print(self.keyFrame, index.row())

            self.info.pop(index.row()+1)
            self.keyFrame.pop(index.row()+1)

            self.showTable()

    def showDialog(self, msg):
        w = Dialog(self.tr("ERROR"), msg, self)
        w.setTitleBarVisible(False)
        w.exec()

    def closeEvent(self, event):
        if self.parent_ is not None:
            self.parent_.fresh()
        event.accept()

    async def testSkeleton(self):

        import aiohttp
        url = "http://192.168.3.137:8080/pose/landmark"
        files = {'file': open(r'C:\Users\user\Desktop\test\pose-server\1.jpg', 'rb')}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, files=files) as resp:
                print("")
        async with httpx.AsyncClient() as client:
            response = await client.post(url, files=files)
            data = response.json()
            skeleton = data["landmarksWorld"]
            skeleton = np.array(skeleton)
            self.skeletonWidget.drawSkeleton(skeleton)
        print("hhh")


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

    w = StandardWindow(course_id=3)
    w.show()
    app.exec_()
