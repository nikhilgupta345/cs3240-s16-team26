import sys
import os
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT
import psycopg2
import csv

PG_USER = "postgres"
PG_USER_PASS = "liamjd"
PG_HOST_INFO = ""
PG_DATABASE = "testdb"
reports = []

def load_user_database(csv_filename):
    conn = psycopg2.connect("dbname=" + PG_DATABASE + " user=" + PG_USER + " password=" + PG_USER_PASS + PG_HOST_INFO)
    cur = conn.cursor()
    with open(csv_filename, 'rU') as csvfile:
        filtered = (line.replace('\n', '') for line in csvfile)
        reader = csv.reader(csvfile)
        for row in csv.reader(filtered):
            #l_info = tuple(item for item in row.split(',') if item.strip())
            l_info = tuple(row)
            query = """INSERT INTO logininfo VALUES %s returning *"""
            cur.execute(query, (l_info,))
            conn.commit()

def authenticate_login(username, password):
    conn = psycopg2.connect("dbname=" + PG_DATABASE  + " user=" + PG_USER + " password=" + PG_USER_PASS + PG_HOST_INFO)
    cur = conn.cursor()
    cur.execute('SELECT * FROM logininfo')
    usr = False
    pas = False
    for login in cur.fetchall():
        if login[0] == username:
            usr = True
        if login[1] == password:
            pas = True
    if usr and pas:
        return True
    else:
        return False


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
        if authenticate_login(self.userName.text(), self.password.text()):
            self.mainWindow = Window()
            self.mainWindow.show()
            self.close()
        else:
            incorrect = QtGui.QLabel("Invalid username or password. Please try again.", self)
            incorrect.resize(incorrect.sizeHint())
            incorrect.move(170, 270)
            incorrect.show()


class FileItem(QtGui.QListWidgetItem):

    def __init__(self, filename):
        QtGui.QListWidgetItem.__init__(self, filename)
        self.fullFile = filename
        i = str(self.fullFile).rindex("/")
        self.trncFileName = self.fullFile[i+1:]


class FileList(QtGui.QListWidget):

    def __init__(self, parent=None):
        #QtGui.QListWidget.__init__(self, parent)
        super(FileList, self).__init__(parent)
        #self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.setAcceptDrops(True)
        #self.setIconSize(QtCore.QSize(72, 72))

    def addFile(self, file):
        """Might have to change this to accomodate full filename in order to execute opening files"""
        if file:
            #newFile = FileItem(file)
            newFile = QtGui.QListWidgetItem()
            #newFile.setFlags(QtCore.Qt.ItemIsUserCheckable)
            #newFile.setCheckState(QtCore.Qt.Unchecked)
            newFile.setText(file)
            self.addItem(newFile)

    def addFiles(self, files):
        i = 0
        while i < files.count():
            item = QtGui.QListWidgetItem()
            item.setText(files.item(i).text())
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.addItem(item)
            i += 1

    def decrypt_files(self, files):
        #Add decryption algorithm
        i = 0
        while i < files.count():
            item = files.item(i)
            j = 0
            same = False
            while j < self.count():
                if files.item(i).text() == self.item(j).text():
                    same = True
                    break
                j += 1
            if item.checkState() == QtCore.Qt.Checked and not same:
                self.addItem(item.text())
            i += 1

    #Get Drag and Drop working
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.emit(QtCore.SIGNAL("dropped"), links)
        else:
            event.ignore()

    def decryptFile(self):
        #Decryption stuff
        return True

    @pyqtSlot(QtGui.QListWidgetItem)
    def doubleClickedSlot(self, item):
        os.startfile(item.text())


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

        encBtn = QtGui.QPushButton("Encrypt Files", self)
        encBtn.resize((encBtn.sizeHint()))
        encBtn.move(450, 200)
        encBtn.clicked.connect(self.add_encrypted_files)

        decBtn = QtGui.QPushButton("Decrypt Files", self)
        decBtn.resize((decBtn.sizeHint()))
        decBtn.move(450, 275)
        decBtn.clicked.connect(self.decrypt_all_files)

        uplAllBtn = QtGui.QPushButton("Upload Files to Safecollab", self)
        uplAllBtn.resize(uplAllBtn.sizeHint())
        uplAllBtn.move(90, 515)
        uplAllBtn.clicked.connect(self.upload_files_to_Heroku)

        dlBtn = QtGui.QPushButton("Download Files", self)
        dlBtn.resize(dlBtn.sizeHint())
        dlBtn.move(780, 515)
        dlBtn.clicked.connect(self.download_files)

        encFiles = QtGui.QLabel("Encrypted Files", self)
        encFiles.resize(encFiles.sizeHint())
        encFiles.move(120, 75)

        decFiles = QtGui.QLabel("Decrypted Files", self)
        decFiles.resize(decFiles.sizeHint())
        decFiles.move(790, 75)

        self.reportList.move(20, 100)
        self.reportList.resize(300, 400)
        self.decList.move(680, 100)
        self.decList.resize(300, 400)
        self.reportList.setAcceptDrops(False)
        self.reportList.setDragEnabled(False)
        self.decList.setAcceptDrops(False)
        self.decList.setDragEnabled(False)
        self.reportList.connect(self.reportList,SIGNAL("itemDoubleClicked(QListWidgetItem*)"),
                                self.reportList,SLOT("doubleClickedSlot(QListWidgetItem*)"))
        self.decList.connect(self.decList,SIGNAL("itemDoubleClicked(QListWidgetItem*)"),
                                self.decList,SLOT("doubleClickedSlot(QListWidgetItem*)"))

    def close_application(self):
        sys.exit()

    #To do
    def upload_files_to_Heroku(self):
        return True

    #To do
    def download_files(self):
        return True

    def add_encrypted_files(self):
        self.files = AddFileDialog()
        self.hide()
        self.files.move(1400, 217)
        self.files.show()
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Load File', '')
        self.files.encFiles.addFile(filename)
        self.files.addFilesBtn.clicked.connect(self.encrypt_Files)

    def open_file(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Load File', '')

    def encrypt_Files(self):
        self.reportList.addFiles(self.files.encFiles)
        self.files.close()
        self.show()

    #To do
    def decrypt_all_files(self):
        self.decList.decrypt_files(self.reportList)


class AddFileDialog(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.resize(400, 600)
        self.encFiles = FileList(self)
        self.encFiles.resize(300, 400)
        self.encFiles.move(50, 75)

        self.addFilesBtn = QtGui.QPushButton("Add to Encrypted Files", self)
        self.addFilesBtn.resize(self.addFilesBtn.sizeHint())
        self.addFilesBtn.move(200, 485)

        self.moreFilesBtn = QtGui.QPushButton("Upload Files", self)
        self.moreFilesBtn.resize(self.moreFilesBtn.sizeHint())
        self.moreFilesBtn.move(80, 485)
        self.moreFilesBtn.clicked.connect(self.upload_files)
        self.connect(self.encFiles, QtCore.SIGNAL("dropped"), self.pictureDropped)

    def pictureDropped(self, l):
        for url in l:
            if os.path.exists(url):
                print(url)
                icon = QtGui.QIcon(url)
                pixmap = icon.pixmap(72, 72)
                icon = QtGui.QIcon(pixmap)
                item = QtGui.QListWidgetItem(url, self.encFiles)
                item.setIcon(icon)
                item.setStatusTip(url)

    def upload_files(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Load File', '')
        self.encFiles.addItem(filename)

if __name__ == "__main__":
    load_user_database("users.csv")
    app = QtGui.QApplication(sys.argv)
    #w = Window()
    #w.show()
    lg = LoginWindow()
    lg.show()
    sys.exit(app.exec_())