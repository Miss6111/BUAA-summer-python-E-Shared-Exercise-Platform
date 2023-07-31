# 这是一个示例 Python 脚本。
import os.path
from functools import partial

import upload_file
import Stu
import Graph
# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import org1
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QInputDialog, QFileDialog, QListWidget, \
    QListWidgetItem, QPushButton
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


def modify_selection(i):
    global selection
    if selection[i] == '0':
        selection[i] = '1'
    else:
        selection[i] = '0'


class norm_action():
    def change_password(self):
        text, ok = QInputDialog.getText(win, '改密码', '请输入原密码:')
        if ok:
            if text == password:
                text2, ok2 = QInputDialog.getText(win, '改密码', '请输入新密码:')
                Stu.change_password(text2, user)
            else:
                reply = QMessageBox.about(win, '改密码', '原密码错误')

    def change_motto(self):
        text, ok = QInputDialog.getText(win, '改个人简介', '请输入新的个人简介:')
        if ok:
            Stu.change_quote(text, user)
            orgUi.label_motto.setText(text)


class search_action():
    def search_for_group(self):  # 调出选择组界面
        text = orgUi.groupline.text()
        itemlist = Stu.search_for_groups(text, user)
        if len(itemlist) == 0:
            QMessageBox.information(search_group_list, "警告", f"您已加入当前小组或没有当前小组")
        else:
            search_group_list.initializeList(itemlist)
            search_group_list.show()

    def confirm_search_group_list(self):  # 确定搜索组
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
        gname = orgUi.groupname.text()
        # backend

        flag = Stu.create_new_group(gname, user)
        if flag:
            QMessageBox.about(win, '创建小组', '创建成功')
        else:
            QMessageBox.about(win, '创建小组', '创建失败，小组已经存在')
        orgUi.groupname.setText('')
        orgUi.wgn.hide()
        print('create group ok')

    def add_people_to_group(self):  # 加入用户到组界面调出
        orgUi.waddp.show()
        print('add people to group')

    def chose_group(self):

        itemlist = Stu.all_groups()  # backend
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

    def upload(self):
        window = upload_file.MainWindow()
        path = window.getPath()
        Stu.load_files(path, user)


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
    search_question_list = list_window.CheckableListWidget()
    search_question_list.hide()

    orgUi = org1.Ui_MainWindow()
    orgUi.setupUi(win)
    orgUi.load.hide()
    orgUi.load_2.hide()
    orgUi.comment.show()
    orgUi.comment_2.show()
    orgUi.textEdit_comment.hide()
    orgUi.textEdit_comment_2.hide()
    orgUi.scrollArea2.hide()
    orgUi.scrollArea3.hide()
    orgUi.scrollArea4.hide()
    orgUi.scrollArea5.hide()
    orgUi.scrollArea2_3.hide()
    orgUi.scrollArea3_3.hide()
    orgUi.scrollArea4_3.hide()
    orgUi.scrollArea5_3.hide()
    orgUi.scrollArea.hide()
    orgUi.scrollArea_3.hide()
    orgUi.stackedWidget.setCurrentIndex(1)

    page = 1

    user = 'manager'
    password = ""
    if os.path.exists('temp'):
        with open('temp', "rt") as file:
            user = file.readline()
    if os.path.exists('pass'):
        with open('pass', "rt") as file:
            password = file.readline()

    orgUi.label_motto.setText(Stu.getMotto(user))
    orgUi.password_change.clicked.connect(norm_action.change_password)
    orgUi.motto_change.clicked.connect(norm_action.change_motto)


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
        qgroups = Stu.search_qgroups(user)
        orgUi.lineEdit_type_4.clear()
        orgUi.lineEdit_type_4.addItem("全部")
        for i in range(len(qgroups)):
            orgUi.lineEdit_type_4.addItem(qgroups[i])
        # orgUi.widget_btn.hide()
        # orgUi.widget_ques.hide()


    def change_widget_3():  # 查看问题
        orgUi.stackedWidget.setCurrentIndex(5)

        orgUi.load.hide()
        orgUi.load_2.hide()
        orgUi.comment.show()
        orgUi.comment_2.show()
        orgUi.textEdit_comment.hide()
        orgUi.textEdit_comment_2.hide()
        orgUi.scrollArea2.hide()
        orgUi.scrollArea3.hide()
        orgUi.scrollArea4.hide()
        orgUi.scrollArea5.hide()
        orgUi.scrollArea2_3.hide()
        orgUi.scrollArea3_3.hide()
        orgUi.scrollArea4_3.hide()
        orgUi.scrollArea5_3.hide()
        orgUi.scrollArea.hide()
        orgUi.scrollArea_3.hide()
        lis = Stu.get_question(1)
        t = str(1)
        print(t)
        orgUi.label_2.setText(t)
        change_widget_q(lis[0], lis[2], lis[1], 1, 0)


    def change_widget_4():  # 错误日志
        # orgUi.stackedWidget.setCurrentIndex(6)
        wrong.show()


    def change_widget_5():  # 我的
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


    def change_widget_10():  # 搜索问题
        orgUi.pushButton_10.hide()
        orgUi.searchGroup.hide()
        orgUi.groupline.hide()
        orgUi.confirm_button.hide()
        orgUi.label_type.show()
        orgUi.label_key.show()
        orgUi.label_chapter.show()
        orgUi.label_26.show()
        orgUi.lineEdit_chapter_2.show()
        orgUi.lineEdit_key.show()
        orgUi.lineEdit_type_2.show()
        orgUi.lineEdit_type_4.show()
        orgUi.pushButton_12.show()
        orgUi.pushButton_12.clicked.connect(lambda: change_widget_12())


    def change_widget_12():  # 搜索按键ques_name,chapters_name,mytype,user
        ques_name = orgUi.lineEdit_key.text()
        chapters_name = orgUi.lineEdit_chapter_2.currentText()
        mytype = orgUi.lineEdit_type_2.currentText()
        range = orgUi.lineEdit_type_4.currentText()
        x = 0
        if mytype == '填空':
            x = 1
        else:
            x = 0
        lis = [ques_name, chapters_name, x, user]
        orgUi.widget_ques.show()
        orgUi.label_type.hide()
        orgUi.label_key.hide()
        orgUi.label_chapter.hide()
        orgUi.label_26.hide()
        orgUi.lineEdit_chapter_2.hide()
        orgUi.lineEdit_key.hide()
        orgUi.lineEdit_type_2.hide()
        orgUi.lineEdit_type_4.hide()
        orgUi.pushButton_12.hide()
        q = []
        ans = []
        typ = []
        qid = []
        st = orgUi.lineEdit_type_4.currentText()
        if st == "全部":
            y = []
        else:
            y = [st]
        for i in Stu.scope_questions(ques_name, [chapters_name], x, user, y):
            lis = Stu.get_question(i)
            q.append(lis[0])
            ans.append(lis[2])
            typ.append(lis[1])
            qid.append(i)
        print(q)
        if len(q) > 0:
            orgUi.question0.setText(q[0])
            orgUi.question0.clicked.connect(lambda: change_widget_q(q[0], ans[0], typ[0], qid[0], 0))
        else:
            orgUi.question0.hide()
        if len(q) > 1:
            orgUi.question1.setText(q[1])
            orgUi.question1.clicked.connect(lambda: change_widget_q(q[1], ans[1], typ[1], qid[1], 0))
        else:
            orgUi.question1.hide()
        if len(q) > 2:
            orgUi.question2.setText(q[2])
            orgUi.question2.clicked.connect(lambda: change_widget_q(q[2], ans[2], typ[2], qid[2], 0))
        else:
            orgUi.question2.hide()
        if len(q) > 3:
            orgUi.question3.setText(q[3])
            orgUi.question3.clicked.connect(lambda: change_widget_q(q[3], ans[3], typ[3], qid[3],0))
        else:
            orgUi.question3.hide()


    def change_widget_q(text, answer, mytype, qid, flag):
        ans = ''
        lis = Stu.get_question(qid)
        print("qqqqqqq")
        orgUi.stackedWidget.setCurrentIndex(5)
        if flag == 0:
            t = str(qid)
            print(qid)
            orgUi.label_2.setText(t)
        else:
            t = orgUi.label_2.text()
            qid = int(t)
            print(qid)
        a = 0
        b = 0
        c = 0
        d = 0
        a1 = 0
        b1 = 0
        c1 = 0
        d1 = 0
        print(lis[2])
        myans = ['0', '0', '0', '0']
        myans[0] = '0'
        myans[1] = '0'
        myans[2] = '0'
        myans[3] = '0'
        if mytype == 1:
            orgUi.page_2.show()
            orgUi.page.hide()
            orgUi.page_3.hide()
            orgUi.textBrowser_3.setText(text)
            orgUi.notice_2.show()
            orgUi.comment_2.show()
            orgUi.comment_next_2.show()
            ans = orgUi.answer1.text()
            orgUi.submit.clicked.connect(lambda: change_widget_submit(qid, user, ans, lis[2]))
        else:
            orgUi.page.show()
            orgUi.page_2.hide()
            orgUi.page_3.hide()
            orgUi.notice.show()
            orgUi.comment.show()
            orgUi.comment_next.show()
            orgUi.A.setText("A " + lis[3])
            orgUi.B.setText("B " + lis[4])
            orgUi.C.setText("C " + lis[5])
            orgUi.D.setText("D " + lis[6])
            orgUi.textBrowser_2.setText(text)
            orgUi.A.clicked.connect(lambda: change_widget_a(lis[3]))
            if orgUi.A.text()[0:1] == "!":
                myans[0] = '1'
                print(a, end="a")

            orgUi.B.clicked.connect(lambda: change_widget_b(lis[4]))
            if orgUi.B.text()[0:1] == "!":
                myans[1] = '1'
                print(b, end="b")

            orgUi.C.clicked.connect(lambda: change_widget_c(lis[5]))
            if orgUi.C.text()[0:1] == "!":
                myans[2] = '1'

            orgUi.D.clicked.connect(lambda: change_widget_d(lis[6]))
            if orgUi.D.text()[0:1] == "!":
                myans[3] = '1'

            ans = myans[0] + myans[1] + myans[2] + myans[3]
            orgUi.submit1.clicked.connect(lambda: change_widget_submit1(qid, user, ans, lis[2]))


    def change_widget_submit1(qid, user, ans, answer):
        liss = Stu.get_question(qid)
        orgUi.A.setText("A " + liss[3])
        orgUi.B.setText("B " + liss[4])
        orgUi.C.setText("C " + liss[5])
        orgUi.D.setText("D " + liss[6])
        print("enter")
        lis = Stu.do_question(qid, user, ans, ans)
        right = lis[0]
        answers = list(answer)
        if right == False:
            if answers[0] == '1':
                orgUi.A.setStyleSheet("background-color: rgb(69, 188, 55);")  # green
            else:
                orgUi.A.setStyleSheet("background-color: rgb(255, 43, 15);")  # red
            if answers[1] == '1':
                orgUi.B.setStyleSheet("background-color: rgb(69, 188, 55);")
            else:
                orgUi.B.setStyleSheet("background-color: rgb(255, 43, 15);")
            if answers[2] == '1':
                orgUi.C.setStyleSheet("background-color: rgb(69, 188, 55);")
            else:
                orgUi.C.setStyleSheet("background-color: rgb(255, 43, 15);")
            if answers[3] == '1':
                orgUi.D.setStyleSheet("background-color: rgb(69, 188, 55);")
            else:
                orgUi.D.setStyleSheet("background-color: rgb(255, 43, 15);")
        else:
            if ans[0:1] == '1':
                orgUi.A.setStyleSheet("background-color: rgb(69, 188, 55);")
            if ans[1:2] == '1':
                orgUi.B.setStyleSheet("background-color: rgb(69, 188, 55);")
            if ans[2:3] == '1':
                orgUi.C.setStyleSheet("background-color: rgb(69, 188, 55);")
            if ans[3:] == '1':
                orgUi.D.setStyleSheet("background-color: rgb(69, 188, 55);")


    def change_widget_submit(qid, user, ans, answer):  # 按下按钮
        ans = orgUi.answer1.text()
        lis = Stu.do_question(qid, user, ans, ans)
        right = lis[0]
        if right == False:
            orgUi.answer1.setStyleSheet("background-color: rgb(255, 43, 15);")
        else:
            orgUi.answer1.setStyleSheet("background-color: rgb(69, 188, 55);")
        orgUi.label_5.setText(lis[2])


    def change_widget_next():
        t = orgUi.label_2.text()
        qid = int(t) + 1
        lis = Stu.get_question(qid)

        t = str(qid)
        orgUi.label_2.setText(t)
        orgUi.A.setStyleSheet("background-color: rgb(255, 255, 255);")

        orgUi.B.setStyleSheet("background-color: rgb(255, 255, 255);")
        orgUi.C.setStyleSheet("background-color: rgb(255, 255, 255);")
        orgUi.D.setStyleSheet("background-color: rgb(255, 255, 255);")
        orgUi.label_5.setText("")
        orgUi.answer1.setText("")

        orgUi.answer1.setStyleSheet("background-color: rgb(255, 255, 255);")
        change_widget_q(lis[0], lis[2], lis[1], qid, 1)


    def change_widget_front():
        t = orgUi.label_2.text()
        qid = int(t) - 1
        lis = Stu.get_question(qid)

        t = str(qid)
        print(t)
        orgUi.label_2.setText(t)
        orgUi.A.setStyleSheet("background-color: rgb(255, 255, 255);")

        orgUi.B.setStyleSheet("background-color: rgb(255, 255, 255);")
        orgUi.C.setStyleSheet("background-color: rgb(255, 255, 255);")
        orgUi.D.setStyleSheet("background-color: rgb(255, 255, 255);")
        orgUi.answer1.setText("")
        orgUi.label_5.setText("")

        orgUi.answer1.setStyleSheet("background-color: rgb(255, 255, 255);")
        change_widget_q(lis[0], lis[2], lis[1], qid, 1)


    def change_widget_a(text):
        orgUi.A.setText("!" + text)
        orgUi.A.setStyleSheet("background-color: rgb(255, 203, 151);")


    def change_widget_b(text):
        orgUi.B.setText("!" + text)
        orgUi.B.setStyleSheet("background-color: rgb(255, 203, 151);")


    def change_widget_c(text):
        orgUi.C.setText("!" + text)
        orgUi.C.setStyleSheet("background-color: rgb(255, 203, 151);")


    def change_widget_d(text):
        orgUi.D.setText("!" + text)
        orgUi.D.setStyleSheet("background-color: rgb(255, 203, 151);")


    def change_widget_comment_next():
        s = orgUi.notice.text()
        notice = int(s)
        if notice != 1:
            print(notice)
            exec('orgUi.scrollArea' + s + ".hide()")
        notice += 1
        s = str(notice)
        if notice < 6:
            orgUi.notice.setText(s)
            exec('orgUi.scrollArea' + s + ".show()")


    def change_widget_comment_next_2():
        s = orgUi.notice_2.text()
        notice = int(s)
        if notice != 1:
            exec('orgUi.scrollArea' + s + "_3" + ".hide()")
        notice += 1
        s = str(notice)
        if notice < 6:
            orgUi.notice_2.setText(s)
            exec('orgUi.scrollArea' + s + "_3" + ".show()")
        else:
            orgUi.notice_2.setText("1")


    def change_widget_comment():
        orgUi.notice.setText("1")
        orgUi.scrollArea.show()
        orgUi.scrollArea2.hide()
        orgUi.scrollArea3.hide()
        orgUi.scrollArea4.hide()
        orgUi.scrollArea5.hide()
        orgUi.load.show()
        orgUi.comment_next.show()
        orgUi.textEdit_comment.show()
        qid = int(orgUi.label_2.text())
        lis = Stu.show_some_comments(qid)
        length = len(lis)
        for i in range(0, length):
            x = i + 1
            text = ''.join([lis[i][0], ':', lis[i][1]])
            exec("orgUi.comment" + str(x) + ".setText(text)")


    def change_widget_comment_2():
        orgUi.notice_2.setText("1")
        orgUi.scrollArea_3.show()
        orgUi.scrollArea2_3.hide()
        orgUi.scrollArea3_3.hide()
        orgUi.scrollArea4_3.hide()
        orgUi.scrollArea5_3.hide()
        orgUi.load_2.show()
        orgUi.comment_next_2.show()
        orgUi.textEdit_comment_2.show()
        qid = int(orgUi.label_2.text())
        lis = Stu.show_some_comments(qid)
        length = len(lis)
        for i in range(0, length):
            x = i + 1
            text = ''.join([lis[i][0], ':', lis[i][1]])
            exec("orgUi.comment" + str(x) + "_7" + ".setText(text)")


    def change_widget_load():
        content = orgUi.textEdit_comment.toPlainText()

        qid = int(orgUi.label_2.text())
        Stu.send_comments(qid, content, user)
        lis = Stu.show_some_comments(qid)
        # text = ''.join([user,':',ccontent])*********66
        length = len(lis)
        for i in range(0, length):
            x = i + 1
            text = ''.join([lis[i][0], ':', lis[i][1]])
            exec("orgUi.comment" + str(x) + ".setText(text)")


    #            orgUi.comment1.setText(lis[0])
    #            exec("x" + "=" + "orgUi.comment" + str(i) + ".toPlainText()")
    #            print(x)
    #            if x == "":
    #                exec('orgUi.comment' + str(i) + ".setText(text)")
    #                break
    #            else:
    #                x = ""
    #                continue
    # orgUi.comment1.setText(text)

    def change_widget_load_2():
        content = orgUi.textEdit_comment_2.toPlainText()

        qid = int(orgUi.label_2.text())
        Stu.send_comments(qid, content, user)
        lis = Stu.show_some_comments(qid)
        # text = ''.join([user,':',content])
        length = len(lis)
        for i in range(0, length):
            x = i + 1
            text = ''.join([lis[i][0], ':', lis[i][1]])
            exec("orgUi.comment" + str(x) + "_7" + ".setText(text)")


    #            orgUi.comment1_7.setText(lis[0])
    #        comment = orgUi.textEdit_comment_2.toPlainText()
    #        x = orgUi.comment1_7.toPlainText()

    #        user = 'fmy'
    #        if os.path.exists('temp'):
    #            with open('temp', "rt") as file:
    #                user = file.readline()

    #        text = ''.join([user,':',comment])

    #        for i in range(1,31):
    #            exec("x" + "=" + "orgUi.comment" + str(i) + "_7" + ".toPlainText()")
    #            print(x)
    #            if x == "":
    #                exec('orgUi.comment' + str(i) + "_7" + ".setText(text)")
    #                break
    #            else:
    #                x = ""
    #                continue
    # orgUi.comment1.setText(text)

    def change_widget_star():
        qid = orgUi.label_2.text()
        Stu.star_questioin(user, qid)


    def change_widget_9(i):  # 只显示收藏题
        qid = Stu.get_starquestion(user)
        if qid != None:
            lis = Stu.get_question(qid[i])
            change_widget_q(lis[0], lis[2], lis[1], qid[i], 1)
            orgUi.pushButton_30.clicked.connect(lambda: change_widget_next_star(qid, i))
            orgUi.pushButton_36.clicked.connect(lambda: change_widget_front_star(qid, i))


    def change_widget_next_star(qid, i):
        i = i + 1
        x = qid[i]
        t = str(x)
        orgUi.label_2.setText(t)
        orgUi.A.setStyleSheet("background-color: rgb(255, 255, 255);")

        orgUi.B.setStyleSheet("background-color: rgb(255, 255, 255);")
        orgUi.C.setStyleSheet("background-color: rgb(255, 255, 255);")
        orgUi.D.setStyleSheet("background-color: rgb(255, 255, 255);")
        orgUi.label_5.setText("")
        orgUi.answer1.setText("")
        lis = Stu.get_question(x)
        orgUi.answer1.setStyleSheet("background-color: rgb(255, 255, 255);")
        change_widget_q(lis[0], lis[2], lis[1], x, 1)
        change_widget_9(i)


    def change_widget_front_star(qid, i):
        i = i - 1
        x = qid[i]
        t = str(x)
        orgUi.label_2.setText(t)
        orgUi.A.setStyleSheet("background-color: rgb(255, 255, 255);")

        orgUi.B.setStyleSheet("background-color: rgb(255, 255, 255);")
        orgUi.C.setStyleSheet("background-color: rgb(255, 255, 255);")
        orgUi.D.setStyleSheet("background-color: rgb(255, 255, 255);")
        orgUi.label_5.setText("")
        orgUi.answer1.setText("")
        lis = Stu.get_question(x)
        orgUi.answer1.setStyleSheet("background-color: rgb(255, 255, 255);")
        change_widget_q(lis[0], lis[2], lis[1], x, 1)
        change_widget_9(i)


    def change_widget_star2():
        qid = orgUi.label_2.text()
        Stu.star_questioin(user, qid)


    def change_widget_btn(text):  # 按下按钮
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


    def graph_show():
        new_window = Graph.MainWindow(user)
        new_window.exec_()


    orgUi.personability.clicked.connect(graph_show)
    orgUi.pushButton.clicked.connect(change_widget_1)
    orgUi.pushButton_2.clicked.connect(change_widget_2)
    orgUi.pushButton_3.clicked.connect(change_widget_3)
    orgUi.pushButton_4.clicked.connect(change_widget_4)
    orgUi.pushButton_5.clicked.connect(change_widget_5)
    orgUi.pushButton_6.clicked.connect(change_widget_6)
    orgUi.pushButton_7.clicked.connect(change_widget_7)
    orgUi.pushButton_star.clicked.connect(lambda: change_widget_9(0))
    orgUi.pushButton_10.clicked.connect(change_widget_10)
    orgUi.pushButton_12.clicked.connect(change_widget_12)
    orgUi.pushButton_29.clicked.connect(change_widget_front)
    orgUi.pushButton_30.clicked.connect(change_widget_next)
    orgUi.pushButton_36.clicked.connect(change_widget_front)
    orgUi.pushButton_37.clicked.connect(change_widget_next)
    orgUi.comment.clicked.connect(change_widget_comment)
    orgUi.load.clicked.connect(change_widget_load)
    orgUi.comment_next.clicked.connect(change_widget_comment_next)
    orgUi.comment_2.clicked.connect(change_widget_comment_2)
    orgUi.load_2.clicked.connect(change_widget_load_2)
    orgUi.comment_next_2.clicked.connect(change_widget_comment_next_2)
    orgUi.star.clicked.connect(change_widget_star)
    orgUi.star2.clicked.connect(change_widget_star)
    # my window admin
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
    orgUi.pushButton_8.clicked.connect(admin_action.upload)


    # share
    def change_widget_share():
        orgUi.stackedWidget.setCurrentIndex(7)


    # share
    orgUi.share.clicked.connect(change_widget_share)


    def create_qgroup():

        s = Stu.create_own_ques_group(orgUi.lineEdit.text(), user)
        if s:
            QMessageBox.information(win, "", f"创建成功")
        else:
            QMessageBox.information(win, "", f"当前组名已存在")


    def choose_qgroup():
        # orgUi.pushButton_19.hide()
        # orgUi.pushButton_18.hide()
        qgroup_list = list_window.CheckableListWidget()
        text = orgUi.groupline.text()
        itemlist = Stu.search_for_groups(text, user)
        if len(itemlist) == 0:
            QMessageBox.information(search_group_list, "警告", f"您已加入当前小组或没有当前小组")
        else:
            qgroup_list.initializeList(itemlist)
            search_group_list.show()


    def change1():
        orgUi.stackedWidget.setCurrentIndex(8)


    def change2():
        _translate = QtCore.QCoreApplication.translate
        orgUi.stackedWidget.setCurrentIndex(9)
        qgroups = Stu.search_qgroups(user)
        print('qgroups = :')
        print(qgroups)
        for i in range(len(qgroups)):
            orgUi.comboBox.addItem(qgroups[i])
        groups = Stu.search_groups(1)
        for i in range(len(groups)):
            orgUi.comboBox_2.addItem(groups[i])


    def share():
        Stu.share_qgroup_with_group(orgUi.comboBox.currentText(), orgUi.comboBox_2.currentText())
        QMessageBox.information(win, "", f"分享成功")


    def change3():
        orgUi.stackedWidget.setCurrentIndex(10)
        qgroups = Stu.search_qgroups(user)
        for i in range(len(qgroups)):
            orgUi.comboBox_3.addItem(qgroups[i])


    def changecan():
        i = 0
        j = 0
        if (orgUi.checkBox_5.checkState()):
            i = i + 1
            j = 1
        if (orgUi.checkBox_6.checkState()):
            i = i + 1
            j = 2
        if i == 0 | i > 1:
            QMessageBox.information(win, "警告", f"权限矛盾")
        elif j == 1:
            Stu.set_qgroup_public(orgUi.comboBox_3.currentText())
            pass
        elif j == 2:
            Stu.set_qgroup_private(orgUi.comboBox_3.currentText())
            pass


    def change4():
        orgUi.stackedWidget.setCurrentIndex(11)
        qgroups = Stu.search_qgroups(user)
        for i in range(len(qgroups)):
            orgUi.comboBox_4.addItem(qgroups[i])


    def search1():
        ques = Stu.search_ques(orgUi.lineEdit_6.text())
        search_question_list.initializeList(ques)
        search_question_list.show()


    def confirm1():
        selected_items = search_question_list.list_widget.selectedItems()
        selected_names = [item.text() for item in selected_items]
        QMessageBox.information(search_question_list, "选中的项", f"选中的项: {selected_names}")
        Stu.add_ques_into_group(orgUi.comboBox_4.currentText(), selected_names)
        search_question_list.close()
        QMessageBox.information(search_question_list, " ", f"加入成功")


    def chakanwenti(n):  # qid
        lis = Stu.get_question(n)

        t = str(n)
        orgUi.label_2.setText(t)
        orgUi.A.setStyleSheet("background-color: rgb(255, 255, 255);")

        orgUi.B.setStyleSheet("background-color: rgb(255, 255, 255);")
        orgUi.C.setStyleSheet("background-color: rgb(255, 255, 255);")
        orgUi.D.setStyleSheet("background-color: rgb(255, 255, 255);")
        orgUi.label_5.setText("")
        orgUi.answer1.setText("")

        orgUi.answer1.setStyleSheet("background-color: rgb(255, 255, 255);")
        change_widget_q(lis[0], lis[2], lis[1], n, 1)
        change_widget_q()
        print(n)


    def show_all_questions(name):  # 传入的是组名

        orgUi.stackedWidget.setCurrentIndex(13)
        orgUi.ques_list.clear()
        print('name:' + name)
        ques = Stu.ques_in_qgroup(name)  # qid,title
        print('ques:' + str(len(ques)))
        for i in range(len(ques)):
            itemBtn = QListWidgetItem()
            btn = QPushButton("序号" + str(ques[i][0]) + ":" + ques[i][1])
            btn.clicked.connect(partial(chakanwenti, ques[i][0]))
            btn.setFixedWidth(600)
            orgUi.ques_list.insertItem(orgUi.ques_list.count(), itemBtn)
            orgUi.ques_list.setItemWidget(itemBtn, btn)
        orgUi.ques_list.show()


    def change5():
        orgUi.stackedWidget.setCurrentIndex(12)
        orgUi.qgroup_list.clear()
        qgroups = Stu.search_qgroups(user)

        for i in range(len(qgroups)):
            itemBtn = QListWidgetItem()
            btn = QPushButton(qgroups[i])
            print('in_change5:' + qgroups[i])
            temp = qgroups[i]
            btn.clicked.connect(partial(show_all_questions, temp))
            btn.setFixedWidth(450)
            orgUi.qgroup_list.addItem(itemBtn)
            orgUi.qgroup_list.setItemWidget(itemBtn, btn)
        orgUi.qgroup_list.show()


    orgUi.pushButton_16.clicked.connect(search1)
    orgUi.creategroup.clicked.connect(change1)
    orgUi.sharegroup.clicked.connect(change2)
    orgUi.pushButton_15.clicked.connect(change3)
    orgUi.add.clicked.connect(change4)
    ##jljl
    orgUi.pushButton_9.clicked.connect(create_qgroup)
    orgUi.pushButton_13.clicked.connect(share)
    orgUi.pushButton_14.clicked.connect(changecan)
    #    orgUi.pushButton_17.clicked.connect(change_widget_share)
    search_question_list.confirm_button.clicked.connect(confirm1)
    orgUi.creategroup_3.clicked.connect(change5)
    orgUi.pushButton_17.clicked.connect(change_widget_share)
    orgUi.pushButton_35.clicked.connect(change_widget_share)
    win.show()
    sys.exit(app.exec_())
