from flask import Flask, request, jsonify
import os
import json
import getpass
from datetime import datetime, timedelta

from dotenv import load_dotenv

from personalcapital import (
    PersonalCapital,
    RequireTwoFactorException,
    TwoFactorVerificationModeEnum,
)

load_dotenv()

app = Flask(__name__)

class PewCapital(PersonalCapital):
    """
    Extends PersonalCapital to save and load session
    So that it doesn't require 2-factor auth every time
    """

    def __init__(self):
        PersonalCapital.__init__(self)
        self.__session_file = os.path.join(os.path.dirname(__file__), "session.json")

    def load_session(self):
        try:
            with open(self.__session_file) as data_file:
                cookies = {}
                try:
                    cookies = json.load(data_file)
                except ValueError as err:
                    app.logger.error(err)
                self.set_session(cookies)
        except IOError as err:
            app.logger.error(err)

    def save_session(self):
        with open(self.__session_file, "w") as data_file:
            data_file.write(json.dumps(self.get_session()))

def get_email_from_env():
    email = os.getenv("EMPOWER_EMAIL")
    if not email:
        app.logger.error("EMPOWER_EMAIL environment variable not set.")
    return email

def get_password_from_env():
    password = os.getenv("EMPOWER_PASSWORD")
    if not password:
        app.logger.error("EMPOWER_PASSWORD environment variable not set.")
    return password

def get_financial_data():
    email = get_email_from_env()
    password = get_password_from_env()

    if not email or not password:
        return {"error": "EMPOWER_EMAIL or EMPOWER_PASSWORD environment variables not set."}, 500

    pc = PewCapital()
    pc.load_session()

    try:
        pc.login(email, password)
    except RequireTwoFactorException:
        return {"error": "Two-factor authentication required. Please handle 2FA manually or ensure a persistent session."}, 401
    except Exception as e:
        return {"error": f"Login failed: {e}"}, 401

    accounts_response = pc.fetch("/newaccount/getAccounts")
    
    pc.save_session()

    accounts = accounts_response.json()
    networth = accounts['spData']['networth']

    output_data = {
        "networth": networth,
        "accounts": []
    }

    for account in accounts["spData"]["accounts"]:
        original_name = account.get('originalName', 'N/A')
        firm_name = account.get('firmName', 'N/A')
        account_type_group = account.get('accountTypeGroup', 'N/A')
        balance = account.get('balance', 'N/A')
        output_data["accounts"].append({
            "originalName": original_name,
            "firmName": firm_name,
            "accountTypeGroup": account_type_group,
            "balance": balance
        })
    
    return output_data, 200

@app.route('/get_financial_data', methods=['GET'])
def api_get_financial_data():
    result, status_code = get_financial_data()
    return jsonify(result), status_code

if __name__ == '__main__':
    # For development, run with debug=True. In production, use a production-ready WSGI server.
    app.run(debug=True, host='0.0.0.0', port=5000)
