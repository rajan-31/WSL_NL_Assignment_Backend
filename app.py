from flask import Flask, request, jsonify, render_template
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()   # load environment variables from .env file

app = Flask(__name__)

# ================================================

@app.route('/')
def index_page():
    return render_template('index.html')

# Define validation criteria
REQUIRED_SHEETS = ["Course", "Topic", "Resource", "Learner"]
REQUIRED_FIELDS = {
    "Course": ["Course ID", "Course Name"],
    "Topic": ["Topic ID", "Topic Name", "Description"],
    "Resource": ["Resource ID", "Resource Name", "Resource Content", "Module ID", "Module Name", "Sub Module ID"],
    "Learner": ["Learner ID", "Name", "Essay", "Module ID", "Submodule ID"]
}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith('.xlsx'):
        return jsonify({"error": "Invalid file format. Please upload an Excel file."}), 400

    try:
        excel_data = pd.ExcelFile(file)     # throws error if file contents are not excel data
        response = {"valid": True, "errors": []}

        # Check for required sheets
        for sheet in REQUIRED_SHEETS:
            if sheet not in excel_data.sheet_names:
                response["valid"] = False
                response["errors"].append(f"Missing required sheet: {sheet}")

        # Validate fields and data in each sheet
        for sheet, fields in REQUIRED_FIELDS.items():
            if sheet in excel_data.sheet_names:
                df = excel_data.parse(sheet)
                missing_fields = [field for field in fields if field not in df.columns]

                if missing_fields:
                    response["valid"] = False
                    response["errors"].append(f"Missing fields in {sheet}: {', '.join(missing_fields)}")

                if df.empty:
                    response["valid"] = False
                    response["errors"].append(f"Sheet {sheet} is empty.")

        if response["valid"]:
            # in real app here we will add logic to create new course to be shown on dashboard

            return jsonify({"message": "Validation successful."}), 200
        else:
            return jsonify({"message": "Validation failed.", "details": response["errors"]}), 400

    except Exception as e:
        return jsonify({"error": f"An error occurred while processing the file: {str(e)}"}), 500

# ================================================

if __name__ == '__main__':
    # use environment variables if present else default values
    debug = os.getenv('DEBUG', False)
    host = os.getenv('HOST', '0.0.0.0')
    port = os.getenv('PORT', 8080)

    app.run(host=host, port=port, debug=debug)
