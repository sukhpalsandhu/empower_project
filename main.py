import sys
import os
import getpass
import json
import logging
from datetime import datetime, timedelta

from dotenv import load_dotenv

# Add the vendor directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'vendor')))

from personalcapital import (
    PersonalCapital,
    RequireTwoFactorException,
    TwoFactorVerificationModeEnum,
)

load_dotenv()

# Python 2 and 3 compatibility
if hasattr(__builtins__, "raw_input"):
    input = raw_input


class PewCapital(PersonalCapital):
    """
    Extends PersonalCapital to save and load session
    So that it doesn't require 2-factor auth every time
    """

    def __init__(self):
        PersonalCapital.__init__(self)
        self.__session_file = "session.json"

    def load_session(self):
        try:
            with open(self.__session_file) as data_file:
                cookies = {}
                try:
                    cookies = json.load(data_file)
                except ValueError as err:
                    logging.error(err)
                self.set_session(cookies)
        except IOError as err:
            logging.error(err)

    def save_session(self):
        with open(self.__session_file, "w") as data_file:
            data_file.write(json.dumps(self.get_session()))


def get_email():
    email = os.getenv("EMPOWER_EMAIL") # Changed from PEW_EMAIL to EMPOWER_EMAIL
    if not email:
        print(
            "You can set the environment variables for EMPOWER_EMAIL and EMPOWER_PASSWORD so the prompts don't come up every time"
        )
        return input("Enter email:")
    return email


def get_password():
    password = os.getenv("EMPOWER_PASSWORD") # Changed from PEW_PASSWORD to EMPOWER_PASSWORD
    if not password:
        return getpass.getpass("Enter password:")
    return password


def main():
    email, password = get_email(), get_password()
    pc = PewCapital()
    pc.load_session()

    try:
        pc.login(email, password)
    except RequireTwoFactorException:
        print("Two-factor authentication required.")
        pc.two_factor_challenge(TwoFactorVerificationModeEnum.SMS)
        two_factor_code = input("Enter 2FA code (sent via SMS): ")
        pc.two_factor_authenticate(TwoFactorVerificationModeEnum.SMS, two_factor_code)
        pc.authenticate_password(password) # Re-authenticate password after 2FA
        print("Two-factor authentication successful.")
    except Exception as e:
        print(f"Login failed: {e}")
        return

    accounts_response = pc.fetch("/newaccount/getAccounts")

    now = datetime.now()
    date_format = "%Y-%m-%d"
    days = 90
    start_date = (now - (timedelta(days=days + 1))).strftime(date_format)
    end_date = (now - (timedelta(days=1))).strftime(date_format)
    pc.save_session()

    # Accounts Data
    accounts_data = accounts_response.json()
    networth = accounts_data['spData']['networth']

    output_data = {
        "networth": networth,
        "accounts": []
    }

    for account in accounts_data["spData"]["accounts"]:
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

    print(json.dumps(output_data, indent=2))


if __name__ == "__main__":
    main()
