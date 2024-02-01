import sys
import os
current_path = os.path.dirname(os.path.abspath(__file__))

# 添加上上级目录到sys.path
parent_path = os.path.abspath(os.path.join(current_path, '..'))
grandparent_path = os.path.abspath(os.path.join(parent_path, '..'))
sys.path.append(grandparent_path)
sys.path.append(os.path.abspath('.'))
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QSize

from qfluentwidgets import (NavigationItemPosition, MSFluentWindow, SplashScreen, 
                            setThemeColor, NavigationBarPushButton, toggleTheme, 
                            setTheme, darkdetect, Theme, FluentWindow)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar, InfoBarPosition

from .HomeInterface import HomeInterface
from .UserManagerInterface import UserManagerInterface
class adminWindow(MSFluentWindow):

    def __init__(self, parent=None):
        super().__init__()
        self.parent_ = parent
        setThemeColor('#28afe9')
        self.setMicaEffectEnabled(False)

        self.initWindow()

        self.homeInterface = HomeInterface(self)
        self.userManagerInterface = UserManagerInterface(self)
        self.initNavigation()
        self.splashScreen.finish()


    
    def initWindow(self):
        # 禁用最大化
        self.titleBar.maxBtn.setHidden(True)
        self.titleBar.maxBtn.setDisabled(True)
        self.titleBar.setDoubleClickEnabled(False)
        self.setResizeEnabled(False)

        self.resize(960, 700)
        self.setWindowIcon(QIcon(r'assets\logo\March7th.ico'))
        self.setWindowTitle(self.tr("管理员界面"))
        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(128, 128))
        self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr("主页"))
        self.addSubInterface(self.userManagerInterface, FIF.PEOPLE, self.tr("用户管理"))
        self.navigationInterface.addWidget(
            'themeButton',
            NavigationBarPushButton(FIF.BRUSH, '主题', isSelectable=False),
            self.toggleTheme,
            NavigationItemPosition.BOTTOM)


    def toggleTheme(self):
        toggleTheme()

if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    # Internationalization
    # translator = FluentTranslator(QLocale())
    # app.installTranslator(translator)

    w = adminWindow()
    w.show()
    app.exec_()
