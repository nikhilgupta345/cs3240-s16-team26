import sys
from PyQt4 import QtGui, QtCore

class LoginPage(QtGui.QWidget):
    def __init__(self, parent=None):
        super(LoginPage, self).__init__(parent)

        self.initUI()

    def initUI(self):
        btn = QtGui.QPushButton(self)
        btn.setText("Login")
        btn.move(210, 125)
        btn.clicked.connect(self.on_pushButton_clicked)

        self.resize(500,250)
        self.center()

        self.displayPage = None

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @QtCore.pyqtSlot()
    def on_pushButton_clicked(self):
        if self.displayPage == None:
            self.displayPage = DisplayPage()
        self.displayPage.show()


class DisplayPage(QtGui.QMainWindow):
    def __init__(self):
        super(DisplayPage, self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(500, 250)
        self.center()
        self.statusBar().showMessage('Ready')

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('FDA')

    main = LoginPage()
    main.show()

    sys.exit(app.exec_())