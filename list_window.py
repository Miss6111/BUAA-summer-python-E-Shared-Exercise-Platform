import sys
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QHBoxLayout, QVBoxLayout, QPushButton, QMessageBox

class CheckableListWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.list_widget = QListWidget(self)
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        self.list_widget.itemClicked.connect(self.handleItemClicked)

        self.confirm_button = QPushButton("确定", self)
        # self.confirm_button.clicked.connect(self.handleConfirmClicked)

        self.cancel_button = QPushButton("取消", self)
        self.cancel_button.clicked.connect(self.close)

        # Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.confirm_button)
        button_layout.addWidget(self.cancel_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.list_widget)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.setWindowTitle("带复选框的列表")

    def handleItemClicked(self, item):
        item.setCheckState(1 if item.checkState() == 0 else 0)

    def handleConfirmClicked(self):
        selected_items = self.list_widget.selectedItems()
        selected_names = [item.text() for item in selected_items]
        QMessageBox.information(self, "选中的项", f"选中的项: {selected_names}")
        self.close()

    def initializeList(self, items):  # 初始化所有item
        self.list_widget.clear()
        self.list_widget.addItems(items)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CheckableListWidget()
    window.resize(300, 200)

    # Initialize the list with desired content
    items_to_load = ["Item 1", "Item 2", "Item 3", "Item 4"]
    window.initializeList(items_to_load)

    window.show()
    sys.exit(app.exec_())
