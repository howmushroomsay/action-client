import sys
import yaml
import json
import requests

from PyQt5.QtCore import Qt, QTranslator, QLocale
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication
from qframelesswindow import FramelessWindow, StandardTitleBar, AcrylicWindow
from .Ui_LoginWindow import Ui_Form
from qfluentwidgets import setThemeColor, FluentTranslator, setTheme, Theme, SplitTitleBar, Dialog

from .SiguUpWindow import SignUpWindow

class LoginWindow(AcrylicWindow, Ui_Form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # setTheme(Theme.DARK)
        setThemeColor('#28afe9')

        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()

        # self.label.setScaledContents(False)
        self.setWindowTitle('Action-Login')
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
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def initConfig(self):
        config = yaml.load(open('./app/config/ServerConfig.yaml', 'r'), 
                           Loader=yaml.FullLoader)
        self.host = config["server"]["host"]
        self.port = config["server"]["port"]
        config = yaml.load(open('./app/config/ClientConfig.yaml', 'r'), 
                           Loader=yaml.FullLoader)
        if (config["login"]["isRememberedUsername"]):
            self.usernameCheckBox.setChecked(True)
            self.usernameLineEdit.setText(config["login"]["username"])
        if (config["login"]["isRememberedPassword"]):
            self.passwordCheckBox.setChecked(True)
            self.passwordLineEdit.setText(config["login"]["password"])
    def initFun(self):
        self.signInBtn.clicked.connect(self.signIn)
        self.signUpBtn.clicked.connect(self.signUp)
        # self.forgotPasswordBtn.clicked.connect(self.forgotPassword)
    
    def signIn(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        if username == "":
            self.usernameLineEdit.setPlaceholderText("请输入用户名")
            return
        if password == "":
            self.passwordLineEdit.setPlaceholderText("请输入密码")
            return
        url = "http://{}:{}/admin/usr/login".format(self.host, self.port)
        payload = json.dumps({"username": username, "password": password})
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data=payload, headers=headers)
        response = json.loads(response.text)
        # 登录成功，保存token，跳转进入下一界面
        if (response["code"] == 1):
            token = response["data"]["token"]
            with open('./app/config/ClientConfig.yaml','r') as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
                config["user"]["token"] = token
                # yaml.(mapping=2, sequence=4, offset=2)  
            with open('./app/config/ClientConfig.yaml','w') as f:                
                yaml.dump(config, f)
            if response["data"]["id"] == 0:
                # 管理员账户，进入管理端
                adminWindow = adminWindow(self)
                adminWindow.show()
                self.hide()
            else:
                userWindow = userWindow(self)
                userWindow.show()
                self.hide()
            
        else:
            errorMsg = response["msg"]
            self.showDialog(errorMsg)
    
    def showDialog(self, msg):
        title = '错误'
        w = Dialog(title, msg, self)
        w.setTitleBarVisible(False)
        w.exec()
  
    def signUp(self):
        signUpWindow = SignUpWindow(self)
        signUpWindow.show() 
        # self.hide()

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

    w = LoginWindow()
    w.show()
    app.exec_()
