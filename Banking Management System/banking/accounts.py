"""Account package functions: create, find, list, and close accounts."""
from .storage import load_data, save_data

def list_accounts():
    """Return every account without exposing the stored PIN."""
    return [{k:v for k,v in account.items() if k != "pin"} for account in load_data()["accounts"]]

def create_account(name, account_type, opening_balance, pin):
    """Validate and create a savings or current account."""
    name = name.strip()
    if not name: raise ValueError("Please enter the account holder's name.")
    if account_type not in ("Savings", "Current"): raise ValueError("Choose Savings or Current account.")
    try: balance = round(float(opening_balance), 2)
    except (TypeError, ValueError): raise ValueError("Opening balance must be a number.")
    if balance < 0: raise ValueError("Opening balance cannot be negative.")
    pin = str(pin).strip()
    if not pin.isdigit() or len(pin) != 4: raise ValueError("PIN must contain exactly 4 digits.")
    data = load_data(); number = data["next_account"]; data["next_account"] += 1
    account = {"number": number, "name": name, "type": account_type, "balance": balance, "pin": pin, "status": "Active"}
    data["accounts"].append(account); save_data(data)
    return {k:v for k,v in account.items() if k != "pin"}

def close_account(number):
    """Close an account only when its balance is zero."""
    data=load_data(); account=find_account(data, number)
    if account["balance"] != 0: raise ValueError("Withdraw or transfer the remaining balance before closing.")
    account["status"]="Closed"; save_data(data)
    return {k:v for k,v in account.items() if k != "pin"}

def find_account(data, number):
    """Find an account by number or raise a useful error."""
    account=next((a for a in data["accounts"] if str(a["number"]) == str(number)), None)
    if not account: raise ValueError("Account number was not found.")
    if account["status"] != "Active": raise ValueError("This account is closed.")
    return account
