import os
from datetime import datetime
from flask import Flask, render_template, request
import openpyxl

app = Flask(__name__)

EXCEL_FILE = "log_data.xlsx"


def log_to_excel(username, password):
    # Get current time stamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check if excel file already exists
    if os.path.exists(EXCEL_FILE):
        workbook = openpyxl.load_workbook(EXCEL_FILE)
        sheet = workbook.active
    else:
        # Create a new workbook and add headers if it doesn't exist
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Login Logs"
        sheet.append(["Username", "Password Entered", "Timestamp"])

    # Append the log data row
    sheet.append([username, password, current_time])

    # Save the file safely
    workbook.save(EXCEL_FILE)


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    # Capture data from HTML form
    username = request.form.get("username")
    password = request.form.get("password")

    # Send data to Excel Logger
    log_to_excel(username, password)

    return f"<h3>Login logged successfully for {username}! Check your log_data.xlsx file inside VS Code.</h3>"


if __name__ == "__main__":
    # app.run(debug=True, port=5000)
    app.run(debug=True, host='0.0.0.0', port=5000)