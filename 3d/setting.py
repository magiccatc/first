from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import pyqtSignal

class SettingsWindow(QWidget):
    # 自定义信号，传递字符串值
    value_submitted = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Second Window')
        self.setGeometry(150, 150, 300, 200)

        # 布局和组件
        layout = QVBoxLayout()

        self.label = QLabel('Enter a value:', self)
        layout.addWidget(self.label)

        self.lineEdit = QLineEdit(self)
        layout.addWidget(self.lineEdit)

        self.submitButton = QPushButton('Submit', self)
        self.submitButton.clicked.connect(self.submit_value)
        layout.addWidget(self.submitButton)

        self.setLayout(layout)

    def submit_value(self):
        value = self.lineEdit.text()  # 获取输入框中的值
        self.value_submitted.emit(value)  # 发送信号，将值传递出去
        self.close()  # 关闭第二个窗口
