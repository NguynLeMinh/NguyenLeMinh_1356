import sys
import socket
import threading
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, QObject
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad

class Communicate(QObject):
    update_chat = pyqtSignal(str)

class ClientUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(ClientUI, self).__init__()
        # Load file UI bạn đã thiết kế
        uic.loadUi('UI/BoxChat.ui', self)
        
        self.c = Communicate()
        self.c.update_chat.connect(self.display_message)
        
        # Kết nối nút Gửi
        self.btnGui.clicked.connect(self.send_action)
        
        # Thiết lập kết nối và bảo mật
        self.setup_connection()
        
        # Luồng nhận tin nhắn
        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()

    def setup_connection(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('localhost', 12345))
            self.client_key = RSA.generate(2048)
            server_pub_key = RSA.import_key(self.client_socket.recv(2048))
            self.client_socket.send(self.client_key.publickey().export_key())
            encrypted_aes_key = self.client_socket.recv(2048)
            cipher_rsa = PKCS1_OAEP.new(self.client_key)
            self.aes_key = cipher_rsa.decrypt(encrypted_aes_key)
            
            self.txtNhan.append("<i style='color:green;'>Hệ thống: Đã thiết lập kênh mã hóa AES-RSA an toàn.</i>")
        except Exception as e:
            self.txtNhan.append(f"<b style='color:red;'>Lỗi kết nối: {e}</b>")

    def encrypt_message(self, message):
        cipher = AES.new(self.aes_key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
        return cipher.iv + ciphertext

    def decrypt_message(self, encrypted_message):
        iv = encrypted_message[:AES.block_size]
        ct = encrypted_message[AES.block_size:]
        cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size).decode()

    def send_action(self):
        message = self.txtGui.toPlainText().strip()
        if message:
            if message.lower() == 'exit':
                self.close()
                return
            
            try:
                encrypted = self.encrypt_message(message)
                self.client_socket.send(encrypted)
                
                self.txtNhan.append(f"<b>Me:</b> {message}")
                
                self.txtGui.clear()
            except Exception as e:
                self.txtNhan.append(f"Lỗi gửi: {e}")

    def receive_messages(self):
        while True:
            try:
                encrypted_data = self.client_socket.recv(1024)
                if not encrypted_data: break
                
                decrypted_msg = self.decrypt_message(encrypted_data)
                self.c.update_chat.emit(decrypted_msg)
            except:
                break

    def display_message(self, msg):
        self.txtNhan.append(f"<b>Server/Peer:</b> {msg}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ClientUI()
    window.show()
    sys.exit(app.exec())