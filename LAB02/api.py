from flask import Flask , request, jsonify
from cipher.caesar import CaesarCipher
app = Flask(__name__)

#CAESAR
caesar_cipher = CaesarCipher()

@app.route("/api/caesar/encrypt", methods = ["POST"])
def caesar_encrypt():
    data = request.json
    plaintext = data['plaintext']
    key = int(data['key'])
    encrypted_text = caesar_cipher.encrypt_text(plaintext, key)
    return jsonify({'encrypt_message': encrypted_text})

@app.route("/api/caesar/decrypt", methods = ["POST"])
def caesar_decrypt():
    data = request.json
    plaintext = data['plaintext']
    key = int(data['key'])
    decrypted_text = caesar_cipher.decrypt_text(plaintext, key)
    return jsonify({'decrypt_message': decrypted_text})

#Main
if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=5000, debug=True)