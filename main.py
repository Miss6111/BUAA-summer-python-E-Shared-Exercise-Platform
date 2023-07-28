# 这是一个示例 Python 脚本。
import os.path

import Stu
# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import org1
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
import list_window, wrong_window
from PyQt5 import QtCore, QtGui, QtWidgets

# define index_my_add 0
# define index_welcom 1
# define index_upload 2
# define index_search 3
# define index_my_norm 4
from PyQt5.QtWidgets import QComboBox, QCheckBox

selection = ['0', '0', '0', '0']


def init_global():
    global selection
    selection = ['0', '0', '0', '0']


# 定义函数来修改全局变量
def modify_chapter(new):
    global selected_chapter
    selected_chapter = new


def modify_type(new):
    global selected_type
    selected_type = new


def modify_public(new):
    global selected_public
    selected_public = new


def modify_selection(i):
    global selection
    if selection[i] == '0':
        selection[i] = '1'
    else:
        selection[i] = '0'


def setA(s):
    global answerA
    answerA = s


def setB(s):
    global answerB
    answerB = s


def setC(s):
    global answerC
    answerC = s


def setD(s):
    global answerD
    answerD = s


class search_action():
    def search_for_group(self):  # 调出选择组界面
        user = 'fmy'
        # if os.path.exists('temp'):
        #     with open('temp', "rt") as file:
        #         user = file.readline()
        text = orgUi.groupline.text()
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
        QMessageBox.information(search_group_list, " ", f"加入成功")


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
        gname = orgUi.waddpgn.text()
        itemlist = Stu.search_students(gname, text)  # backend
        if len(itemlist) == 0:
            QMessageBox.information(user_list, "警告", f"没有不在此小组的用户或没有此用户")
        else:
            user_list.initializeList(itemlist)
            user_list.show()

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

        orgUi.answer_load_A.hide()
        orgUi.A_load.hide()
        orgUi.answer_load_B.hide()
        orgUi.B_load.hide()
        orgUi.answer_load_C.hide()
        orgUi.C_load.hide()
        orgUi.answer_load_D.hide()
        orgUi.D_load.hide()
        orgUi.answer_load.show()


    def change_widget_2():  # 搜索
        orgUi.stackedWidget.setCurrentIndex(3)
        orgUi.searchGroup.show()
        orgUi.groupline.show()
        orgUi.confirm_button.show()
        orgUi.pushButton_10.show()
        orgUi.label_type.hide()
        orgUi.label_key.hide()
        orgUi.label_chapter.hide()
        orgUi.lineEdit_chapter_2.hide()
        orgUi.lineEdit_key.hide()
        orgUi.lineEdit_type_2.hide()
        orgUi.pushButton_11.hide()
        orgUi.pushButton_12.hide()
        orgUi.widget_ques.hide()
        # orgUi.widget_btn.hide()
        # orgUi.widget_ques.hide()


    def change_widget_3():  # 查看问题
        orgUi.stackedWidget.setCurrentIndex(5)


    def change_widget_4():  # 错误日志
        # orgUi.stackedWidget.setCurrentIndex(6)
        wrong.show()


    def change_widget_5():  # 我的
        # todo 确定是用户还是管理员
        user = 'fmy'
        if os.path.exists('temp'):
            with open('temp', "rt") as file:
                user = file.readline()
        # flag = Stu.check_super()  # admin todo backend
        flag = False  # admin
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
            # orgUi.bg.setText()  # 获取当前人所在的组
            orgUi.ntp1.setText(tp)


    def change_widget_6():  # 关于
        orgUi.stackedWidget.setCurrentIndex(1)


    def change_widget_7():  # 上传

        user = 'fmy'
        if os.path.exists('temp'):
            with open('temp', "rt") as file:
                user = file.readline()
        title = orgUi.textEdit_title.toPlainText()
        if orgUi.type_choose.currentText() == "填空":
            type_l = 1
        else:
            type_l = 0

        if orgUi.public_choose.currentText() == "Yes":
            public = True
        else:
            public = False

        if type_l == 1:
            gap = orgUi.answer_load.text()
            Stu.load_one_question(title, "", orgUi.chapter_choose.currentText(), type_l, '', '', '', '', gap, public,
                                  user)
        else:
            Stu.load_one_question(title, ''.join(selection), orgUi.chapter_choose.currentText(), type_l,
                                  orgUi.answer_load_A.text(),
                                  orgUi.answer_load_B.text(),
                                  orgUi.answer_load_C.text(), orgUi.answer_load_D.text(), '', public, user)

        init_global()
        QMessageBox.about(win, '上传问题', '上传成功')


    def change_widget_9(self):  # 失效
        pass


    def change_widget_10():  # 搜索问题
        user = 'fmy'
        if os.path.exists('temp'):
            with open('temp', "rt") as file:
                user = file.readline()
        orgUi.pushButton_10.hide()
        orgUi.searchGroup.hide()
        orgUi.groupline.hide()
        orgUi.confirm_button.hide()
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
    # orgUi.pushButton_9.clicked.connect(change_widget_9)
    orgUi.pushButton_10.clicked.connect(change_widget_10)
    # # my window admin
    orgUi.atg.clicked.connect(change_widget_2)
    orgUi.apb.clicked.connect(admin_action.add_people_to_group)
    orgUi.cgb.clicked.connect(admin_action.create_group)
    orgUi.wgn_cancel.clicked.connect(admin_action.create_group_cancel)
    orgUi.wgn_ok.clicked.connect(admin_action.create_group_ok)
    orgUi.waddpc.clicked.connect(orgUi.waddp.hide)
    orgUi.waddpsearch.clicked.connect(admin_action.chose_people)
    orgUi.confirm_button.clicked.connect(search_action.search_for_group)
    user_list.confirm_button.clicked.connect(admin_action.confirm_userlist)
    search_group_list.confirm_button.clicked.connect(search_action.confirm_search_group_list)
    orgUi.waddpcg.clicked.connect(admin_action.chose_group)
    group_list.confirm_button.clicked.connect(admin_action.confirm_glist)

    def Modify_type():
        if orgUi.type_choose.currentText() == '填空':
            orgUi.answer_load_A.hide()
            orgUi.A_load.hide()
            orgUi.answer_load_B.hide()
            orgUi.B_load.hide()
            orgUi.answer_load_C.hide()
            orgUi.C_load.hide()
            orgUi.answer_load_D.hide()
            orgUi.D_load.hide()
            orgUi.answer_load.show()
        else:
            orgUi.answer_load_A.show()
            orgUi.A_load.show()
            orgUi.answer_load_B.show()
            orgUi.B_load.show()
            orgUi.answer_load_C.show()
            orgUi.C_load.show()
            orgUi.answer_load_D.show()
            orgUi.D_load.show()
            orgUi.answer_load.hide()

    orgUi.type_choose.currentIndexChanged.connect(Modify_type)


    def handleCheckboxA():
        modify_selection(0)


    def handleCheckboxB():
        modify_selection(1)


    def handleCheckboxC():
        modify_selection(2)


    def handleCheckboxD():
        modify_selection(3)


    orgUi.A_load.stateChanged.connect(handleCheckboxA)
    orgUi.B_load.stateChanged.connect(handleCheckboxB)
    orgUi.C_load.stateChanged.connect(handleCheckboxC)
    orgUi.D_load.stateChanged.connect(handleCheckboxD)

    win.show()
    sys.exit(app.exec_())
