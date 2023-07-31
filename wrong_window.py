import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from sqlalchemy import create_engine
import os
import Stu
import login_widget
import exercise2, list_window
from PyQt5.QtWidgets import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.orm.session  # 数据库操作核心
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base  # 父类

class ResultDialog(QDialog):
    def __init__(self, ans, me, all):
        super().__init__(None)
        self.setWindowTitle('结果窗口')

        layout = QVBoxLayout()
        txt = ''
        if ans:
            txt = '正确'
            self.setStyleSheet('background-color: green; color: white;')
        else:
            txt = '错误'
            self.setStyleSheet('background-color: red; color: white;')
        self.label_correct = QLabel(txt, self)
        txt2 = '您的正确率是: ' + str(me) + '%'
        self.label_correct_rate = QLabel(txt2, self)
        txt3 = '所有用户的正确率是: '+ str(all) + '%'
        self.label_all_correct_rate = QLabel(txt3, self)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(me)
        self.all_progress_bar = QProgressBar(self)
        self.all_progress_bar.setValue(all)

        layout.addWidget(self.label_correct)
        layout.addWidget(self.label_correct_rate)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.label_all_correct_rate)
        layout.addWidget(self.all_progress_bar)

        self.setLayout(layout)
class WrongWindow(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.Ui = exercise2.Ui_Form()
        self.Ui.setupUi(self)

        user = 'fmy'
        if os.path.exists('temp'):
            with open('temp', "rt") as file:
                user = file.readline()
        self.username = user
        #  todo test self.username = 'manager'

        self.num = 10
        self.chap = []
        # self.mode = 0 # 填空 + 选择
        self.choose = 1
        self.gap = 1
        self.mode_text = ''
        self.cur = 0

        self.chap_list = list_window.CheckableListWidget()
        self.chap_list.setWindowTitle('选择章节')
        chap_item = ['1', '2', '3', '4', '5', '6']
        self.chap_list.initializeList(chap_item)
        self.chap_list.hide()

        self.mode_list = list_window.CheckableListWidget()
        self.mode_list.setWindowTitle('选择答题模式')
        mode_item = ['只做填空', '只做选择', '填空和选择']
        self.mode_list.initializeList(mode_item)
        self.mode_list.hide()

        self.button_init()
        self.show()

    def select_chapter(self):
        self.chap_list.show()

    def select_confirm(self):
        selected_items = self.chap_list.list_widget.selectedItems()
        selected_names = [item.text() for item in selected_items]
        for i in selected_names:
            txt = 'Chapter_' + i
            self.chap.append(txt)
        reply = QMessageBox.about(self, '章节选择', '选择成功')
        self.chap_list.close()

    def select_mode(self):
        self.mode_list.show()

    def mode_select_confirm(self):
        selected_items = self.mode_list.list_widget.selectedItems()
        selected_names = [item.text() for item in selected_items]
        if len(selected_names) != 1:
            reply = QMessageBox.about(self, '模式选择', '只能选择一个模式')
            self.mode_list.hide()
            self.mode_list.show()
        else:
            self.mode_text = selected_names[0]
            # mode_item = ['只做填空', '只做选择', '填空和选择']
            if self.mode_text == '只做填空':
                self.choose = 0
            elif self.mode_text == '只做选择':
                self.gap = 0
            reply = QMessageBox.about(self, '模式选择', '选择成功')
            self.mode_list.close()

    def confirm_enum(self):
        tnum = self.Ui.enums.text()
        if not tnum.isdigit():
            reply = QMessageBox.about(self, '题目数量', '只能输入数字，请重新输入')
        else:
            self.num = int(tnum)
            text = '已将题目数量设定为' + str(self.num)
            reply = QMessageBox.about(self, '题目数量', text)

    def startexercise(self):
        self.cur = 0
        self.ques = Stu.personalized_recommendation(self.num, self.chap, self.choose, self.gap, self.username)
        # print(self.ques)
        if len(self.ques) == 0:
            reply = QMessageBox.about(self, '做题', '暂无推荐题目')
        else:
            self.show_exercise(self.ques[self.cur])

    def show_exercise(self, qid):
        #  todo backend
        lis = Stu.get_question(qid)
        # lis =['ques.title', 0, 'ques.answer1',' ques.answer2', 'ques.answer3', 'ques.answer4']
        self.Ui.exercise.setText(lis[0])
        # type 0选择,1填空,2多选
        if lis[1] == 0:
            self.Ui.etype.setText('选择题')
            self.Ui.stackedWidget.setCurrentIndex(0)
            # print('lis[2] is ' + lis[2])
            self.Ui.pushButton.setText(lis[3])
            self.Ui.pushButton_2.setText(lis[4])
            self.Ui.pushButton_3.setText(lis[5])
            self.Ui.pushButton_4.setText(lis[6])
        elif lis[1] == 1:
            self.Ui.etype.setText('填空题')
            self.Ui.stackedWidget.setCurrentIndex(1)
        else:
            self.Ui.etype.setText('多选题')
            self.Ui.stackedWidget.setCurrentIndex(2)
            self.Ui.checkBox.setText(lis[3])
            self.Ui.checkBox_3.setText(lis[4])
            self.Ui.checkBox_4.setText(lis[5])
            self.Ui.checkBox_5.setText(lis[6])

    def fresh(self):
        self.Ui.exercise.setText('')
        self.Ui.lineEdit.setText('')

    def next(self):
        print('next')
        self.fresh()
        if self.cur + 1 < self.num:
            self.cur = self.cur + 1
            self.show_exercise(self.ques[self.cur])
        else:
            reply = QMessageBox.about(self, '', '已经是最后一道题了')

    def pre(self):
        self.fresh()
        if self.cur - 1 >= 0:
            self.cur = self.cur - 1
            self.show_exercise(self.ques[self.cur])
        else:
            reply = QMessageBox.about(self, '', '已经是第一道题了')

    def select_do_question_a(self):
        lis = Stu.do_question(self.ques[self.cur], self.username, '1000', '')
        answer = lis[0] == 1
        myrate = lis[3]
        allrate = lis[4]
        print(1)
        result = ResultDialog(answer,myrate,allrate)
        print(2)
        result.exec_()
        print(3)
        self.next()

    def select_do_question_b(self):
        lis = Stu.do_question(self.ques[self.cur], self.username, '0100', '')
        answer = lis[0] == 1
        myrate = lis[3]
        allrate = lis[4]
        result = ResultDialog(answer, myrate, allrate)
        result.exec_()
        self.next()

    def select_do_question_c(self):
        lis = Stu.do_question(self.ques[self.cur], self.username, '0010', '')
        answer = lis[0] == 1
        myrate = lis[3]
        allrate = lis[4]
        result = ResultDialog(answer, myrate, allrate)
        result.exec_()
        self.next()

    def select_do_question_d(self):
        lis = Stu.do_question(self.ques[self.cur], self.username, '0001', '')
        answer = lis[0] == 1
        myrate = lis[3]
        allrate = lis[4]
        result = ResultDialog(answer, myrate, allrate)
        result.exec_()
        self.next()

    def blank_do_question(self):
        line0 = self.Ui.lineEdit.text()
        myans = line0
        lis = Stu.do_question(self.ques[self.cur], self.username, 0, myans)
        answer = lis[0] == 1
        myrate = lis[3]
        allrate = lis[4]
        result = ResultDialog(answer, myrate, allrate)
        result.exec_()
        self.next()

    def mul_do_question(self):
        myans = ''
        mymul = []
        mymul.append(self.Ui.checkBox.isChecked())
        mymul.append(self.Ui.checkBox_3.isChecked())
        mymul.append(self.Ui.checkBox_4.isChecked())
        mymul.append(self.Ui.checkBox_5.isChecked())
        for item in mymul:
            if item:
                myans = myans + '1'
            else:
                myans = myans + '0'
        lis = Stu.do_question(self.ques[self.cur], self.username, myans, '')
        answer = lis[0] == 1
        myrate = lis[3]
        allrate = lis[4]
        result = ResultDialog(answer, myrate, allrate)
        result.exec_()
        self.next()
    def star(self):
        Stu.star_questioin(self.username,self.ques[self.cur])
        reply = QMessageBox.about(self, '收藏问题', '收藏成功')


    def button_init(self):
        self.Ui.s_chap.clicked.connect(self.select_chapter)
        self.chap_list.confirm_button.clicked.connect(self.select_confirm)
        self.Ui.s_mode.clicked.connect(self.select_mode)
        self.mode_list.confirm_button.clicked.connect(self.mode_select_confirm)
        self.Ui.s_confirm.clicked.connect(self.confirm_enum)
        self.Ui.nexte.clicked.connect(self.next)
        self.Ui.pree.clicked.connect(self.pre)
        self.Ui.start.clicked.connect(self.startexercise)
        self.Ui.pushButton.clicked.connect(self.select_do_question_a)
        self.Ui.pushButton_2.clicked.connect(self.select_do_question_b)
        self.Ui.pushButton_3.clicked.connect(self.select_do_question_c)
        self.Ui.pushButton_4.clicked.connect(self.select_do_question_d)
        self.Ui.confirm_mul.clicked.connect(self.mul_do_question)
        self.Ui.confirm_blank.clicked.connect(self.blank_do_question)
        self.Ui.shoucang.clicked.connect(self.star)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WrongWindow()
    sys.exit(app.exec_())
