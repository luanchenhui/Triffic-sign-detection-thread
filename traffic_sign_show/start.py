import sys
from PyQt5 import QtWidgets

from main import Ui_MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    start_window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()

    ui.setupUi(start_window)
    start_window.show()
    sys.exit(app.exec_())
