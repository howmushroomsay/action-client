import json
import sys

import httpx
import yaml
from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import setThemeColor, FluentTranslator, SplitTitleBar, Dialog
from qframelesswindow import AcrylicWindow

from .SiguUpWindow import SignUpWindow
from .Ui_LoginWindow import Ui_Form
from ..mainWindow.AdminWindow import AdminWindow
from app.net.admin import adminConfig


class LoginWindow(AcrylicWindow, Ui_Form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        setThemeColor('#28afe9')

        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()

        self.setWindowTitle(self.tr('Action-Login'))
        self.setWindowIcon(QIcon(":/images/logo.png"))
        self.resize(1000, 650)

        self.windowEffect.setMicaEffect(self.winId(), isDarkMode=False)
        self.setStyleSheet("LoginWindow{background: rgba(242, 242, 242, 0.8)}")
        self.titleBar.titleLabel.setStyleSheet("""
            QLabel{
                background: transparent;
                font: 13px 'Segoe UI';
                padding: 0 4px;
                color: white
            }
        """)
        self.initConfig()
        self.initFun()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def initConfig(self):
        with open("./app/config/ClientConfig.yaml", 'r') as f:
            clientConfig = yaml.load(f, Loader=yaml.FullLoader)
        if clientConfig["login"]["isRememberedUsername"]:
            self.usernameCheckBox.setChecked(True)
            self.usernameLineEdit.setText(clientConfig["login"]["username"])
        if clientConfig["login"]["isRememberedPassword"]:
            self.passwordCheckBox.setChecked(True)
            self.passwordLineEdit.setText(clientConfig["login"]["password"])

    def initFun(self):
        self.signInBtn.clicked.connect(self.signIn)
        self.signUpBtn.clicked.connect(self.signUp)
        self.forgotPasswordBtn.clicked.connect(self.forgotPassword)

    def signIn(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        if username == "":
            self.usernameLineEdit.setPlaceholderText(self.tr("请输入用户名"))
            return
        if password == "":
            self.passwordLineEdit.setPlaceholderText(self.tr("请输入密码"))
            return
        url = f'http://{adminConfig.host}:{adminConfig.port}/admin/usr/login'
        response = httpx.post(url, json={"username": username, "password": password},
                              headers={"Content-Type": "application/json"})
        response = json.loads(response.text)
        # 登录成功，保存token，跳转进入下一界面
        if response["code"] == 1:
            token = response["data"]["token"]
            with open('./app/config/ClientConfig.yaml', 'r') as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
                config["user"]["token"] = token
            with open('./app/config/ClientConfig.yaml', 'w') as f:
                yaml.dump(config, f)
            self.hide()
            if response["data"]["id"] == 0:
                # 管理员账户，进入管理端
                adminWin = AdminWindow(self)
                adminWin.show()
        else:
            errorMsg = response["msg"]
            self.showDialog(errorMsg)

    def showDialog(self, msg):
        title = self.tr('错误')
        w = Dialog(title, msg, self)
        w.setTitleBarVisible(False)
        w.exec()

    def signUp(self):
        signUpWindow = SignUpWindow(self)
        signUpWindow.show()
        # self.hide()

    def forgotPassword(self):
        pass

    def resizeEvent(self, e):
        super().resizeEvent(e)
        pixmap = QPixmap(":/images/background.jpg").scaled(
            self.label.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)


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

    window = LoginWindow()
    window.show()
    app.exec_()
