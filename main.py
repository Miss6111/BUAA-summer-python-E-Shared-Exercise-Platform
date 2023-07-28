# 这是一个示例 Python 脚本。
import os.path

import Stu
# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import org1
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
import about
import list_window, wrong_window
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

    def add_people_to_group(self):  # 加入用户到组界面调出
        orgUi.waddp.show()
        print('add people to group')

    def chose_group(self):
        # itemlist = ['好好学习组','天天向上组']
        # for i in range(20):
        #     print(i)
        #     itemlist.append('1')
        # print(itemlist)
        print('chose group1')
        itemlist = Stu.all_groups()  # backend
        print('chose group2')
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

    def chose_people(self):  # 调出选择用户界面
        text = orgUi.personname.text()
        # gname = orgUi.groupname_2.text()
        # orgUi.waddp.close()
        # self.wad = QtWidgets.QWidget(self.my_ad)
        # list_win.setWindowTitle('添加用户到组：' + gname)
        itemlist = ['小王', '小张']
        itemlist = Stu.search_students(1, text)  # backend
        user_list.initializeList(itemlist)
        user_list.show()

    def search_for_group(self):  # 调出选择组界面
        user = 'fmy'
        if os.path.exists('temp'):
            with open('temp', "rt") as file:
                user = file.readline()
        text = orgUi.search_group_name.text()
        itemlist = Stu.search_for_groups(text, user)
        if len(itemlist) == 0:
            QMessageBox.information(search_group_list, "警告", f"您已加入当前小组或没有当前小组")
        else:
            search_group_list.initializeList(itemlist)
            search_group_list.show()

    def confirm_search_group_list(self):  # 确定搜索组
        if os.path.exists('temp'):
            with open('temp', "rt") as file:
                user = file.readline()
        selected_items = search_group_list.list_widget.selectedItems()
        selected_names = [item.text() for item in selected_items]
        QMessageBox.information(search_group_list, "选中的项", f"选中的项: {selected_names}")
        Stu.user_add_into_group(selected_names, user)
        search_group_list.close()

    def confirm_userlist(self):  # 确定用户
        selected_items = user_list.list_widget.selectedItems()
        selected_names = [item.text() for item in selected_items]
        QMessageBox.information(user_list, "选中的项", f"选中的项: {selected_names}")
        gname = orgUi.waddpgn.text()
        Stu.add_into_group(selected_names, gname)  # todo backend
        user_list.close()


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QMainWindow()

    wrong = wrong_window.WrongWindow()
    wrong.hide()
    user_list = list_window.CheckableListWidget()  # admin界面userlist
    user_list.hide()
    group_list = list_window.CheckableListWidget()  # admin界面grouplist
    group_list.hide()
    search_group_list = list_window.CheckableListWidget()
    search_group_list.hide()

    orgUi = org1.Ui_MainWindow()
    orgUi.setupUi(win)
    orgUi.stackedWidget.setCurrentIndex(1)
    page = 1


    def change_widget_1():  # 上传问题
        orgUi.stackedWidget.setCurrentIndex(2)


    def change_widget_2():  # 搜索
        orgUi.stackedWidget.setCurrentIndex(3)
        orgUi.label_type.hide()
        orgUi.label_key.hide()
        orgUi.label_chapter.hide()
        orgUi.lineEdit_chapter_2.hide()
        orgUi.lineEdit_key.hide()
        orgUi.lineEdit_type_2.hide()
        orgUi.pushButton_11.hide()
        orgUi.pushButton_12.hide()
        orgUi.widget_btn.hide()
        orgUi.widget_ques.hide()


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
        flag = True  # admin
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
        org1.init_global()
        user = 'fmy'
        if os.path.exists('temp'):
            with open('temp', "rt") as file:
                user = file.readline()
        title = orgUi.textEdit_title.toPlainText()
        chapter = org1.selected_chapter
        if org1.selected_type == "填空":
            type_l = 1
        else:
            type_l = 0

        if org1.selected_public == "yes":
            public = True
        else:
            public = False

        if type_l == 1:
            gap = orgUi.lineEdit_answer.text()
            Stu.load_one_question(title, "", chapter, type_l, '', '', '', '', gap, public, user)
        else:
            Stu.load_one_question(title, ''.join(org1.selection), chapter, type_l, org1.answerA, org1.answerB,
                                  org1.answerC, org1.answerD, '', public, user)

        print('cuesss')
        QMessageBox.about(win, '上传问题', '上传成功')


    def change_widget_9(self):  # 搜索组

        page = 1
        orgUi.pushButton_9.hide()

        orgUi.pushButton_10.hide()
        orgUi.pushButton_11.show()
        orgUi.widget_btn.show()
        # orgUi.pushButton_11.clicked.connect(change_widget_11)
        # orgUi.pushButton_11.clicked.connect(change_widget_11)
        print("enx")
        group = Stu.search_groups(page)
        print(group)
        orgUi.button0.setText(group[0])
        orgUi.button0.clicked.connect(lambda: change_widget_btn(group[0]))
        orgUi.button1.setText(group[1])
        orgUi.button1.clicked.connect(lambda: change_widget_btn(group[1]))
        orgUi.button2.setText(group[2])
        orgUi.button2.clicked.connect(lambda: change_widget_btn(group[2]))


    def change_widget_10():  # 搜索问题
        user = 'fmy'
        if os.path.exists('temp'):
            with open('temp', "rt") as file:
                user = file.readline()
        print(user)
        orgUi.pushButton_9.hide()
        orgUi.label_type.show()
        orgUi.label_key.show()
        orgUi.label_chapter.show()
        orgUi.lineEdit_chapter_2.show()
        orgUi.lineEdit_key.show()
        orgUi.lineEdit_type_2.show()
        orgUi.pushButton_12.show()
        ques_name = orgUi.lineEdit_key.text()
        chapters_name = orgUi.lineEdit_chapter_2.text()
        mytype = orgUi.lineEdit_type_2.text()
        orgUi.pushButton_12.clicked.connect(lambda: change_widget_12(ques_name, chapters_name, mytype, user))


    def change_widget_12(ques_name, chapters_name, mytype, user):  # 搜索
        q = []
        q = Stu.scope_questions(ques_name, chapters_name, mytype, user)
        orgUi.question0.setText(q[0])

        orgUi.question0.clicked.connect(lambda: change_widget_q(q[0]))
        orgUi.question1.setText(q[1])
        orgUi.question1.clicked.connect(lambda: change_widget_q(q[1]))
        orgUi.question2.setText(q[2])
        orgUi.question2.clicked.connect(lambda: change_widget_q(q[2]))
        orgUi.question3.setText(q[3])
        orgUi.question3.clicked.connect(lambda: change_widget_q(q[3]))


    def change_widget_q(text, answer, mytype):
        orgUi.stackedWidget.setCurrentIndex(5)
        if (mytype == 1):
            orgUi.page_2.show()
            orgUi.page.hide()
            orgUi.page_3.hide()
            orgUi.textBrowser_3.setText(text)
            given = orgUi.answer1.text()
            orgUi.submit.clicked.connect(lambda: change_widget_submit(given))
        else:
            orgUi.page.show()
            orgUi.page_2.hide()
            orgUi.page_3.hide()
            orgUi.textBrowser_2.setText(text)


    def change_widget_submit(given):  # 按下按钮
        orgUi.label_5.setText(given)


    def change_widget_star(given):
        orgUi.label_5.setText(given)


    def change_widget_star2(given):
        orgUi.label_5.setText(given)


    def change_widget_btn(text):  # 按下按钮
        user = 'fmy'
        if os.path.exists('temp'):
            with open('temp', "rt") as file:
                user = file.readline()
        Stu.user_add_into_group(text, user)


    def create_group():
        orgUi.wgn.show()
        print('create group')


    def create_group_cancel():
        orgUi.groupname.setText('')
        orgUi.wgn.hide()
        print('create group cancel')


    def create_group_ok():
        gname = orgUi.groupname.text()
        # backend
        Stu.creat_new_group(gname)

        orgUi.groupname.setText('')
        orgUi.wgn.hide()
        print('create group ok')


    def add_people_to_group():
        orgUi.waddp.show()
        print('add people to group')


    orgUi.pushButton.clicked.connect(change_widget_1)
    orgUi.pushButton_2.clicked.connect(change_widget_2)
    orgUi.pushButton_3.clicked.connect(change_widget_3)
    orgUi.pushButton_4.clicked.connect(change_widget_4)
    orgUi.pushButton_5.clicked.connect(change_widget_5)
    orgUi.pushButton_6.clicked.connect(change_widget_6)
    orgUi.pushButton_7.clicked.connect(change_widget_7)
    orgUi.pushButton_9.clicked.connect(change_widget_9)
    orgUi.pushButton_10.clicked.connect(change_widget_10)
    # my window admin
    orgUi.atg.clicked.connect(change_widget_2)
    orgUi.apb.clicked.connect(admin_action.add_people_to_group)
    orgUi.cgb.clicked.connect(admin_action.create_group)
    orgUi.wgn_cancel.clicked.connect(admin_action.create_group_cancel)
    orgUi.wgn_ok.clicked.connect(admin_action.create_group_ok)
    orgUi.waddpc.clicked.connect(orgUi.waddp.hide)
    orgUi.waddpsearch.clicked.connect(admin_action.chose_people)
    orgUi.searchicon.clicked.connect(admin_action.search_for_group)
    user_list.confirm_button.clicked.connect(admin_action.confirm_userlist)
    search_group_list.confirm_button.clicked.connect(admin_action.confirm_search_group_list)
    orgUi.waddpcg.clicked.connect(admin_action.chose_group)
    group_list.confirm_button.clicked.connect(admin_action.confirm_glist)

    win.show()
    sys.exit(app.exec_())
