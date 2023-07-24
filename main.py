# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import org1
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import about


# define index_my_add 0
# define index_welcom 1
# define index_upload 2
# define index_search 3
# define index_my_norm 4


class AboutWindow(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.aboutUi = about.Ui_Form()
        self.aboutUi.setupUi(self)
        self.show()


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QMainWindow()
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
        orgUi.stackedWidget.setCurrentIndex(4)


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
    win.show()
    sys.exit(app.exec_())
