from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from new_window import NewWindow
from parking_client import *
from parking_client import getQR
from parking_client import registerUser
from parking_client import sendQR
import os 
import qrcode, smtplib
from email.message import EmailMessage
import cv2



class LoginForm(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Ingresar")

        self.e1 = QLineEdit()
        self.e1.setPlaceholderText("ID")

        self.e2 = QLineEdit()
        self.e2.setPlaceholderText("Contraseña")
        self.e2.setEchoMode(QLineEdit.Password)

        b1 = QPushButton("Obtener QR")
        b1.clicked.connect(self.parent.newWindow)

        layout = QVBoxLayout()
        layout.addWidget(self.e1)
        layout.addWidget(self.e2)
        
        layout.addWidget(b1)

        self.setLayout(layout)


class RegisterForm(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Registro de Usuario")

        self.e1 = QLineEdit()
        self.e1.setPlaceholderText("ID")

        self.e2 = QLineEdit()
        self.e2.setPlaceholderText("Contraseña")
        self.e2.setEchoMode(QLineEdit.Password)

        self.e3 = QLineEdit()
        self.e3.setPlaceholderText("Role")

        self.e4 = QLineEdit()
        self.e4.setPlaceholderText("Program")

        b2 = QPushButton("Registrar")
        b2.clicked.connect(self.parent.newWindow2)

        layout = QVBoxLayout()
        layout.addWidget(self.e1)
        layout.addWidget(self.e2)
        layout.addWidget(self.e3)
        layout.addWidget(self.e4)
        layout.addWidget(b2)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Principal")

        # Botones del menú principal
        b1 = QPushButton("Ingresar")
        b2 = QPushButton("Registrar usuario")
        b3 = QPushButton("Leer código QR")

        b1.clicked.connect(self.mostrar_login)
        b2.clicked.connect(self.mostrar_registro)
        b3.clicked.connect(self.newWindow3)

        layout = QVBoxLayout()
        layout.addWidget(b1)
        layout.addWidget(b2)
        layout.addWidget(b3)

        contenedor = QWidget()
        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)
      
        gridLayout=QGridLayout()
        

        widget = QWidget()
        widget.setLayout(gridLayout)
        #QMainWindow requiere un widget central
        

        
        # Deshabilita el botón de maximizar
        self.setWindowFlags( Qt.MSWindowsFixedSizeDialogHint)
        
        self.login_form = LoginForm(self)
        self.register_form = RegisterForm(self)

    def mostrar_login(self):
        self.login_form.show()

    def mostrar_registro(self):
        self.register_form.show()
    
    def newWindow(self):
        id=self.login_form.e1.text()
        password=self.login_form.e2.text()
        
        if len(id) and len(password):
            url="http://localhost:80"

            # Solicita un código QR al servidor (los códigos QR cambian cada fecha o cuando se reinicia el servidor)
            imgBytes=getQR(url,id,password)
            if len(imgBytes):
                self.nw=NewWindow(imgBytes)
                #self.nw.show()
                msg = EmailMessage()
                msg["Subject"] = "QR"
                msg["From"] = msg["To"] = "brayanvilladam@gmail.com"
                msg.set_content("Aquí está tu QR.")
                msg.add_attachment(imgBytes, maintype="image", subtype="png", filename="qr.png")
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as g:
                    g.login(msg["From"], "tdmy jyyt chzk sgef")  
                    g.send_message(msg)
                
        
            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText("Usuario no Existe o Contraseña Incorrecta")
                msgBox.setWindowTitle("Alerta")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()

    
    def newWindow2(self):
        id=self.register_form.e1.text()
        password=self.register_form.e2.text()
        role=self.register_form.e3.text()
        Program=self.register_form.e4.text()
        
        if len(id) and len(password) and len(role) and len(Program):
            url="http://localhost:80"

            # Solicita un código QR al servidor (los códigos QR cambian cada fecha o cuando se reinicia el servidor)
            Usuario=registerUser(url,id,password,Program,role)

            if Usuario==("users succesfully registered"):
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText("Se registro exitosamente")
                msgBox.setWindowTitle("Informacion")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()

            else:
                msgBox = QMessageBox()
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText("Usuario Registrado")
                msgBox.setWindowTitle("Alerta")
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.exec()
   
    def newWindow3(self):
        import qrscan



        
            
        
        
        

   
        
        
app = QApplication([])
ex = MainWindow()
ex.show()
app.exec()