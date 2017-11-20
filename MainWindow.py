from PyQt5 import QtWidgets as Q
from PyQt5.QtWidgets import QSizePolicy as Size
from PyQt5.QtCore import Qt as Align
from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtCore import Qt
from PyQt5 import QtSql as Sql
from Connection import getConnection
from SceneWindow import SceneWindow


class MainWindow(Q.QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = getConnection()
        self.initUI()

    def initUI(self):
        widget = Q.QWidget()

        self.setMinimumSize(600, 400)
        self.resize(1500, 800)
        layout = Q.QVBoxLayout()

        fileMenu = self.menuBar().addMenu("File")

        self.sectionList = SectionListView(self)

        self.sceneList = SceneListView(self)

        splitter = Q.QSplitter()
        splitter.setSizePolicy(Size.Expanding, Size.Expanding)

        splitter2 = Q.QSplitter()
        splitter2.setOrientation(Align.Vertical)
        splitter2.addWidget(self.sectionList)
        box = Q.QPlainTextEdit()
        splitter2.addWidget(box)

        splitter.addWidget(splitter2)
        splitter.addWidget(self.sceneList)

        layout.addWidget(splitter)

        statusBar = Q.QStatusBar()
        statusBar.setMaximumHeight(30)
        layout.addWidget(statusBar)

        widget.setLayout(layout)
        self.setCentralWidget(widget)


class SectionListView(Q.QTableView):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        self.bind()

    def initUI(self):
        # Add right click menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openRCMenu)

        # Add onclick
        self.clicked.connect(self.rowSelected)

        # TODO: set drag/drop options
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(Q.QAbstractItemView.InternalMove)
        self.setSelectionMode(Q.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(Q.QAbstractItemView.SelectRows)

        # set model
        self.model = Sql.QSqlQueryModel(self)
        self.setModel(self.model)
        # fill container
        self.horizontalHeader().setStretchLastSection(True)

    def bind(self):
        query = "SELECT se.sectionID, se.name, COUNT(sc.sectionID), se.description, se.sectionOrder, se.parentID FROM Section se LEFT JOIN Scene sc ON se.sectionID = sc.sectionID GROUP BY se.sectionID ORDER BY se.sectionOrder"
        self.model.setQuery(query)
        self.model.setHeaderData(1, Align.Horizontal, "Name")
        self.model.setHeaderData(3, Align.Horizontal, "Description")
        self.model.setHeaderData(2, Align.Horizontal, "Scenes")
        self.setColumnHidden(0, True)
        self.setColumnHidden(4, True)
        self.setColumnHidden(5, True)
        self.setColumnHidden(6, True)
        self.setModel(self.model)

    def insertSection(self, order=None, parent=None):
        name = self.getNextSectionName()
        description = ""
        if not order:
            order = self.getNextSectionOrder()
        if not parent:
            parent = "NULL"
        query = "INSERT INTO SectionView (name, description, sectionOrder, parentID) VALUES (:name, :description, :order, :parent)"
        q1 = Sql.QSqlQuery()
        q1.prepare(query)
        q1.bindValue(":name", name)
        q1.bindValue(":description", description)
        q1.bindValue(":order", order)
        q1.bindValue(":parent", parent)
        q1.exec_()
        self.bind()

    def deleteSection(self, sectionID=None):
        if not sectionID:
            index = self.selectionModel().currentIndex().row()
            if index == -1:
                return
            sectionID = self.model.record(index).field("sectionID").value()

        query = "DELETE FROM SectionView WHERE sectionID = :section"
        q1 = Sql.QSqlQuery()
        q1.prepare(query)
        q1.bindValue(":section", sectionID)
        q1.exec_()
        self.bind()

    def getNextSectionName(self):
        query = "SELECT MAX(sectionOrder) FROM Section"
        q1 = Sql.QSqlQuery(query)
        if(q1.first()):
            return "Chapter {}".format(int(q1.value(0)) + 1)
        else:
            return "Chapter 1"

    def getNextSectionOrder(self):
        query = "SELECT MAX(sectionOrder) FROM Section"
        q1 = Sql.QSqlQuery(query)
        if(q1.first()):
            return int(q1.value(0)) + 1
        else:
            return 1

    def openRCMenu(self, position):
        menu = Q.QMenu()
        deleteAct = menu.addAction("Delete")
        deleteAct.triggered.connect(self.deleteSection)
        menu.addAction("Move Up")
        menu.addAction("Move Down")
        menu.exec_(self.viewport().mapToGlobal(position))

    def rowSelected(self):
        index = self.selectionModel().currentIndex().row()
        if index == -1:
            return
        sectionID = self.model.record(index).field("sectionID").value()
        # TODO: parent parent parent parent is bad
        self.parent().parent().parent().parent().sceneList.update(sectionID)


class SceneListView(Q.QTableView):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        self.bind()
        self.sectionID = None

    def initUI(self):
        self.model = Sql.QSqlQueryModel(self)
        self.setModel(self.model)
        self.horizontalHeader().setStretchLastSection(True)

        # TODO: set drag/drop options
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(Q.QAbstractItemView.InternalMove)
        self.setSelectionMode(Q.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(Q.QAbstractItemView.SelectRows)

        # on doubleclick, open scene window
        self.doubleClicked.connect(self.openSceneWindow)

    def openSceneWindow(self):
        index = self.selectionModel().currentIndex().row()
        if index == -1:
            return
        sceneID = self.model.record(index).field("sceneID").value()
        self.window = SceneWindow(sceneID, self)
        self.window.show()

    def update(self, sectionID=None):
        if sectionID:
            self.sectionID = sectionID
        elif self.sectionID:
            sectionID = self.sectionID
        else:
            self.bind()
            return
        query = "SELECT s.sceneID, s.title, r.name, s.description, s.revisionID, s.sectionID, s.sceneOrder FROM Scene s JOIN Revision r ON s.revisionID = r.revisionID WHERE s.sectionID = {} ORDER BY s.sceneOrder".format(
            sectionID)
        self.model.setQuery(query)
        self.setModel(self.model)

    def bind(self):
        query = "SELECT s.sceneID, s.title, r.name, s.description, s.revisionID, s.sectionID, s.sceneOrder FROM Scene s JOIN Revision r ON s.revisionID = r.revisionID ORDER BY s.sceneOrder"
        self.model.setQuery(query)
        self.model.setHeaderData(1, Align.Horizontal, "Title")
        self.model.setHeaderData(3, Align.Horizontal, "Description")
        self.model.setHeaderData(2, Align.Horizontal, "Revision")
        self.setColumnHidden(0, True)
        self.setColumnHidden(4, True)
        self.setColumnHidden(5, True)
        self.setColumnHidden(6, True)
        self.setModel(self.model)
