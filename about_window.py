import login_window
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from sqlalchemy import create_engine
import login_widget
import about
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.orm.session  # 数据库操作核心
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base  # 父类


class AboutWindow(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.aboutUi = about.Ui_Form()
        self.aboutUi.setupUi(self)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AboutWindow()
    sys.exit(app.exec_())
