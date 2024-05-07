import sys

from PyQt5.QtCore import Qt, QTranslator
from PyQt5.QtWidgets import QApplication

from view.login.LoginWindow import LoginWindow

if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    # Internationalization
    translator = QTranslator()
    translator.load(f'app/view/login/test_cn.qm')
    app.installTranslator(translator)

    w = LoginWindow()
    w.show()
    app.exec_()
