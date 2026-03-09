from flask import Flask, render_template, request

from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher
from cipher.transposition import TranspositionCipher

app = Flask(__name__)


# ================= HOME =================

@app.route("/")
def home():
    return render_template("index.html")


# ================= CAESAR =================

@app.route("/caesar")
def caesar():
    return render_template("caesar.html")


@app.route("/caesar_encrypt", methods=["POST"])
def caesar_encrypt():

    text = request.form["inputPlainText"]
    key = int(request.form["inputKeyPlain"])

    cipher = CaesarCipher()

    result = cipher.encrypt_text(text, key)

    return f"""
    Plain text: {text} <br>
    Key: {key} <br>
    Encrypted text: {result}
    """


@app.route("/caesar_decrypt", methods=["POST"])
def caesar_decrypt():

    text = request.form["inputCipherText"]
    key = int(request.form["inputKeyCipher"])

    cipher = CaesarCipher()

    result = cipher.decrypt_text(text, key)

    return f"""
    Cipher text: {text} <br>
    Key: {key} <br>
    Decrypted text: {result}
    """


# ================= VIGENERE =================

@app.route("/vigenere")
def vigenere():
    return render_template("vigenere.html")


@app.route("/vigenere_encrypt", methods=["POST"])
def vigenere_encrypt():

    text = request.form["inputPlainText"]
    key = request.form["inputKeyPlain"]

    cipher = VigenereCipher()

    result = cipher.vigenere_encrypt(text, key)

    return f"""
    Plain text: {text} <br>
    Key: {key} <br>
    Encrypted text: {result}
    """


@app.route("/vigenere_decrypt", methods=["POST"])
def vigenere_decrypt():

    text = request.form["inputCipherText"]
    key = request.form["inputKeyCipher"]

    cipher = VigenereCipher()

    result = cipher.vigenere_decrypt(text, key)

    return f"""
    Cipher text: {text} <br>
    Key: {key} <br>
    Decrypted text: {result}
    """


# ================= RAIL FENCE =================

@app.route("/railfence")
def railfence():
    return render_template("railfence.html")


@app.route("/railfence_encrypt", methods=["POST"])
def railfence_encrypt():

    text = request.form["inputPlainText"]
    key = int(request.form["inputKeyPlain"])

    cipher = RailFenceCipher()

    result = cipher.rail_fence_encrypt(text, key)

    return f"""
    Plain text: {text} <br>
    Key: {key} <br>
    Encrypted text: {result}
    """


@app.route("/railfence_decrypt", methods=["POST"])
def railfence_decrypt():

    text = request.form["inputCipherText"]
    key = int(request.form["inputKeyCipher"])

    cipher = RailFenceCipher()

    result = cipher.rail_fence_decrypt(text, key)

    return f"""
    Cipher text: {text} <br>
    Key: {key} <br>
    Decrypted text: {result}
    """


# ================= PLAYFAIR =================

@app.route("/playfair")
def playfair():
    return render_template("playfair.html")


@app.route("/playfair_encrypt", methods=["POST"])
def playfair_encrypt():

    text = request.form["inputPlainText"]
    key = request.form["inputKeyPlain"]

    cipher = PlayFairCipher()

    matrix = cipher.create_playfair_matrix(key)

    result = cipher.playfair_encrypt(text, matrix)

    return f"""
    Plain text: {text} <br>
    Key: {key} <br>
    Encrypted text: {result}
    """


@app.route("/playfair_decrypt", methods=["POST"])
def playfair_decrypt():

    text = request.form["inputCipherText"]
    key = request.form["inputKeyCipher"]

    cipher = PlayFairCipher()

    matrix = cipher.create_playfair_matrix(key)

    result = cipher.playfair_decrypt(text, matrix)

    return f"""
    Cipher text: {text} <br>
    Key: {key} <br>
    Decrypted text: {result}
    """


# ================= TRANSPOSITION =================

@app.route("/transposition")
def transposition():
    return render_template("transposition.html")


@app.route("/transposition_encrypt", methods=["POST"])
def transposition_encrypt():

    text = request.form["inputPlainText"]
    key = int(request.form["inputKeyPlain"])

    cipher = TranspositionCipher()

    result = cipher.encrypt(text, key)

    return f"""
    Plain text: {text} <br>
    Key: {key} <br>
    Encrypted text: {result}
    """


@app.route("/transposition_decrypt", methods=["POST"])
def transposition_decrypt():

    text = request.form["inputCipherText"]
    key = int(request.form["inputKeyCipher"])

    cipher = TranspositionCipher()

    result = cipher.decrypt(text, key)

    return f"""
    Cipher text: {text} <br>
    Key: {key} <br>
    Decrypted text: {result}
    """


# ================= MAIN =================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)