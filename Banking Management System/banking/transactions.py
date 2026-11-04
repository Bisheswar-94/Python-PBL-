"""Transaction package functions: deposit, withdrawal, transfer, and history."""
from datetime import datetime
from .storage import load_data, save_data
from .accounts import find_account

def _record(data, account, kind, amount, note):
    tx={"id":data["next_transaction"],"account":account["number"],"kind":kind,"amount":round(amount,2),"note":note,"date":datetime.now().strftime("%d %b %Y, %I:%M %p")}
    data["next_transaction"]+=1; data["transactions"].insert(0,tx); return tx

def deposit(number, amount):
    """Add a positive amount to an active account."""
    data=load_data(); account=find_account(data,number); amount=_valid_amount(amount)
    account["balance"]=round(account["balance"]+amount,2); _record(data,account,"Deposit",amount,"Cash deposit"); save_data(data)
    return account["balance"]

def withdraw(number, amount, pin):
    """Withdraw after checking PIN and sufficient funds."""
    data=load_data(); account=find_account(data,number); amount=_valid_amount(amount)
    if str(pin) != account["pin"]: raise ValueError("Incorrect PIN.")
    if amount > account["balance"]: raise ValueError("Insufficient funds.")
    account["balance"]=round(account["balance"]-amount,2); _record(data,account,"Withdrawal",amount,"Cash withdrawal"); save_data(data)
    return account["balance"]

def transfer(source_number, destination_number, amount, pin):
    """Move funds between accounts and record both sides of the transfer."""
    if str(source_number)==str(destination_number): raise ValueError("Choose a different destination account.")
    data=load_data(); source=find_account(data,source_number); destination=find_account(data,destination_number); amount=_valid_amount(amount)
    if str(pin) != source["pin"]: raise ValueError("Incorrect PIN.")
    if amount > source["balance"]: raise ValueError("Insufficient funds.")
    source["balance"]=round(source["balance"]-amount,2); destination["balance"]=round(destination["balance"]+amount,2)
    _record(data,source,"Transfer out",amount,f"To account {destination['number']}"); _record(data,destination,"Transfer in",amount,f"From account {source['number']}"); save_data(data)
    return source["balance"]

def history(number):
    """Return recent transactions for one account."""
    data=load_data(); find_account(data,number)
    return [t for t in data["transactions"] if str(t["account"])==str(number)][:50]

def _valid_amount(value):
    try: amount=round(float(value),2)
    except (TypeError,ValueError): raise ValueError("Amount must be a number.")
    if amount <= 0: raise ValueError("Amount must be greater than zero.")
    return amount
