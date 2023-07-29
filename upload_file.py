from PyQt5.QtWidgets import QMainWindow, QFileDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "选择文件")
        print("选择的文件路径:", file_path)
