import sys
import requests
import json
import yaml

from PyQt5.QtCore import Qt, QTranslator, QLocale
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from qframelesswindow import FramelessWindow, StandardTitleBar, AcrylicWindow
from qfluentwidgets import setThemeColor, FluentTranslator, Dialog, SplitTitleBar,FluentWindow
from .Ui_SignUPWindow import Ui_Form

class SignUpWindow(FluentWindow, Ui_Form):
    
    def __init__(self, parent=None):
        super().__init__()
        self.parentWindow = parent
        self.setupUi(self)
        # setTheme(Theme.DARK)
        setThemeColor('#28afe9')

        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()
        self.titleBar.maxBtn.disconnect()
        self.initConfig()
        self.initFun()
        self.setWindowTitle('用户注册')
        self.setWindowIcon(QIcon(":/images/logo.png"))
        self.setFixedSize(420, 450)

        items = ["男", "女"]
        self.sexComboBox.addItems(items)
        self.sexComboBox.setCurrentIndex(-1)

        

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def initFun(self):
        self.signUpBtn.clicked.connect(self.signUp)
        self.backBtn.clicked.connect(self.back)
    
    def initConfig(self):
        config = yaml.load(open('./app/config/ServerConfig.yaml', 'r'), Loader=yaml.FullLoader)
        self.host = config["server"]["host"]
        self.port = config["server"]["port"]
    def signUp(self):
        username = self.usernameLineEdit.text()
        name = self.nameLineEdit.text()
        phone = self.phoneLineEdit.text()
        sex = self.sexComboBox.currentText()
        idNumber = self.idNumberLineEdit.text()
        password1 = self.passwordLineEdit.text()
        password2 = self.passwordLineEdit_2.text()
        if username == "":
            self.usernameLineEdit.setPlaceholderText("请输入用户名")
        if name == "":
            self.nameLineEdit.setPlaceholderText("请输入昵称")
        if phone == "":
            self.phoneLineEdit.setPlaceholderText("请输入手机号")
        if idNumber == "":
            self.idNumberLineEdit.setPlaceholderText("请输入身份证号")
        if "" in [username, name, phone, idNumber]:
            return
        if password1 != password2:
            self.passwordLineEdit_2.clear()
            self.passwordLineEdit_2.setPlaceholderText("两次输入密码不一致")
            return
        
        url = "http://{}:{}/admin/usr".format(self.host, self.port)
        payload = json.dumps({
            "username": username,
            "name": name,
            "phone": phone,
            "sex": sex,
            "idNumber": idNumber
            })
        headers = {
            'Content-Type': 'application/json'
            }
        response = requests.post(url, data=payload, headers=headers)
        response = json.loads(response.text)
        if (response["code"] == 1):
            self.showDialog("注册成功")
        else:
            erroMsg = response["msg"]
            self.showDialog(erroMsg)

    def showDialog(self, msg):
        w = Dialog("", msg, self)

        # w.setTitleBarVisible(False)
        w.exec()     
    def back(self):
        self.close()
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

    w = SignUpWindow()
    w.show()
    app.exec_()
