# child_window.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal


class ChildWindow(QWidget):
    # 自定义信号，带一个字符串参数
    value_submitted = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("子窗口")
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout()
        self.label = QLabel("点击按钮发送信号")
        self.layout.addWidget(self.label)

        self.button = QPushButton("发送信号", self)
        self.button.clicked.connect(self.send_value)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def send_value(self):
        # 按钮点击后发送信号，并传递一个字符串
        self.value_submitted.emit("这是来自子窗口的消息")
