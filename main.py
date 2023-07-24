# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import org1
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QMainWindow()
    orgUi = org1.Ui_MainWindow()
    orgUi.setupUi(win)
    orgUi.search.hide()

    def change_widget_1():      #上传问题
        orgUi.search.hide()
        orgUi.textEdit.show()
        orgUi.pushButton_7.show()
        orgUi.pushButton_8.show()

    def change_widget_2():      #搜索
        orgUi.search.show()
        orgUi.lineEdit.setText('')
        orgUi.textEdit.hide()
        orgUi.pushButton_7.hide()
        orgUi.pushButton_8.hide()

    def change_widget_3():      #查看问题
        orgUi.search.hide()
        orgUi.textEdit.hide()
        orgUi.pushButton_7.hide()
        orgUi.pushButton_8.hide()

    def change_widget_4():      #错误日志
        orgUi.search.hide()
        orgUi.textEdit.hide()
        orgUi.pushButton_7.hide()
        orgUi.pushButton_8.hide()

    def change_widget_5():      #我的
        orgUi.search.hide()
        orgUi.textEdit.hide()
        orgUi.pushButton_7.hide()
        orgUi.pushButton_8.hide()

    def change_widget_6():      #关于
        orgUi.search.hide()
        orgUi.textEdit.hide()
        orgUi.pushButton_7.hide()
        orgUi.pushButton_8.hide()


    def change_widget_7():      #上传
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