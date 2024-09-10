import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from setting import SecondWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 300, 200)

        # 主窗口中的按钮
        self.pushButton = QPushButton('Open Second Window', self)
        self.pushButton.setGeometry(50, 50, 200, 50)
        self.pushButton.clicked.connect(self.open_second_window)

        # 显示从第二个窗口传递过来的值的标签
        self.label = QLabel('Waiting for input...', self)
        self.label.setGeometry(50, 120, 200, 50)

    def open_second_window(self):
        self.second_window = SecondWindow()  # 创建第二个窗口实例
        self.second_window.value_submitted.connect(self.display_value)  # 连接信号与槽函数
        self.second_window.show()  # 显示第二个窗口

    def display_value(self, value):
        self.label.setText(f'Received: {value}')  # 在标签上显示传递过来的值

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
