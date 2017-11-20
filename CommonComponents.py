from PyQt5 import QtWidgets as Q
from PyQt5.QtCore import Qt as Align
from PyQt5.QtWidgets import QSizePolicy as Size


class DescriptionBox(Q.QVBoxLayout):
    def __init__(self, parent=None, label="Description:", align=Align.AlignLeft):
        super().__init__()
        self.initUI(label, align, parent)

    def initUI(self, label, align, parent):
        self.label = Q.QLabel(parent)
        self.box = Q.QPlainTextEdit(parent)

        self.label.setText(label)
        self.label.setAlignment(align)

        self.addWidget(self.label)
        self.addWidget(self.box)

    def __getattr__(self, name):
        return self.box.__getattribute__(name)


class ButtonGrid(Q.QHBoxLayout):
    def __init__(self, parent=None, labels={"applyBtn": "Apply", "okBtn": "OK", "cancelBtn": "Cancel"}, order=("okBtn", "applyBtn", "cancelBtn")):
        super().__init__()
        self.initUI(labels, order, parent)

    def initUI(self, labels, order, parent):
        self.btns = {}

        for btn in order:
            self.btns[btn] = Q.QPushButton(labels[btn], parent)
            self.btns[btn].setSizePolicy(Size.Preferred, Size.Preferred)
            self.addWidget(self.btns[btn])

    def __getattr__(self, name):
        return self.btns[name]
