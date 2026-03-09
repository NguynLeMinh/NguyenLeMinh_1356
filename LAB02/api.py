from flask import Flask , request, jsonify
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher

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

# VIGENERE CIPHER ALGORITHM
vigenere_cipher = VigenereCipher()


@app.route('/api/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    data = request.json
    plain_text = data['plaintext']
    key = data['key']

    encrypted_text = vigenere_cipher.vigenere_encrypt(plain_text, key)
    return jsonify({'encryptedtext': encrypted_text})


@app.route('/api/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    data = request.json
    ciphertext = data['ciphertext']
    key = data['key']

    decryptedtext = vigenere_cipher.vigenere_decrypt(ciphertext, key)
    return jsonify({'decryptedtext': decryptedtext})

# RAIL FENCE
railfence_cipher = RailFenceCipher()

@app.route('/api/railfence/encrypt', methods = ['POST'])
def encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = int(data['key'])
    
    encrypted_text = railfence_cipher.rail_fence_encrypt(plain_text, key)
    return jsonify({'encryptedtext': encrypted_text})

@app.route('/api/railfence/decrypt', methods = ['POST'])
def decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = int(data['key'])
    
    decrypted_text = railfence_cipher.rail_fence_decrypt(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})

#Main
if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=5000, debug=True)