"""Identificación de código QR válido"""
"""Alexander López Parrado"""

# Módulos de Qt 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import requests
from PIL import Image
import io
# Módulos OpenCV
import cv2, imutils
import parking_client

# Módulo de código QR
from pyzbar.pyzbar import decode

# Hilo para enviar imagen sin bloquear la interfaz
class QRSenderThread(QThread):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path

    def run(self):
        url = "http://localhost:80"
        parking_client.sendQR(url, self.image_path)


# Clase hilo para captura de la cámara
class MyThread(QThread):
    frame_signal = pyqtSignal(QImage, bool)

    def run(self):
        self.is_running = True
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        while self.is_running:
            _, frame = self.cap.read()
            qframe = self.cvimage_to_qimage(frame)
            decodedQR = decode(frame)

            if len(decodedQR):
                self.cap.release()
                self.frame_signal.emit(qframe, True)
                self.is_running = False
                return

            self.frame_signal.emit(qframe, False)

        self.cap.release()

    def cvimage_to_qimage(self, image):
        image = imutils.resize(image, width=640)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(image, image.shape[1], image.shape[0], QImage.Format_RGB888)
        return image

    @pyqtSlot()
    def stop_capture(self):        
        self.is_running = False


# Ventana principal
class MainApp(QMainWindow):
    stop_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.__init__ui()
        self.show()
    
    def __init__ui(self):
        self.setFixedSize(640, 640)
        self.setWindowTitle("QR Scanner")
        self.is_streaming = False

        widget = QWidget(self)
        layout = QVBoxLayout()
        widget.setLayout(layout)

        self.label = QLabel()
        layout.addWidget(self.label)

        self.open_btn = QPushButton("Open The Camera", clicked=self.open_close_camera)
        layout.addWidget(self.open_btn)

        self.setCentralWidget(widget)

    def stop_streaming(self):
        self.open_btn.setText("Open The Camera")
        self.is_streaming = False
        self.camera_thread.frame_signal.disconnect()

    def open_close_camera(self):       
        if self.is_streaming:
            self.stop_streaming()
            self.stop_signal.emit()
            self.camera_thread.wait()
        else:
            self.camera_thread = MyThread()
            self.camera_thread.frame_signal.connect(self.setImage, Qt.BlockingQueuedConnection)
            self.stop_signal.connect(self.camera_thread.stop_capture)
            self.is_streaming = True
            self.open_btn.setText("Close The Camera")
            self.camera_thread.start()
            
    @pyqtSlot(QImage, bool)
    def setImage(self, image, flag):              
        if flag == False:
            self.label.setPixmap(QPixmap.fromImage(image))
        else:
            print('Qr valido')
            image_path = "codigo_qr_detectado.png"
            image.save(image_path, "PNG")
            print(f"Imagen guardada como '{image_path}'")

            
            self.sender_thread = QRSenderThread(image_path)
            self.sender_thread.start()

          
            self.stop_streaming()


# Crea la aplicación
app = QApplication([])

# Crea la ventana principal
main_window = MainApp()

# Lanza el manejador de eventos
app.exec()
    
