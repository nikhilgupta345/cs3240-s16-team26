import sys
import os
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT
import psycopg2
import csv
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA256
#import django
from django.core.wsgi import get_wsgi_application
from django.contrib.auth import authenticate

####This part is to get the standAlone to access our Django Project####

#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#sys.path.append(BASE_DIR)

#os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "safecollab.settings")

application = get_wsgi_application()

####End accessing django, beginning of stand-alone app####


PG_USER = "postgres"
PG_USER_PASS = "liamjd"
PG_HOST_INFO = ""
PG_DATABASE = "testdb"

def authenticate_login(username, password):
    """conn = psycopg2.connect("dbname=" + PG_DATABASE  + " user=" + PG_USER + " password=" + PG_USER_PASS + PG_HOST_INFO)
    cur1 = conn.cursor()
    cur2 = conn.cursor()
    cur1.execute('SELECT username FROM auth_user')
    cur2.execute('SELECT password FROM auth_user')"""
    user = authenticate(username=username, password=password)
    if user is not None:
        # the password verified for the user
        if user.is_active:
            return True
        else:
            print("The password is valid, but the account has been disabled!")
    else:
        # the authentication system was unable to verify the username and password
        print("The username and password were incorrect.")
    """usr = False
    pas = False
    for user in cur1.fetchall():
        print(user)
        if user == username:
            usr = True
    for passw in cur2.fetchall():
        print(passw)
        if passw == password:
            pas = True
    if usr and pas:
        return True
    else:
        return False"""

class LoginWindow(QtGui.QWidget):

    def __init__(self):
        super(LoginWindow, self).__init__()
        self.resize(600, 400)
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
            user = self.userName.text()
            self.mainWindow = Window(user)
            self.mainWindow.show()
            self.close()
        else:
            incorrect = QtGui.QLabel("Invalid username or password. Please try again.", self)
            incorrect.resize(incorrect.sizeHint())
            incorrect.move(170, 270)
            incorrect.show()


class FileItem(QtGui.QListWidgetItem):

    def __init__(self, filename, key):
        QtGui.QListWidgetItem.__init__(self, filename)
        self.filename = filename
        self.key = key

class Report(QtGui.QListWidgetItem):
    def __init__(self, title, owner, report_files, short_desc):
        QtGui.QListWidgetItem.__init__(self, title)
        self.owner = owner
        self.report_files = report_files
        self.short_desc = short_desc


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
            item = FileItem('', '')
            file = files.item(i)
            encrypted = self.encrypt_file(file.filename, file.key)
            item.filename = (str(encrypted)[26:len(str(encrypted)) - 2])
            item.setText(item.filename)
            item.key = None
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.addItem(item)
            i += 1

    def encrypt_file(self, file_name, symm_key):
        hash_key = SHA256.new()
        hash_key.update(symm_key)
        key_size16 = hash_key.digest()[0:16]
        try:
            fout = open(file_name + '.enc', 'wb')

            text = ''
            with open(file_name, 'rb') as f:
                text = f.read()


            enc = AES.new(key_size16, AES.MODE_CFB, b'abcdefghijklmnop')
            final_string = enc.encrypt(text)

            fout.write(final_string)

            fout.close()

            return fout
        except IOError as ex:
            print("IO Error. File not valid.")
            return False
        except ValueError as ex:
            print(ex)
            print("Invalid key.")
            return False

    def decrypt_file(self, file_name, symm_key):
        hash_key = SHA256.new()
        hash_key.update(symm_key)
        key_size16 = hash_key.digest()[0:16]
        totaltext = ''
        try:
            with open(file_name, 'rb') as f:
                totaltext = f.read()

            dec = AES.new(key_size16, AES.MODE_CFB, b'abcdefghijklmnop')
            plaintext = dec.decrypt(totaltext)

            #print(plaintext)

            index = file_name.rindex("/")
            newfile = file_name[:index+1] + "DEC_" + file_name[index+1:-4]
            fout = open(newfile, 'wb')
            fout.write(plaintext)
            fout.close()
            return fout
        except FileNotFoundError as ex:
            print(ex)
            print("File not found.")
        except UnicodeDecodeError as ex:
            print("Unicode Decode Error.")
        except ValueError as ex:
            print("Invalid Key Provided.")

    def decrypt_files(self, files):
        #Add decryption algorithm
        i = 0
        while i < files.count():
            item = files.item(i)
            #random_generator = Random.new().read
            #key = RSA.generate(1024, 1246832)
            #public = key.publickey()
            """key2 = self.key_input()
            if key2 != item.key:
                print(item.key)
                print(key2)
                print("Invalid Key.")
                break"""
            j = 0
            same = False
            while j < self.count():
                if files.item(i).text() == self.item(j).text():
                    same = True
                    break
                j += 1
            i += 1
            if item.checkState() == QtCore.Qt.Checked:
                decrypted = self.decrypt_file(item.text(), item.key)
                self.addItem(str(decrypted)[26:len(str(decrypted))-2])

    def key_input(self, fileItem):
        self.keyIn2 = KeyInput()
        self.keyIn2.show()
        self.keyIn2.key.returnPressed.connect(lambda: self.set_key(self.secret_string2(self.keyIn2.key.text()), fileItem, self.keyIn2))

    def set_key(self, key, fileItem, keyIn):
        fileItem.key = key
        keyIn.close()

    def secret_string2(self, string):
        """encoded_string = public_key.encrypt(str.encode(string), 32)
        return encoded_string"""
        b = bytes(string, ('utf-8'))
        #enc_data = public_key.encrypt(b, None)
        return b

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

    @pyqtSlot(QtGui.QListWidgetItem)
    def doubleClickedSlot2(self, item):
        self.key_input(item)

class Window(QtGui.QMainWindow):

    def __init__(self, username):
        super(Window, self).__init__()
        self.username = username
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
        encBtn.move(385, 250)
        encBtn.clicked.connect(self.add_encrypted_files)

        decBtn = QtGui.QPushButton("Decrypt Files", self)
        decBtn.resize((decBtn.sizeHint()))
        decBtn.move(520, 250)
        decBtn.clicked.connect(self.decrypt_all_files)

        """uplAllBtn = QtGui.QPushButton("Download Enc Files", self)
        uplAllBtn.resize(uplAllBtn.sizeHint())
        uplAllBtn.move(100, 515)
        uplAllBtn.clicked.connect(self.download_files)"""

        dlBtn = QtGui.QPushButton("Download Dec Files", self)
        dlBtn.resize(dlBtn.sizeHint())
        dlBtn.move(780, 515)
        dlBtn.clicked.connect(self.download_files)

        reports = QtGui.QLabel("Reports", self)
        reports.resize(reports.sizeHint())
        reports.move(140, 75)

        decFiles = QtGui.QLabel("Decrypted Files", self)
        decFiles.resize(decFiles.sizeHint())
        decFiles.move(790, 75)

        self.report_files = FileList(self)
        self.report_files.resize(250, 150)
        self.report_files.move(375, 350)

        rep_files = QtGui.QLabel("Report Files", self)
        rep_files.resize(rep_files.sizeHint())
        rep_files.move(465, 330)

        self.short_desc = QtGui.QTextEdit(self)
        self.short_desc.setReadOnly(True)
        self.short_desc.resize(250, 100)
        self.short_desc.move(375, 100)

        sh_desc = QtGui.QLabel("Short Description", self)
        sh_desc.resize(sh_desc.sizeHint())
        sh_desc.move(455, 80)

        self.reportList.move(20, 100)
        self.reportList.resize(300, 400)
        self.decList.move(680, 100)
        self.decList.resize(300, 400)
        self.reportList.setAcceptDrops(False)
        self.reportList.setDragEnabled(False)
        self.decList.setAcceptDrops(False)
        self.decList.setDragEnabled(False)
        self.report_files.connect(self.report_files,SIGNAL("itemDoubleClicked(QListWidgetItem*)"),
                                self.report_files,SLOT("doubleClickedSlot2(QListWidgetItem*)"))
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
        if filename:
            #random_generator = Random.new().read
            #key = RSA.generate(1024, 1246832)
            #public = key.publickey()
            self.keyIn = KeyInput()
            self.keyIn.show()
            self.keyIn.key.returnPressed.connect(lambda: self.files.create_enc_object(filename, self.secret_string(self.keyIn.key.text()), self.keyIn))
        #self.files.encFiles.addFile(filename)
        self.files.addFilesBtn.clicked.connect(self.encrypt_All_Files)

    def open_file(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Load File', '')

    def secret_string(self, string):
        """encoded_string = public_key.encrypt(str.encode(string), 32)
        return encoded_string"""
        b = bytes(string,('utf-8'))
        #enc_data = public_key.encrypt(b, None)
        return b

    def encrypt_All_Files(self):
        #Add encryption algorithm using key field of fileItem object
        """i = 0
        while i < self.files.encFiles.count():
            file = self.files.encFiles.item(i)
            print(file.filename)
            print(file.key[0])
            print(sys.getsizeof(file.key[0]))
            encrypted = QtGui.QListWidgetItem()
            encrypted = self.encrypt_file(file.filename, file.key[0])
            self.reportList.addItem(str(encrypted)[26:len(str(encrypted)) - 2])
            i += 1"""
        self.report_files.addFiles(self.files.encFiles)
        self.files.close()
        self.show()

    #To do
    def decrypt_all_files(self):
        self.decList.decrypt_files(self.report_files)


class KeyInput(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.resize(300, 200)
        self.key = QtGui.QLineEdit(self)
        self.key.resize(150, 22)
        self.key.move(80, 100)
        self.label = QtGui.QLabel("Please enter the public key.", self)
        self.label.resize(self.label.sizeHint())
        self.label.move(78, 75)


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
        if filename:
            self.keyIn = KeyInput()
            self.keyIn.show()
            self.keyIn.key.returnPressed.connect(lambda: self.create_enc_object(filename, self.keyIn.key.text(), self.keyIn))

    def create_enc_object(self, filename, key, keyIn):
        fileIt = FileItem(filename, key)
        keyIn.close()
        self.encFiles.addItem(fileIt)

if __name__ == "__main__":
    #load_user_database("users.csv")
    app = QtGui.QApplication(sys.argv)
    #w = Window()
    #w.show()
    lg = LoginWindow()
    lg.show()
    #k = KeyInput()
    #k.show()
    sys.exit(app.exec_())