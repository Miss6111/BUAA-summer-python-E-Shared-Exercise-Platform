# 这是一个示例 Python 脚本。
import os.path

import Stu
# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import org1
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
import about
import list_window
from PyQt5 import QtCore, QtGui, QtWidgets


# define index_my_add 0
# define index_welcom 1
# define index_upload 2
# define index_search 3
# define index_my_norm 4


class admin_action():
    def create_group(self):  # 调出创建组页面
        orgUi.wgn.show()
        print('create group')

    def create_group_cancel(self):  # 创建组 cancel
        orgUi.groupname.setText('')
        orgUi.wgn.hide()
        print('create group cancel')

    def create_group_ok(self):  # 创建组 ok
        user = 'fmy'
        # if os.path.exists('temp'):
        #     with open('temp', "rt") as file:
        #         user = file.readline()
        print('user name find')
        gname = orgUi.groupname.text()
        # backend

        flag = Stu.create_new_group(gname, user)
        if flag:
            print('11')
            reply = QMessageBox.about(win, '创建小组', '创建成功')
            print('22')
        else:
            reply = QMessageBox.about(win, '创建小组', '创建失败，小组已经存在')
        orgUi.groupname.setText('')
        orgUi.wgn.hide()
        print('create group ok')

    def add_people_to_group(self): # 加入用户到组界面调出
        orgUi.waddp.show()
        print('add people to group')

    def chose_group(self):
        # itemlist = ['好好学习组','天天向上组']
        # for i in range(20):
        #     print(i)
        #     itemlist.append('1')
        # print(itemlist)
        itemlist = Stu.all_groups() #  backend
        group_list.setWindowTitle('小组')
        group_list.initializeList(itemlist)
        group_list.show()

    def confirm_glist(self):
        selected_items = group_list.list_widget.selectedItems()
        selected_names = [item.text() for item in selected_items]
        text = ''
        for i in selected_names:
            text = text + i + ' '
        orgUi.waddpgn.setText(text)
        group_list.close()


    def chose_people(self): # 调出选择用户界面
        text = orgUi.personname.text()
        # gname = orgUi.groupname_2.text()
        # orgUi.waddp.close()
        # self.wad = QtWidgets.QWidget(self.my_ad)
        # list_win.setWindowTitle('添加用户到组：' + gname)
        itemlist = ['小王', '小张']
        itemlist = Stu.search_students(1, text) # backend
        user_list.initializeList(itemlist)
        user_list.show()

    def confirm_userlist(self): #  确定用户
        selected_items = user_list.list_widget.selectedItems()
        selected_names = [item.text() for item in selected_items]
        QMessageBox.information(user_list, "选中的项", f"选中的项: {selected_names}")
        gname = orgUi.waddpgn.text()
        Stu.add_into_group(selected_names,gname) # todo backend
        user_list.close()


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QMainWindow()

    user_list = list_window.CheckableListWidget() # admin界面userlist
    user_list.hide()
    group_list = list_window.CheckableListWidget() # admin界面grouplist
    group_list.hide()

    orgUi = org1.Ui_MainWindow()
    orgUi.setupUi(win)
    orgUi.stackedWidget.setCurrentIndex(1)


    def change_widget_1():  # 上传问题
        orgUi.stackedWidget.setCurrentIndex(2)


    def change_widget_2():  # 搜索
        orgUi.stackedWidget.setCurrentIndex(3)


    def change_widget_3():  # 查看问题
        orgUi.stackedWidget.setCurrentIndex(5)


    def change_widget_4():  # 错误日志
        orgUi.stackedWidget.setCurrentIndex(6)


    def change_widget_5():  # 我的
        # todo 确定是用户还是管理员
        user = 'fmy'
        if os.path.exists('temp'):
            with open('temp', "rt") as file:
                user = file.readline()
        # flag = Stu.check_super()  # admin todo backend
        flag = True
        if flag:
            tp = '管理员'
            orgUi.stackedWidget.setCurrentIndex(0)
            orgUi.wgn.hide()  # widget group name
            orgUi.waddp.hide()  # widget add people to group
            orgUi.nhello2.setText(user)
            orgUi.ntp2.setText(tp)
        else:
            tp = '普通用户'
            orgUi.stackedWidget.setCurrentIndex(4)
            orgUi.nhello1.setText(user)
            orgUi.ntp1.setText(tp)


    def change_widget_6():  # 关于
        orgUi.stackedWidget.setCurrentIndex(1)


    def change_widget_7():  # 上传
        orgUi.textEdit.setText('')


    orgUi.pushButton.clicked.connect(change_widget_1)
    orgUi.pushButton_2.clicked.connect(change_widget_2)
    orgUi.pushButton_3.clicked.connect(change_widget_3)
    orgUi.pushButton_4.clicked.connect(change_widget_4)
    orgUi.pushButton_5.clicked.connect(change_widget_5)
    orgUi.pushButton_6.clicked.connect(change_widget_6)
    orgUi.pushButton_7.clicked.connect(change_widget_7)
    # my window admin
    orgUi.atg.clicked.connect(change_widget_2)
    orgUi.apb.clicked.connect(admin_action.add_people_to_group)
    orgUi.cgb.clicked.connect(admin_action.create_group)
    orgUi.wgn_cancel.clicked.connect(admin_action.create_group_cancel)
    orgUi.wgn_ok.clicked.connect(admin_action.create_group_ok)
    orgUi.waddpc.clicked.connect(orgUi.waddp.hide)
    orgUi.waddpsearch.clicked.connect(admin_action.chose_people)
    user_list.confirm_button.clicked.connect(admin_action.confirm_userlist)
    orgUi.waddpcg.clicked.connect(admin_action.chose_group)
    group_list.confirm_button.clicked.connect(admin_action.confirm_glist)


    win.show()
    sys.exit(app.exec_())
