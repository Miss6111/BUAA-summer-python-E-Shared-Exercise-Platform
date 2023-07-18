import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from sqlalchemy import create_engine
import login_widget
import about
import os
import Stu
from PyQt5.QtWidgets import *


class LoginWindow(QWidget):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.loginUi = login_widget.Ui_Form()
        self.loginUi.setupUi(self)
        self.loginUi.widget_3.hide()
        self.loginUi.pushButton_3.clicked.connect(self.login)
        self.loginUi.pushButton_5.clicked.connect(self.sign_up)
        self.loginUi.pushButton.clicked.connect(self.change_widget2)
        self.loginUi.pushButton_2.clicked.connect(self.change_widget_3)
        self.show()

    def login(self):
        # 登录
        username = self.loginUi.lineEdit.text()
        password = self.loginUi.lineEdit_2.text()
        # todo:find in database jump if success
        flag = True
        if flag:
            self.close()
            os.system("python ./about_window.py")
        else:
            reply = QMessageBox.about(self, '登录', '账号或密码错误')
        print("login clicked")

    def sign_up(self):
        # 注册功能
        username = self.loginUi.lineEdit_3.text()
        password = self.loginUi.lineEdit_4.text()
        confirm_pass = self.loginUi.lineEdit_5.text()
        flag = False
        if confirm_pass == password:
            # todo:Stu.create_new_user(username, password, 0)
            flag = True
        if flag:
            print('success')
            reply = QMessageBox.about(self, '注册', '注册成功,跳转到登录界面')
            self.change_widget2()
        else:
            print('fail')
            reply = QMessageBox.about(self, '注册', '两次输入的密码不同，请重新注册')
            self.loginUi.lineEdit_4.setText('')
            self.loginUi.lineEdit_5.setText('')
        print("sign up clicked")

    def change_widget_3(self):
        self.loginUi.widget_2.hide()
        self.loginUi.lineEdit_3.setText('')
        self.loginUi.lineEdit_4.setText('')
        self.loginUi.lineEdit_5.setText('')
        self.loginUi.widget_3.show()

    def change_widget2(self):
        self.loginUi.widget_3.hide()
        self.loginUi.lineEdit.setText('')
        self.loginUi.lineEdit_2.setText('')
        self.loginUi.widget_2.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    sys.exit(app.exec_())
