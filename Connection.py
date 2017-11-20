from PyQt5 import QtSql as Sql


def getConnection():
    db = Sql.QSqlDatabase.database()
    if not db.isValid():
        db = Sql.QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("test.db")
        db.open()
    return db
