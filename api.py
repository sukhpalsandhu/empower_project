import subprocess
from flask import Flask, request, jsonify
import os
import json
# Removed getpass as it's not needed when calling main.py
from datetime import datetime, timedelta

from dotenv import load_dotenv

# Removed PersonalCapital imports as main.py will handle it
# from personalcapital import (
#     PersonalCapital,
#     RequireTwoFactorException,
#     TwoFactorVerificationModeEnum,
# )

load_dotenv()

app = Flask(__name__)

# Removed PewCapital class as main.py will handle it
# class PewCapital(PersonalCapital):
#     """
#     Extends PersonalCapital to save and load session
#     So that it doesn't require 2-factor auth every time
#     """

#     def __init__(self):
#         PersonalCapital.__init__(self)
#         self.__session_file = os.path.join(os.path.dirname(__file__), "session.json")

#     def load_session(self):
#         try:
#             with open(self.__session_file) as data_file:
#                 cookies = {}
#                 try:
#                     cookies = json.load(data_file)
#                 except ValueError as err:
#                     app.logger.error(err)
#                 self.set_session(cookies)
#         except IOError as err:
#             app.logger.error(err)

#     def save_session(self):
#         with open(self.__session_file, "w") as data_file:
#             data_file.write(json.dumps(self.get_session()))

# Removed get_email_from_env and get_password_from_env as main.py will handle it
# def get_email_from_env():
#     email = os.getenv("EMPOWER_EMAIL")
#     if not email:
#         app.logger.error("EMPOWER_EMAIL environment variable not set.")
#     return email

# def get_password_from_env():
#     password = os.getenv("EMPOWER_PASSWORD")
#     if not password:
#         app.logger.error("EMPOWER_PASSWORD environment variable not set.")
#     return password

def get_financial_data():
    try:
        # Execute main.py as a subprocess
        result = subprocess.run(
            ['python', 'main.py'],
            capture_output=True,
            text=True,
            check=True # Raise an exception for non-zero exit codes
        )
        
        # main.py prints JSON to stdout
        output_data = json.loads(result.stdout)
        return output_data, 200
    except subprocess.CalledProcessError as e:
        app.logger.error(f"main.py subprocess failed: {e.stderr}")
        return {"error": f"Failed to retrieve financial data: {e.stderr}"}, 500
    except json.JSONDecodeError as e:
        app.logger.error(f"Failed to parse JSON from main.py output: {e}")
        return {"error": "Failed to parse financial data from main.py output."}, 500
    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {e}")
        return {"error": f"An unexpected error occurred: {e}"}, 500

@app.route('/get_financial_data', methods=['GET'])
def api_get_financial_data():
    result, status_code = get_financial_data()
    return jsonify(result), status_code

if __name__ == '__main__':
    # For development, run with debug=True. In production, use a production-ready WSGI server.
    app.run(debug=True, host='0.0.0.0', port=5000)
