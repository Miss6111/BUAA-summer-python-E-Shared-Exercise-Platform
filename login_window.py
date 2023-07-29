import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from sqlalchemy import create_engine
import login_widget
import os
import Stu
from PyQt5.QtWidgets import *
name = ''

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
        # backend
        # flag = True
        flag = Stu.login(username, password)
        # 保存用户名到临时文件里
        if flag:
            self.close()
            with open('temp', 'wt') as file:
                file.write(username)
            with open('pass', 'wt') as file:
                file.write(password)
            os.system("python ./main.py")
        else:
            reply = QMessageBox.about(self, '登录', '账号或密码错误')
        print("login clicked")

    def sign_up(self):
        # 注册功能
        username = self.loginUi.lineEdit_3.text()
        password = self.loginUi.lineEdit_4.text()
        confirm_pass = self.loginUi.lineEdit_5.text()
        flag = 0
        # 0 成功
        # 1 两次密码不相等
        # 2 密码长度不符合要求（6-10）
        # 3 用户名长度不符合要求(>3)
        # 4 用户名已存在
        if confirm_pass != password:
            flag = 1
        if len(password) < 6 or len(password) > 10:
            flag = 2
        if len(username) < 3:
            flag = 3
        if flag == 0:
            flag2 = Stu.create_new_user(username, password, 0)
            print(flag2)
            if not flag2:
                    flag = 4
                    print(flag)
        if flag == 0:
            print('success')
            reply = QMessageBox.about(self, '注册', '注册成功,跳转到登录界面')
            self.change_widget2()
        elif flag == 1:
            print('fail')
            reply = QMessageBox.about(self, '注册', '两次输入的密码不同，请重新注册')
            self.loginUi.lineEdit_4.setText('')
            self.loginUi.lineEdit_5.setText('')
        elif flag == 2:
            print('fail')
            reply = QMessageBox.about(self, '注册', '密码长度不符合要求，请重新注册')
            self.loginUi.lineEdit_4.setText('')
            self.loginUi.lineEdit_5.setText('')
        elif flag == 3:
            reply = QMessageBox.about(self, '注册', '用户名长度不符合要求，请重新注册')
            self.loginUi.lineEdit_3.setText('')
            self.loginUi.lineEdit_4.setText('')
            self.loginUi.lineEdit_5.setText('')
        elif flag == 4:
            print('error 4')
            reply = QMessageBox.about(self, '注册', '该用户名已存在,请重新注册')
            # self.loginUi.lineEdit_3.setText('')
            # self.loginUi.lineEdit_4.setText('')
            # self.loginUi.lineEdit_5.setText('')
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
    # Stu.drop_and_create() 清空表
    app = QApplication(sys.argv)
    window = LoginWindow()
    sys.exit(app.exec_())
