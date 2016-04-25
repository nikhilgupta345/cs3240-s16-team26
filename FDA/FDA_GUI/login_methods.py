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


    """def login(self):
        if authenticate_login(self.userName.text(), self.password.text()):
            self.mainWindow = Window()
            self.mainWindow.show()
            self.close()
        else:
            incorrect = QtGui.QLabel("Invalid username or password. Please try again.", self)
            incorrect.resize(incorrect.sizeHint())
            incorrect.move(170, 270)
            incorrect.show()"""
