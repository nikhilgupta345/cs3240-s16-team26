import sys
import os
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from django.core.wsgi import get_wsgi_application
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import requests

####This part is to get the standAlone to access our Django Project####

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "safecollab.settings")

application = get_wsgi_application()

fs = FileSystemStorage(location = '/media/')

base_path = "http://127.0.0.1:8000/"

####End accessing django, beginning of stand-alone app####


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

    #Login check to verify credentials and load user's specific FDA
    def login(self):
        username = self.userName.text()
        password = self.password.text()
        user = authenticate(username=username, password=password)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                self.mainWindow = Window(user)
                self.mainWindow.show()
                self.close()
        else:
            incorrect = QtGui.QLabel("Invalid username or password. Please try again.", self)
            incorrect.resize(incorrect.sizeHint())
            incorrect.move(170, 270)
            incorrect.show()


#Class to store file information for encrytion and decryption
class FileItem(QtGui.QListWidgetItem):

    def __init__(self, filename, key, id):
        QtGui.QListWidgetItem.__init__(self, filename)
        self.filename = filename
        self.key = key
        self.id = id

#Class to store report information when pulled from the server
class Report(QtGui.QListWidgetItem):
    def __init__(self, title, owner, report_files, long_desc):
        QtGui.QListWidgetItem.__init__(self, title)
        self.owner = owner
        self.report_files = report_files
        self.long_desc = long_desc
        self.id = id


#Class to store different kinds of information to be displayed to the user
class FileList(QtGui.QListWidget):

    def __init__(self, parent=None):
        super(FileList, self).__init__(parent)
        self.setAcceptDrops(True)

    #Adds a single file after converting it to a QListWidgetItem
    def addFile(self, file):
        if file:
            newFile = QtGui.QListWidgetItem()
            newFile.setText(file)
            self.addItem(newFile)

    #Adds all files from a given FileList into another FileList after encrypting them
    def addFiles(self, files, report):
        i = 0
        while i < files.count():
            item = FileItem('', '', None)
            file = files.item(i)
            encrypted = self.encrypt_file(file.filename, file.key)
            item.filename = (str(encrypted)[26:len(str(encrypted)) - 2])
            item.setText(item.filename)
            item.key = None
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)
            #self.addItem(item)
            report.report_files.append(item)
            i += 1

    #Encryption algorithm for files
    def encrypt_file(self, file_name, symm_key):
        hash_key = SHA256.new()
        hash_key.update(symm_key)
        key_size16 = hash_key.digest()[0:16]
        print(key_size16)
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

    #Decryption algorithm for files
    def decrypt_file(self, file_name, symm_key):
        if symm_key == None:
            print("Do the thing.")
            raise TypeError
        hash_key = SHA256.new()
        hash_key.update(symm_key)
        key_size16 = hash_key.digest()[0:16]
        key_size16.decode("Latin-1")
        print(key_size16)
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
        except TypeError as ty:
            print("Do the thing.")

    #Decrypts all "checked" files from the report_list
    def decrypt_files(self, files):
        i = 0
        while i < files.count():
            item = files.item(i)
            j = 0
            same = False
            while j < self.count():
                newName1 = files.item(i).text()[0:len(files.item(i).text())-4]
                newName2 = self.item(j).text()[0:29] + self.item(j).text()[33:len(self.item(j).text())]
                if newName1 == newName2:
                    same = True
                    break
                j += 1
            i += 1
            if item.key == None and item.checkState() == QtCore.Qt.Checked:
                break
            if item.checkState() == QtCore.Qt.Checked and not same:
                decrypted = self.decrypt_file(item.text(), item.key)
                self.addItem(str(decrypted)[26:len(str(decrypted))-2])

    """def raiseKeyError(self, window):
        incorrectKey = QtGui.QLabel("Please set the decryption key", window)
        incorrectKey.resize(incorrectKey.sizeHint())
        incorrectKey.move(600, 600)"""

    #Opens a key_input window to set decryption key for a file
    def key_input(self, fileItem):
        self.keyIn2 = KeyInput()
        self.keyIn2.show()
        self.keyIn2.key.returnPressed.connect(lambda: self.set_key(self.secret_string2(self.keyIn2.key.text()), fileItem, self.keyIn2))

    #Sets decryption key for a given file
    def set_key(self, key, fileItem, keyIn):
        fileItem.key = key
        keyIn.close()

    #Converts encryption/decryption key into bytes object
    def secret_string2(self, string):
        b = bytes(string, ('utf-8'))
        return b

    #Custom slot for when specific FileList is double clicked
    @pyqtSlot(QtGui.QListWidgetItem)
    def doubleClickedSlot(self, item):
        os.startfile(item.text())

    #Custom slot for when specific FileList is double clicked
    @pyqtSlot(QtGui.QListWidgetItem)
    def doubleClickedSlot2(self, item):
        self.key_input(item)

    #Custom slot for when specific FileList is single clicked
    @pyqtSlot(QtGui.QListWidgetItem)
    def singleClickedSlot(self, encFiles, sh_desc):
        i = 0
        while i < encFiles.count():
            item = encFiles.item(i)
            if item != None:
                encFiles.takeItem(i)
        sh_desc.setText(self.currentItem().long_desc)
        for x in self.currentItem().report_files:
            print(isinstance(x, dict))
            if isinstance(x, dict):
                if x['name'] == "":
                    x['name'] = "Unnamed"
                file = FileItem(x['name'], None, x['id'])
                file.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                file.setCheckState(QtCore.Qt.Unchecked)
                encFiles.addItem(file)
            else:
                encFiles.addItem(x)

#Main GUI window class
class Window(QtGui.QMainWindow):

    def __init__(self, username):
        super(Window, self).__init__()
        self.username = username
        self.resize(1000, 600)
        self.setWindowTitle("File Download Application")

        #Sets menu bar option for exiting
        extractAction = QtGui.QAction("&Exit", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Leave the app.')
        extractAction.triggered.connect(self.close_application)

        #Sets menu bar option for opening a file
        openFile = QtGui.QAction("&Open", self)
        openFile.setShortcut("Ctrl+O")
        openFile.setStatusTip("Open a file.")
        openFile.triggered.connect(self.open_file)

        #Creates a status bar in the GUI
        self.statusBar()

        #Creates a menu bar and populates it with defined options
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(extractAction)

        #Defines two main FileLists of the GUI
        self.reportList = FileList(self)
        self.decList = FileList(self)

        #Helper method to extend construction
        self.setupUI()

    def setupUI(self):

        #Push button to open file encryption window
        encBtn = QtGui.QPushButton("Encrypt Files", self)
        encBtn.resize((encBtn.sizeHint()))
        encBtn.move(385, 250)
        encBtn.clicked.connect(self.add_encrypted_files)

        #Push button to decrypt all checked files with set decryption key
        decBtn = QtGui.QPushButton("Decrypt Files", self)
        decBtn.resize((decBtn.sizeHint()))
        decBtn.move(520, 250)
        decBtn.clicked.connect(self.decrypt_all_files)

        #Push button to download all files associated with a given report
        dlBtn = QtGui.QPushButton("Download Enc Files", self)
        dlBtn.resize(dlBtn.sizeHint())
        dlBtn.move(445, 515)
        dlBtn.clicked.connect(self.download_files)

        reports = QtGui.QLabel("Reports", self)
        reports.resize(reports.sizeHint())
        reports.move(140, 75)

        decFiles = QtGui.QLabel("Decrypted Files", self)
        decFiles.resize(decFiles.sizeHint())
        decFiles.move(790, 75)

        #Creates FileList to hold all files associated with a given report
        self.report_files = FileList(self)
        self.report_files.resize(250, 150)
        self.report_files.move(375, 350)

        rep_files = QtGui.QLabel("Report Files", self)
        rep_files.resize(rep_files.sizeHint())
        rep_files.move(465, 330)

        #Creates a text edit box to contain description of report
        self.desc = QtGui.QTextEdit(self)
        self.desc.setReadOnly(True)
        self.desc.resize(250, 100)
        self.desc.move(375, 100)

        l_desc = QtGui.QLabel("Description", self)
        l_desc.resize(l_desc.sizeHint())
        l_desc.move(470, 80)

        self.reportList.move(20, 100)
        self.reportList.resize(300, 400)
        self.decList.move(680, 100)
        self.decList.resize(300, 400)
        self.reportList.setAcceptDrops(False)
        self.reportList.setDragEnabled(False)
        self.decList.setAcceptDrops(False)
        self.decList.setDragEnabled(False)

        #Connect all FileLists to appropriate slots
        self.report_files.connect(self.report_files,SIGNAL("itemDoubleClicked(QListWidgetItem*)"),
                                self.report_files,SLOT("doubleClickedSlot2(QListWidgetItem*)"))
        self.decList.connect(self.decList,SIGNAL("itemDoubleClicked(QListWidgetItem*)"),
                                self.decList,SLOT("doubleClickedSlot(QListWidgetItem*)"))
        self.reportList.itemClicked.connect(lambda: self.reportList.singleClickedSlot(self.report_files, self.desc))

        #Populate FileLists with reports from server
        self.populate_reports()


        """file1 = FileItem("C:/Users/liamj_000/Downloads/addition.ibcm.txt", None)
        file1.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        file1.setCheckState(QtCore.Qt.Unchecked)
        self.report_files.addItem(file1)"""

    #Get all public reports and private reports associated with this user and input them into the GUI
    def populate_reports(self):
        r = requests.get(base_path + "standalone_report_list/" + str(self.username))
        report_list = r.json()
        for report in report_list:
            report1 = Report(report['short_desc'], report['owner'], report['files'], report['long_desc'])
            self.reportList.addItem(report1)

    #Exit application
    def close_application(self):
        sys.exit()

    #Download all files in report_files. Must be done before decryption can occur
    def download_files(self):
        i = 0
        while i < self.report_files.count():
            r = requests.get(base_path + "download/" + str(self.report_files.item(i).id))
            i += 1

    #Open add file window for file encryption
    def add_encrypted_files(self):
        self.files = AddFileDialog()
        self.hide()
        self.files.move(1400, 217)
        self.files.show()
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Load File', '')
        if filename:
            self.keyIn = KeyInput()
            self.keyIn.show()
            self.keyIn.key.returnPressed.connect(lambda: self.files.create_enc_object(filename, self.secret_string(self.keyIn.key.text()), self.keyIn))
        self.files.addFilesBtn.clicked.connect(self.encrypt_All_Files)

    #Open a file dialog to open files
    def open_file(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Load File', '')

    #Convert encryption key into bytes object
    def secret_string(self, string):
        b = bytes(string,('utf-8'))
        return b

    #Calls encrypt method on all files in add file window's FileList
    def encrypt_All_Files(self):
        self.report_files.addFiles(self.files.encFiles, self.reportList.currentItem())
        self.files.close()
        self.show()

    #Calls decrypt method on all files to be decrypted
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
        fileIt = FileItem(filename, key, None)
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