from PyQt5 import QtWidgets as Q
from PyQt5.QtWidgets import QSizePolicy as Size
from PyQt5.QtCore import Qt as Align
from PyQt5 import QtSql as Sql
from CommonComponents import DescriptionBox, ButtonGrid
from Connection import getConnection


class SceneWindow(Q.QDialog):
    def __init__(self, sceneID, parent=None):
        super().__init__(parent)
        self.sceneID = sceneID

        # Set up db transaction
        self.db = getConnection()
        self.ok = False
        self.db.transaction()

        self.initUI()
        self.bind()
        self.okCancelApply.applyBtn.setDisabled(True)

    def initUI(self):
        self.setMinimumSize(600, 400)
        self.setWindowTitle("Edit Scene")
        self.setModal(True)

        layout = Q.QGridLayout()
        self.sceneInfoTab = SceneInfoTab(self.sceneID, self)
        self.charactersTab = SceneCharactersTab(self.sceneID, self)
        tabWidget = Q.QTabWidget(self)
        tabWidget.addTab(self.sceneInfoTab, "Scene Info")
        tabWidget.addTab(self.charactersTab, "Characters")
        layout.addWidget(tabWidget, 0, 0)

        buttonLayout = Q.QHBoxLayout()
        editButton = Q.QPushButton("Edit Content", self)
        editButton.setSizePolicy(Size.Preferred, Size.Preferred)
        self.okCancelApply = ButtonGrid(self)
        self.okCancelApply.okBtn.clicked.connect(self.submit)
        self.okCancelApply.applyBtn.clicked.connect(self.apply)
        self.okCancelApply.cancelBtn.clicked.connect(self.close)
        buttonLayout.addWidget(editButton)
        buttonLayout.addLayout(self.okCancelApply)
        buttonLayout.setAlignment(editButton, Align.AlignLeft)
        buttonLayout.setAlignment(self.okCancelApply, Align.AlignRight)

        layout.addLayout(buttonLayout, 1, 0)
        self.setLayout(layout)

    def bind(self):
        self.sceneInfoTab.bind()

    def apply(self):
        self.db.commit()
        self.parent().update()
        self.okCancelApply.applyBtn.setDisabled(True)
        self.db.transaction()

    def submit(self):
        self.db.commit()
        self.parent().update()
        self.ok = True
        self.close()

    def closeEvent(self, event):
        if not self.ok:
            self.db.rollback()
        super().closeEvent(event)

    def changed(self):
        self.okCancelApply.applyBtn.setDisabled(False)


class SceneInfoTab(Q.QWidget):
    def __init__(self, sceneID, parent=None):
        super().__init__(parent)
        self.initUI()
        self.sceneID = sceneID
        self.query = "SELECT sceneID, title, description, revisionID FROM Scene WHERE sceneID={};".format(
            sceneID)
        self.revQuery = "SELECT revisionID, name FROM Revision ORDER BY revisionID;"

    def initUI(self):
        layout = Q.QVBoxLayout()
        titleStatusLayout = Q.QHBoxLayout()

        titleLayout = Q.QHBoxLayout()
        self.titleBox = Q.QLineEdit(self)
        self.titleBox.setFixedWidth(300)
        self.titleBox.textChanged.connect(self.changed)
        self.titleBox.setObjectName("Title")
        titleBoxLabel = Q.QLabel(self)
        titleBoxLabel.setText("Title:")
        titleLayout.addWidget(titleBoxLabel)
        titleLayout.addWidget(self.titleBox)
        titleLayout.setAlignment(self.titleBox, Align.AlignLeft)

        statusLayout = Q.QHBoxLayout()
        self.statusBox = Q.QComboBox(self)
        self.statusBox.currentIndexChanged.connect(self.changed)
        statusBoxLabel = Q.QLabel(self)
        statusBoxLabel.setText("Revision:")
        statusLayout.addWidget(statusBoxLabel)
        statusLayout.addWidget(self.statusBox)

        titleStatusLayout.addLayout(titleLayout)
        titleStatusLayout.addLayout(statusLayout)
        titleStatusLayout.setAlignment(titleLayout, Align.AlignLeft)
        titleStatusLayout.setAlignment(statusLayout, Align.AlignRight)

        self.description = DescriptionBox(self)
        self.description.box.setObjectName("Description")
        self.description.box.textChanged.connect(self.changed)

        layout.addLayout(titleStatusLayout)
        layout.addSpacing(5)
        layout.addLayout(self.description)

        self.setLayout(layout)

    def bind(self):
        q1 = Sql.QSqlQuery(self.query)
        q1.first()
        revisionID = q1.value(3)
        q2 = Sql.QSqlQueryModel(self)
        q2.setQuery(self.revQuery)
        self.titleBox.setText(q1.value(1))
        self.titleBox.textChanged.connect(self.textChanged)
        self.description.box.setPlainText(q1.value(2))
        self.description.box.textChanged.connect(self.textChanged)
        self.statusBox.setModel(q2)
        self.statusBox.setModelColumn(1)
        self.statusBox.currentIndexChanged.connect(self.updateRevision)
        # find the right revision and select it
        for record in range(q2.rowCount()):
            if(q2.record(record).value("revisionID") == revisionID):
                self.statusBox.setCurrentIndex(record)
                break

    def textChanged(self):
        sender = self.sender()
        field = ""
        value = ""
        if sender.objectName() == "Title":
            field = "title"
            value = sender.text()
        elif sender.objectName() == "Description":
            field = "description"
            value = sender.toPlainText()
        query = Sql.QSqlQuery()
        query.prepare(
            "UPDATE Scene SET {} = :value WHERE sceneID = :sceneID;".format(field))
        query.bindValue(":value", value)
        query.bindValue(":sceneID", self.sceneID)
        query.exec_()

    def updateRevision(self):
        newRevision = self.statusBox.model().record(
            self.statusBox.currentIndex()).value("revisionID")
        query = Sql.QSqlQuery()
        query.prepare(
            "UPDATE Scene SET revisionID = :revisionID WHERE sceneID = :sceneID;")
        query.bindValue(":revisionID", newRevision)
        query.bindValue(":sceneID", self.sceneID)
        query.exec_()

    def changed(self):
        # TODO: parent parent parent is bad
        self.parent().parent().parent().changed()


class SceneCharactersTab(Q.QWidget):
    def __init__(self, sceneID, parent=None):
        super().__init__(parent)
        self.sceneID = sceneID
        self.initUI()

    def initUI(self):
        layout = Q.QHBoxLayout()
        controlsLayout = Q.QVBoxLayout()

        q1 = "SELECT characterID, fullName, shortName, description, bio FROM Character WHERE characterID NOT IN " \
            "(SELECT characterID FROM CharacterInScene WHERE sceneID={})".format(
                self.sceneID)

        q2 = "SELECT characterID, fullName, shortName, description, bio FROM Character WHERE characterID IN " \
            "(SELECT characterID FROM CharacterInScene WHERE sceneID={})".format(
                self.sceneID)

        self.notInSceneList = CharacterList("Not In Scene", q1, 1, self)
        self.inSceneList = CharacterList("In Scene", q2, 1, self)

        addButton = Q.QPushButton(">", self)
        addButton.setFixedWidth(addButton.minimumSizeHint().height())
        addButton.setSizePolicy(Size.Fixed, Size.Fixed)
        addButton.clicked.connect(self.moveInScene)
        removeButton = Q.QPushButton("<", self)
        removeButton.setFixedWidth(removeButton.minimumSizeHint().height())
        removeButton.setSizePolicy(Size.Fixed, Size.Fixed)
        removeButton.clicked.connect(self.moveOutScene)
        controlsLayout.addStretch(50)
        controlsLayout.addWidget(addButton)
        controlsLayout.addSpacing(5)
        controlsLayout.addWidget(removeButton)
        controlsLayout.addStretch(50)
        controlsLayout.setSizeConstraint(Q.QLayout.SetMinimumSize)

        layout.addWidget(self.notInSceneList)
        layout.addLayout(controlsLayout)
        layout.addWidget(self.inSceneList)

        self.setLayout(layout)

    def moveInScene(self):
        changed = False
        for character in self.notInSceneList.listView.selectionModel().selectedIndexes():
            changed = True
            characterID = self.notInSceneList.model.record(
                character.row()).value("characterID")
            query = Sql.QSqlQuery()
            query.prepare(
                "INSERT INTO CharacterInScene VALUES (:characterID, :sceneID);")
            query.bindValue(":characterID", characterID)
            query.bindValue(":sceneID", self.sceneID)
            query.exec_()
        self.notInSceneList.bind(1)
        self.inSceneList.bind(1)
        if changed:
            self.changed()

    def moveOutScene(self):
        changed = False
        for character in self.inSceneList.listView.selectionModel().selectedIndexes():
            changed = True
            characterID = self.inSceneList.model.record(
                character.row()).value("characterID")
            query = Sql.QSqlQuery()
            query.prepare(
                "DELETE FROM CharacterInScene WHERE characterID = :characterID AND sceneID = :sceneID;")
            query.bindValue(":characterID", characterID)
            query.bindValue(":sceneID", self.sceneID)
            query.exec_()
        self.notInSceneList.bind(1)
        self.inSceneList.bind(1)
        if changed:
            self.changed()

    def changed(self):
        # TODO: parent parent parent is bad
        self.parent().parent().parent().changed()


class CharacterList(Q.QWidget):
    def __init__(self, title, query, column, parent=None):
        super().__init__(parent)
        self.initUI(title)
        self.query = query
        self.bind(column)

    def initUI(self, title):
        layout = Q.QVBoxLayout()

        label = Q.QLabel(self)
        label.setText(title)
        label.setAlignment(Align.AlignCenter)
        self.listView = Q.QListView(self)
        self.model = Sql.QSqlQueryModel(self)
        self.listView.setModel(self.model)

        layout.addWidget(label)
        layout.addWidget(self.listView)

        self.setLayout(layout)

    def bind(self, column):
        self.model.setQuery(self.query)
        self.listView.setModelColumn(column)
