import sys
from PyQt5 import QtWidgets
from ui.main import MainWindow


class CurlingLeague:
    pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
