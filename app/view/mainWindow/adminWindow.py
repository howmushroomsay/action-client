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
from PyQt5.QtCore import Qt, QSize, QTranslator

from qfluentwidgets import (NavigationItemPosition, MSFluentWindow, SplashScreen, 
                            setThemeColor, NavigationBarPushButton, toggleTheme, 
                            setTheme, darkdetect, Theme, FluentWindow, 
                            FluentTranslator)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar, InfoBarPosition

from common.config import cfg
from common.icon import Icon
from common.signal_bus import signalBus
from common.translator import Translator
from app.common import resource_rc

from HomeInterface import HomeInterface
from UserManagerInterface import UserManagerInterface
from SettingInterface import SettingInterface
from CourseManagerInterface import CourseManagerInterface
class adminWindow(FluentWindow):

    def __init__(self, parent=None):
        super().__init__()
        self.parent_ = parent

        self.initWindow()


        self.homeInterface = HomeInterface(self)
        self.userManagerInterface = UserManagerInterface(self)
        self.settingInterface = SettingInterface(self)
        self.courseManagerInterface = CourseManagerInterface(self)

        self.navigationInterface.setAcrylicEnabled(True)
        # self.__connectSignalToSlot()
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
        self.setWindowTitle(self.tr("Admin Window"))
        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr("Home"))
        self.addSubInterface(self.userManagerInterface, FIF.PEOPLE, self.tr("User Management"))
        self.addSubInterface(self.courseManagerInterface, FIF.BOOK_SHELF,self.tr("Course Management"))
        self.navigationInterface.addWidget(
            'themeButton',
            NavigationBarPushButton(FIF.BRUSH, 'Theme', isSelectable=False),
            self.toggleTheme,
            NavigationItemPosition.BOTTOM)
        self.addSubInterface(
            self.settingInterface, FIF.SETTING, self.tr('Settings'))

    def toggleTheme(self):
        toggleTheme()

if __name__ == '__main__':
    # enable dpi scale
    # enable dpi scale
    if cfg.get(cfg.dpiScale) == "Auto":
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    else:
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # create application
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    # internationalization
    locale = cfg.get(cfg.language).value
    translator = FluentTranslator(locale)
    galleryTranslator = QTranslator()
    galleryTranslator.load(r'D:\project\python\action-client\app\resource\i18n\gallery.zh_CN.qm')
    # galleryTranslator.load(locale, "gallery", ".", ":/gallery/i18n")

    app.installTranslator(translator)
    app.installTranslator(galleryTranslator)

    # create main window
    w = adminWindow()
    w.show()

    app.exec_()
