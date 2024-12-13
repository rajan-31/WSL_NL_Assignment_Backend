from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv

load_dotenv()   # load environment variables from .env file

app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith('.xlsx'):
        return jsonify({"error": "Invalid file format. Please upload an Excel file."}), 400

    return jsonify({"message": "Validation successful."}), 200

if __name__ == '__main__':
    # use environment variables if present else default values
    debug = os.getenv('DEBUG', False)
    host = os.getenv('HOST', '0.0.0.0')
    port = os.getenv('PORT', 8080)

    app.run(host=host, port=port, debug=debug)
