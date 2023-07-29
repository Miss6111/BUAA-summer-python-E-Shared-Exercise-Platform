from PyQt5.QtWidgets import QMainWindow, QFileDialog
import Stu

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
    def getPath(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "选择文件")
        return file_path

