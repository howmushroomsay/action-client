# coding:utf-8
import sys
import os

# 获取当前脚本所在路径
current_path = os.path.dirname(os.path.abspath(__file__))

# 添加上上级目录到sys.path
parent_path = os.path.abspath(os.path.join(current_path, '..'))
grandparent_path = os.path.abspath(os.path.join(parent_path, '..'))
sys.path.append(grandparent_path)

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QPainterPath, QImage
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QGraphicsDropShadowEffect

from qfluentwidgets import ScrollArea, FluentIcon
from common.style_sheet import StyleSheet

class HomeInterface(ScrollArea):
    """ Home Interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        
        self.initWidget()
        self.loadSamples()
        
    def initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('homeInterface')
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(40)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

    def loadSamples(self):
        """ Load samples """
        self.vBoxLayout.addWidget(QLabel('Home Interface'))
        img = QImage(r"app\resource\images\image1.png")
        label = QLabel()
        img = QPixmap.fromImage(img).scaled(600, 400, Qt.KeepAspectRatio)
        label.setPixmap(img)
        self.vBoxLayout.addWidget(label)