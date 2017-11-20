import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow

# gdb = db("test.db")


def main():
    # global gdb
    app = QApplication(sys.argv)
    # scene = SceneM/odel(gdb, 1)
    # character = CharacterModel(gdb, 1)
    # characterWindow = CharacterWindow(character)
    # mainWindow = SceneWindow(1)
    mainWindow = MainWindow()

    # characterWindow.show()
    mainWindow.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
