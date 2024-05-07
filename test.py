import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSlider, QLabel, QFileDialog, QHBoxLayout, QSizePolicy
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 600, 400)

        # Video display
        self.videoWidget = QVideoWidget()
        # self.videoWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Play button
        self.playButton = QPushButton("Play")
        self.playButton.clicked.connect(self.playClicked)

        # Pause button
        self.pauseButton = QPushButton("Pause")
        self.pauseButton.clicked.connect(self.pauseClicked)

        # Stop button
        self.stopButton = QPushButton("Stop")
        self.stopButton.clicked.connect(self.stopClicked)

        # Select file button
        self.selectButton = QPushButton("Select File")
        self.selectButton.clicked.connect(self.selectFile)

        # Progress slider
        self.progressSlider = QSlider(Qt.Horizontal)
        self.progressSlider.setRange(0, 0)
        self.progressSlider.sliderMoved.connect(self.setPosition)

        # Layout
        controlLayout = QHBoxLayout()
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.pauseButton)
        controlLayout.addWidget(self.stopButton)
        controlLayout.addWidget(self.selectButton)

        layout = QVBoxLayout()
        layout.addWidget(self.videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.progressSlider)

        self.setLayout(layout)

        self.mediaPlayer.setVideoOutput(self.videoWidget)

    def playClicked(self):
        self.mediaPlayer.play()

    def pauseClicked(self):
        self.mediaPlayer.pause()

    def stopClicked(self):
        self.mediaPlayer.stop()

    def selectFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Video")
        if fileName != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.mediaPlayer.play()
            self.progressSlider.setRange(0, int(self.mediaPlayer.duration() / 1000))

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position * 1000)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoPlayer()
    window.show()
    sys.exit(app.exec_())
