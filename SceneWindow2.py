from PyQt5 import QtWidgets as Q
from PyQt5.QtWidgets import QSizePolicy as SP
from PyQt5 import QtCore as QC
from PyQt5 import QtSql as QS
from PyQt5.QtCore import pyqtSlot

db = QS.QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("test.db")
db.open()


class SceneWindow2(Q.QWidget):
    def __init__(self, scene):
        super().__init__()
        self.initUI()
        self.scene = scene
        self.populate()

    def initUI(self):
        self.setMinimumSize(600, 400)
        self.setWindowTitle("Edit Scene")

        layout = Q.QGridLayout(self)
        tabWidget = Q.QTabWidget()
        self.sceneInfoTab = SceneInfoTab()
        self.charactersTab = SceneCharactersTab()
        tabWidget.addTab(self.sceneInfoTab, "Scene Info")
        tabWidget.addTab(self.charactersTab, "Characters")
        layout.addWidget(tabWidget, 0, 0)

        buttonGrid = Q.QGridLayout()
        okCancelHBox = Q.QHBoxLayout()
        editButton = Q.QPushButton("Edit Scene")
        editButton.setSizePolicy(SP.Preferred, SP.Preferred)
        okButton = Q.QPushButton("OK")
        okButton.clicked.connect(self.submit)
        okButton.setSizePolicy(SP.Preferred, SP.Preferred)
        cancelButton = Q.QPushButton("Cancel")
        cancelButton.clicked.connect(self.close)
        cancelButton.setSizePolicy(SP.Preferred, SP.Preferred)
        okCancelHBox.addWidget(okButton)
        okCancelHBox.addWidget(cancelButton)
        buttonGrid.addWidget(editButton, 0, 0)
        buttonGrid.addLayout(okCancelHBox, 0, 1)
        buttonGrid.setAlignment(editButton, QC.Qt.AlignLeft)
        buttonGrid.setAlignment(okCancelHBox, QC.Qt.AlignRight)

        layout.addLayout(buttonGrid, 1, 0)
        self.setLayout(layout)

    def populate(self):
        self.sceneInfoTab.populate(self.scene)
        self.charactersTab.populate(self.scene)

    def submit(self):
        self.sceneInfoTab.update(self.scene)
        self.charactersTab.update(self.scene)
        self.scene.commit()
        self.close()


class SceneInfoTab(Q.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = Q.QVBoxLayout()
        titleStatusLayout = Q.QHBoxLayout()

        titleLayout = Q.QHBoxLayout()
        self.titleBox = Q.QLineEdit()
        self.titleBox.setFixedWidth(300)
        titleBoxLabel = Q.QLabel()
        titleBoxLabel.setText("Title:")
        titleLayout.addWidget(titleBoxLabel)
        titleLayout.addWidget(self.titleBox)
        titleLayout.setAlignment(self.titleBox, QC.Qt.AlignLeft)

        statusLayout = Q.QHBoxLayout()
        self.statusBox = Q.QComboBox()
        statusBoxLabel = Q.QLabel(self.statusBox)
        statusBoxLabel.setText("Revision:")
        statusLayout.addWidget(statusBoxLabel)
        statusLayout.addWidget(self.statusBox)

        titleStatusLayout.addLayout(titleLayout)
        titleStatusLayout.addLayout(statusLayout)
        titleStatusLayout.setAlignment(titleLayout, QC.Qt.AlignLeft)
        titleStatusLayout.setAlignment(statusLayout, QC.Qt.AlignRight)

        descriptionLayout = Q.QVBoxLayout()
        descriptionBoxLabel = Q.QLabel()
        descriptionBoxLabel.setText("Description:")
        self.descriptionBox = Q.QPlainTextEdit()
        descriptionLayout.addWidget(descriptionBoxLabel)
        descriptionLayout.addWidget(self.descriptionBox)
        descriptionLayout.setAlignment(descriptionBoxLabel, QC.Qt.AlignLeft)

        layout.addLayout(titleStatusLayout)
        layout.addSpacing(5)
        layout.addLayout(descriptionLayout)

        self.setLayout(layout)

    def populate(self, scene):
        self.titleBox.setText(scene.title)
        self.descriptionBox.setPlainText(scene.description)

    def update(self, scene):
        scene.title = self.titleBox.text()
        scene.description = self.descriptionBox.toPlainText()


class SceneCharactersTab(Q.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = Q.QHBoxLayout()
        notInSceneLayout = Q.QVBoxLayout()
        controlsLayout = Q.QVBoxLayout()
        inSceneLayout = Q.QVBoxLayout()

        notInSceneLabel = Q.QLabel()
        notInSceneLabel.setText("Not In Scene")
        self.notInSceneList = Q.QListView()
        notInSceneLayout.addWidget(notInSceneLabel)
        notInSceneLayout.addWidget(self.notInSceneList)
        notInSceneLayout.setAlignment(notInSceneLabel, QC.Qt.AlignCenter)

        addButton = Q.QPushButton(">")
        addButton.setFixedWidth(addButton.minimumSizeHint().height())
        addButton.setSizePolicy(SP.Fixed, SP.Fixed)
        addButton.clicked.connect(self.moveInScene)
        removeButton = Q.QPushButton("<")
        removeButton.setFixedWidth(removeButton.minimumSizeHint().height())
        removeButton.setSizePolicy(SP.Fixed, SP.Fixed)
        removeButton.clicked.connect(self.moveOutScene)
        controlsLayout.addStretch(50)
        controlsLayout.addWidget(addButton)
        controlsLayout.addSpacing(5)
        controlsLayout.addWidget(removeButton)
        controlsLayout.addStretch(50)
        controlsLayout.setSizeConstraint(Q.QLayout.SetMinimumSize)

        inSceneLabel = Q.QLabel()
        inSceneLabel.setText("In Scene")
        self.inSceneList = Q.QListView()
        inSceneLayout.addWidget(inSceneLabel)
        inSceneLayout.addWidget(self.inSceneList)
        inSceneLayout.setAlignment(inSceneLabel, QC.Qt.AlignCenter)

        layout.addLayout(notInSceneLayout)
        layout.addLayout(controlsLayout)
        layout.addLayout(inSceneLayout)

        self.setLayout(layout)

    def populate(self, sceneID):
        self.model1 = QS.QSqlQueryModel()
        self.model1.setQuery(
            "SELECT * FROM Character WHERE characterID IN (SELECT characterID FROM CharacterInScene WHERE sceneID=" + str(1) + ")")
        self.model2 = QS.QSqlQueryModel()
        self.model2.setQuery(
            "SELECT * FROM Character WHERE characterID NOT IN (SELECT characterID FROM CharacterInScene WHERE sceneID=" + str(1) + ")")
        self.inSceneList.setModel(self.model1)
        self.inSceneList.setModelColumn(1)
        self.notInSceneList.setModel(self.model2)
        self.notInSceneList.setModelColumn(1)

    def update(self, scene):
        pass

    def moveInScene(self):
        pass

    def moveOutScene(self):
        pass


class CharacterList(Q.QWidget):
    def __init__(self, title, query):
        super().__init__(self)
        self.query = query
        self.initUI(title)

    def initUI(self, title):
        layout = Q.QVBoxLayout()

        label = Q.QLabel()
        label.setText(title)
        label.setAlignment(QC.Qt.AlignCenter)

        self.listView = Q.QListView()
        self.model = Q.QSqlQueryModel()
        self.listView.setModel(self.model)

        layout.addWidget(label)
        layout.addWidget(self.listView)

    def setQuery(self, q):
        self.query = q
        self.updateModel()

    def updateModel(self):
        self.model.setQuery(self.q)
        self.listView.setModelColumn(1)
