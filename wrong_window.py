import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from sqlalchemy import create_engine
import login_widget
import exercise2, list_window
from PyQt5.QtWidgets import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.orm.session  # 数据库操作核心
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base  # 父类


class WrongWindow(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.Ui = exercise2.Ui_Form()
        self.Ui.setupUi(self)

        self.num = 10
        self.chap = []
        self.mode = 0 # 填空 + 选择
        self.mode_text = ''

        self.chap_list = list_window.CheckableListWidget()
        self.chap_list.setWindowTitle('选择章节')
        chap_item = ['1', '2', '3', '4', '5', '6']
        self.chap_list.initializeList(chap_item)
        self.chap_list.hide()

        self.mode_list = list_window.CheckableListWidget()
        self.mode_list.setWindowTitle('选择答题模式')
        mode_item = ['只做填空','只做选择','填空和选择']
        self.mode_list.initializeList(mode_item)
        self.mode_list.hide()

        self.button_init()
        self.show()

    def fresh(self):
        self.Ui.exercise.setText('')

    def next(self):
        print('next')
        self.fresh()
        #  todo

    def select_chapter(self):
        self.chap_list.show()
    def select_confirm(self):
        selected_items = self.chap_list.list_widget.selectedItems()
        selected_names = [item.text() for item in selected_items]
        for i in selected_names:
            self.chap.append(i)
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


    def button_init(self):
        self.Ui.s_chap.clicked.connect(self.select_chapter)
        self.chap_list.confirm_button.clicked.connect(self.select_confirm)
        self.Ui.s_mode.clicked.connect(self.select_mode)
        self.mode_list.confirm_button.clicked.connect(self.mode_select_confirm)
        self.Ui.s_confirm.clicked.connect(self.confirm_enum)
        self.Ui.nexte.clicked.connect(self.next)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WrongWindow()
    sys.exit(app.exec_())
