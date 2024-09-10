# main_window.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from child_window import ChildWindow  # 导入子窗口类


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("主窗口")
        self.setGeometry(100, 100, 400, 300)

        self.button = QPushButton("打开子窗口", self)
        self.button.setGeometry(100, 100, 200, 40)
        self.button.clicked.connect(self.show_child_window)

        self.child_window = None
        self.label = QLabel("", self)
        self.label.setGeometry(100, 150, 200, 40)

    def show_child_window(self):
        if self.child_window is None:
            self.child_window = ChildWindow()
            # 连接信号与槽
            self.child_window.value_submitted.connect(self.display_value)
        self.child_window.show()

    def display_value(self, value):
        # 槽函数，接收来自子窗口的信号并更新主窗口的标签

        print(value)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_win = MainWindow()
    main_win.show()

    sys.exit(app.exec_())
