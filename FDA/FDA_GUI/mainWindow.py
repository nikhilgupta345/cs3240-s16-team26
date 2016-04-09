import sys
import os
from PyQt4 import QtGui, QtCore

class LoginWindow(QtGui.QWidget):

    def __init__(self):
        super(LoginWindow, self).__init__()
        self.resize(600, 400)
        """layout = QtGui.QVBoxLayout()
        layout2 = QtGui.QVBoxLayout()
        layout.addStretch(0.5)
        usr = QtGui.QLabel("Username")
        passw = QtGui.QLabel("Password")
        self.userName = QtGui.QLineEdit(self)
        self.password = QtGui.QLineEdit(self)
        self.loginBtn = QtGui.QPushButton("Login", self)
        self.usr = QtGui.QLabel("Username")
        self.pas = QtGui.QLabel("Password")
        #self.loginBtn.setSizePolicy(25, 100)
        layout.addWidget(self.userName)
        layout.addWidget(self.password)
        layout.addWidget(self.loginBtn)
        layout.setSpacing(30)
        self.setLayout(layout)"""
        usr = QtGui.QLabel("Username")
        passw = QtGui.QLabel("Password")
        self.userName = QtGui.QLineEdit(self)
        self.password = QtGui.QLineEdit(self)
        self.loginBtn = QtGui.QPushButton("Login", self)
        self.usr = QtGui.QLabel("Username", self)
        self.pas = QtGui.QLabel("Password", self)
        self.userName.resize(200, 25)
        self.userName.move(200, 150)
        self.password.resize(200, 25)
        self.password.move(200, 200)
        self.loginBtn.resize(100, 25)
        self.loginBtn.move(255, 240)
        self.usr.resize(70, 25)
        self.usr.move(130, 150)
        self.pas.resize(70, 25)
        self.pas.move(133, 200)
        self.setWindowTitle("Login")
        self.password.setEchoMode(2)

        self.loginBtn.clicked.connect(self.login)

    def login(self):
        #Insert authentication stuff here
        print(self.userName.text())
        print(self.password.text())
        self.mainWindow = Window()
        self.mainWindow.show()
        self.close()

class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.resize(1000, 600)
        self.setWindowTitle("File Download Application")
        """self.setWindowIcon(QtGui.QIcon(filename))"""

        self.fileList = []

        extractAction = QtGui.QAction("&Exit", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Leave the app.')
        extractAction.triggered.connect(self.close_application)

        openFile = QtGui.QAction("&Open", self)
        openFile.setShortcut("Ctrl+O")
        openFile.setStatusTip("Open a file.")
        openFile.triggered.connect(self.open_file)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(extractAction)

        self.reportList = FileList(self)
        self.decList = FileList(self)

        self.setupUI()

    def setupUI(self):
        addFileBtn = QtGui.QPushButton("Add File", self)
        addFileBtn.resize(addFileBtn.sizeHint())
        addFileBtn.move(120, 500)
        uplAllBtn = QtGui.QPushButton("Upload Files to Safecollab", self)
        uplAllBtn.resize(uplAllBtn.sizeHint())
        uplAllBtn.move(320, 270)
        encFiles = QtGui.QLabel("Encrypted Files", self)
        encFiles.resize(encFiles.sizeHint())
        encFiles.move(120, 75)
        decFiles = QtGui.QLabel("Decrypted Files", self)
        decFiles.resize(decFiles.sizeHint())
        decFiles.move(790, 75)
        #newFile = FileWidget(filename)
        #item = QtGui.QListWidgetItem()
        self.reportList.move(20, 100)
        self.reportList.resize(300, 400)
        self.decList.move(680, 100)
        self.decList.resize(300, 400)
        addFileBtn.clicked.connect(self.open_file)
        uplAllBtn.clicked.connect(self.upload_files)
        self.reportList.setAcceptDrops(False)
        #self.reportList.connect(file, QtCore.SIGNAL('itemDoubleClicked'), self.openFileItem(file))

    def close_application(self):
        sys.exit()

    def open_file(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Load File', '')
        """Encryption stuff here"""
        self.reportList.addFile(filename)

    def openFileItem(self, file):
        os.startfile(file)

    def upload_files(self):
        return True

class FileList(QtGui.QListWidget):

    def __init__(self, parent=None):
        QtGui.QListWidget.__init__(self, parent)
        self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.setAcceptDrops(True)

    def addFile(self, file):
        """Might have to change this to accomodate full filename in order to execute opening files"""
        if file:
            newFile = FileItem(file)
            self.addItem(newFile.trncFileName)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            super(FileList, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            super(FileList, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
                links.append("Hi")
            self.emit(QtCore.SIGNAL("dropped"), links)
        else:
            event.setDropAction(QtCore.Qt.MoveAction)
            super(FileList, self).dropEvent(event)

    def decryptFile(self):
        #Decryption stuff
        return True

class FileItem(QtGui.QListWidgetItem):

    def __init__(self, filename):
        QtGui.QListWidgetItem.__init__(self, filename)
        self.fullFile = filename
        i = str(self.fullFile).rindex("/")
        self.trncFileName = self.fullFile[i+1:]

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    #w = Window()
    #w.show()
    lg = LoginWindow()
    lg.show()
    sys.exit(app.exec_())