import os
from pathlib import Path

from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

from securecrypto import aes_utils


app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
FILES_DIR = BASE_DIR / "upload"
FILES_DIR.mkdir(exist_ok=True)


def _save_uploaded_file():
    uploaded_file = request.files.get("file")
    if uploaded_file is None or uploaded_file.filename == "":
        raise ValueError("Missing uploaded file")
    filename = secure_filename(uploaded_file.filename)
    save_path = FILES_DIR / filename
    uploaded_file.save(save_path)
    return save_path


@app.route("/encrypt", methods=["POST"])
def encrypt():
    try:
        password = request.form["password"]
        save_path = _save_uploaded_file()
        key = aes_utils.encrypt_file_aes(save_path, password)
        return jsonify({"key": key, "encrypted_file": str(save_path) + ".enc"})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


@app.route("/decrypt", methods=["POST"])
def decrypt():
    try:
        key = request.form["password"]
        save_path = _save_uploaded_file()
        output_path = aes_utils.decrypt_file_aes(save_path, key)
        return jsonify({"output": output_path})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=True)
