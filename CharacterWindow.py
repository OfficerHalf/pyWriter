from PyQt5 import QtWidgets as Q
from PyQt5.QtWidgets import QSizePolicy as SP
from PyQt5 import QtCore as QC


class CharacterWindow(Q.QWidget):
    def __init__(self, character):
        super().__init__()
        self.initUI()
        self.character = character
        self.populate()

    def initUI(self):
        self.setMinimumSize(600, 400)
        self.setWindowTitle("Edit Character")

        layout = Q.QGridLayout(self)
        tabWidget = Q.QTabWidget()
        self.infoTab = InfoTab()
        self.bioTab = BioTab()
        tabWidget.addTab(self.infoTab, "Info")
        tabWidget.addTab(self.bioTab, "Bio")
        layout.addWidget(tabWidget, 0, 0)

        okCancelHBox = Q.QHBoxLayout()
        okButton = Q.QPushButton("OK")
        okButton.clicked.connect(self.submit)
        okButton.setSizePolicy(SP.Preferred, SP.Preferred)
        cancelButton = Q.QPushButton("Cancel")
        cancelButton.clicked.connect(self.close)
        cancelButton.setSizePolicy(SP.Preferred, SP.Preferred)
        okCancelHBox.addWidget(okButton)
        okCancelHBox.addWidget(cancelButton)

        layout.addLayout(okCancelHBox, 1, 0)
        layout.setAlignment(okCancelHBox, QC.Qt.AlignRight)
        self.setLayout(layout)

    def populate(self):
        self.infoTab.populate(self.character)
        self.bioTab.populate(self.character)

    def submit(self):
        self.infoTab.update(self.character)
        self.bioTab.update(self.character)
        self.character.commit()
        self.close()


class InfoTab(Q.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = Q.QGridLayout(self)
        self.shortNameBox = Q.QLineEdit()
        shortNameLabel = Q.QLabel()
        shortNameLabel.setText("Short Name:")

        self.fullNameBox = Q.QLineEdit()
        fullNameLabel = Q.QLabel()
        fullNameLabel.setText("Full Name:")

        self.descriptionBox = Q.QPlainTextEdit()
        descriptionLabel = Q.QLabel()
        descriptionLabel.setText("Description:")

        layout.addWidget(shortNameLabel, 0, 0)
        layout.addWidget(self.shortNameBox, 0, 1)
        layout.addWidget(fullNameLabel, 1, 0)
        layout.addWidget(self.fullNameBox, 1, 1)
        layout.addWidget(descriptionLabel, 2, 0)
        layout.setAlignment(descriptionLabel, QC.Qt.AlignTop)
        layout.addWidget(self.descriptionBox, 2, 1)

        self.setLayout(layout)

    def populate(self, character):
        self.shortNameBox.setText(character.shortName)
        self.fullNameBox.setText(character.fullName)
        self.descriptionBox.setPlainText(character.description)

    def update(self, character):
        character.shortName = self.shortNameBox.text()
        character.fullName = self.fullNameBox.text()
        character.description = self.descriptionBox.toPlainText()


class BioTab(Q.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = Q.QGridLayout()
        self.bioBox = Q.QTextEdit()
        layout.addWidget(self.bioBox)
        self.setLayout(layout)

    def populate(self, character):
        self.bioBox.setText(character.bio)

    def update(self, character):
        character.bio = self.bioBox.toPlainText()
