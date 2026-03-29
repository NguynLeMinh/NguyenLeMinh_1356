import sys
import socket
import threading
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, QObject
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

class Communicate(QObject):
    update_chat = pyqtSignal(str)
    system_log = pyqtSignal(str)

class BoxChatController(QtWidgets.QMainWindow):
    def __init__(self):
        super(BoxChatController, self).__init__()
        # 1. Load giao diện từ file .ui
        uic.loadUi('UI/BoxChat.ui', self)
        
        self.comm = Communicate()
        self.comm.update_chat.connect(self.display_message)
        self.comm.system_log.connect(self.display_system_log)

        self.aes_key = None
        self.client_socket = None

        self.btnGui.clicked.connect(self.send_message)

        threading.Thread(target=self.init_network, daemon=True).start()

    def init_network(self):
        try:
            self.comm.system_log.emit("Đang kết nối tới Server...")
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('localhost', 12345))

            client_rsa_key = RSA.generate(2048)

            server_pub_key = RSA.import_key(self.client_socket.recv(2048))

            self.client_socket.send(client_rsa_key.publickey().export_key())

            encrypted_aes_key = self.client_socket.recv(2048)
            cipher_rsa = PKCS1_OAEP.new(client_rsa_key)
            self.aes_key = cipher_rsa.decrypt(encrypted_aes_key)
            
            self.comm.system_log.emit("Kênh bảo mật AES-RSA đã sẵn sàng!")

            self.receive_loop()
            
        except Exception as e:
            self.comm.system_log.emit(f"Lỗi mạng: {e}")

    def encrypt_aes(self, plain_text):
        cipher = AES.new(self.aes_key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(plain_text.encode('utf-8'), AES.block_size))
        return cipher.iv + ct_bytes

    def decrypt_aes(self, cipher_data):
        iv = cipher_data[:AES.block_size]
        ct = cipher_data[AES.block_size:]
        cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')

    def send_message(self):
        msg = self.txtGui.toPlainText().strip()
        if msg and self.aes_key:
            try:
                encrypted_msg = self.encrypt_aes(msg)
                self.client_socket.send(encrypted_msg)

                self.txtNhan.append(f"<b style='color:blue;'>Me:</b> {msg}")
                self.txtGui.clear()
            except Exception as e:
                self.txtNhan.append(f"<i style='color:red;'>Lỗi gửi: {e}</i>")

    def receive_loop(self):
        while True:
            try:
                data = self.client_socket.recv(2048)
                if not data: break
                
                decrypted_msg = self.decrypt_aes(data)
                self.comm.update_chat.emit(decrypted_msg)
            except:
                break

    def display_message(self, msg):
        self.txtNhan.append(f"<b style='color:green;'>Server:</b> {msg}")

    def display_system_log(self, log):
        self.txtNhan.append(f"<i style='color:gray;'>[Hệ thống]: {log}</i>")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = BoxChatController()
    window.show()
    sys.exit(app.exec_())