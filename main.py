import sys
import tickle
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initGUI()
        
    def initGUI(self):
        self.setWindowTitle("自动化工具")
        fbox = QFormLayout()

        self.label = QLabel("请输入目标网址")
        self.target = QLineEdit()
        fbox.addRow(self.label, self.target)
        submitButton = QPushButton("Submit")
        cancelButton = QPushButton("Cancel")
        fbox.addRow(submitButton, cancelButton)
        submitButton.clicked.connect(self.on_submit_clicked)
        cancelButton.clicked.connect(self.on_cancle_clicked)

        self.setLayout(fbox)

    def on_submit_clicked(self):
        target = self.target.text()
        if target:
            tickle.ticket_snatch(target=target)
        else:
            # raise "目标网址不能为空"
            target = "https://detail.damai.cn/item.htm?spm=a2oeg.home.card_0.ditem_1.591b23e1zTvcwn&id=722910145901"
            tickle.ticket_snatch(target=target)

    def on_cancle_clicked(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
