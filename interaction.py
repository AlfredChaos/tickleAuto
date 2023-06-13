import sys
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


# app = QApplication(sys.argv)
# w = QWidget()
# w.resize(500, 500)

# w.layout = QVBoxLayout()
# w.label = QLabel("Hello World!")
# w.label.setStyleSheet("font-size:25px;margin-left:155px;")
# w.setWindowTitle("PyQt5 窗口")
# w.layout.addWidget(w.label)
# w.setLayout(w.layout)

# w.show()
# sys.exit(app.exec_())

def window():
    app = QApplication(sys.argv)
    win = QWidget()
    
    l1 = QLabel("Name")
    nm = QLineEdit()

    l2 = QLabel("Address")
    add1 = QLineEdit()
    add2 = QLineEdit()
    fbox = QFormLayout()
    fbox.addRow(l1, nm)
    
    vbox = QVBoxLayout()
    vbox.addWidget(add1)
    vbox.addWidget(add2)
    fbox.addRow(l2, vbox)
    
    hbox = QHBoxLayout()
    r1 = QRadioButton("Male")
    r2 = QRadioButton("Female")
    hbox.addWidget(r1)
    hbox.addWidget(r2)
    hbox.addStretch()
    fbox.addRow(QLabel("sex"), hbox)
    fbox.addRow(QPushButton("Submit"), QPushButton("Cancel"))

    win.setLayout(fbox)
    win.setWindowTitle("PyQt5 from Layout")
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    window()
    