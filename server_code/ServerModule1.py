import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
import anvil.server
from anvil import tables, app
import random
import uuid

@anvil.server.callable
def get_user_for_login(login_input):
  user_by_username = app_tables.wallet_users.get(username=login_input)
  if login_input.isdigit():
    phone_number = int(login_input)
    user_by_phone = app_tables.wallet_users.get(phone=phone_number)
    return user_by_phone
    # Continue with the rest of your code
  else:
    print("Invalid phone number. Please enter a numeric value.")
  user_by_email = app_tables.wallet_users.get(email=login_input)
  if user_by_username:
            return user_by_username
  if user_by_email:
            return user_by_email 
  else:
            return None

@anvil.server.callable
def add_info(email, username, password, pan, address, phone, aadhar):
    user_row = app_tables.wallet_users.add_row(
        email=email,
        username=username,
        password=password,
        pan=pan,
        address=address,
        phone=phone,
        aadhar=aadhar,
        usertype='customer',
        confirm_email=True,
        user_limit=(100000),
        last_login = datetime.now()
    )
    return user_row

# @anvil.server.callable
# def get_user_by_phone(phone_number):
#     # Convert the phone_number to a number before searching
#     phone_number = int(phone_number)
#     users = app_tables.wallet_users.search(phone=phone_number)
#     return users[0] if users else None
###

@anvil.server.callable
def get_acc_data(phone):
    user_accounts = app_tables.wallet_users_account.search(phone=phone)
    return [acc['account_number'] for acc in user_accounts]

@anvil.server.callable
def get_user_account_numbers(phone):
    user_accounts = app_tables.wallet_users_account.search(phone=phone)
    return [acc['account_number'] for acc in user_accounts]

@anvil.server.callable
def get_username(phone):
    user = app_tables.wallet_users.get(phone=phone)
    if user:
        return user['username']
    else:
        return "Username Not Found"      




###

@anvil.server.callable
def get_user_by_phone(phone_number):
    try:
        phone_number = int(phone_number)  # Convert the phone_number to an integer
        users = app_tables.wallet_users.search(phone=phone_number)

        if users and len(users) > 0:
            return users[0]
        else:
            return None
    except ValueError:
        # Handle the case where the input cannot be converted to an integer
        return None
 

@anvil.server.callable
def get_wallet_transactions():
    return app_tables.wallet_users_transaction.search()

@anvil.server.callable
def get_user_bank_name(phone):
  bank_names = app_tables.wallet_users_account.search(phone=phone)
  return bank_names
@anvil.server.callable
def get_username(phone):
  user = app_tables.wallet_users.get(phone=phone)
  return user['username'] 
@anvil.server.callable
def get_user_currency(phone):
  currency= app_tables.wallet_users_balance.search(phone=phone)
  return currency

@anvil.server.callable
def get_wallet_transactions():
    return app_tables.wallet_users_transaction.search()

@anvil.server.callable
def get_transaction_proofs():
    # Fetch proof data from the 'transactions' table
    transaction_proofs = app_tables.wallet_users_transaction.search()

    return transaction_proofs


@anvil.server.callable
def get_transactions():
    return app_tables.wallet_users_transaction.search()

@anvil.server.callable
def get_user_data():
    # Fetch user data from the 'users' table
    users_data = app_tables.wallet_users.search()

    # Create a list to store user information
    user_list = []

    # Iterate through each user's data
    for user_row in users_data:
        # Check the 'banned' column to determine if the user is active or non-active
        if user_row['banned'] is None:
            status = 'Active'
        else:
            status = 'Non-Active'

        # Append user information to the list
        user_info = {
            'username': user_row['username'],
            'banned': user_row['banned'],
            'status': status  # Include the 'status' information based on the 'banned' column
        }
        user_list.append(user_info)

    return user_list

@anvil.server.callable
def update_daily_limit(name, emoney_value):
    user_row = app_tables.users.get(username=name)  # Use get() instead of search() if username is unique

    if user_row is not None:
        user_row['user_limit'] = emoney_value
        user_row.update()
        return "Daily limit updated successfully"
    else:
        return "User not found"
@anvil.server.callable
def user_detail(name, no):
    user_row = app_tables.wallet_users.get(username=name)
    
    if user_row is not None:
        try:
            # Try to convert 'no' to a numeric type
            numeric_no = float(no)
            user_row['daily_limit'] = numeric_no
            user_row.update()
            return "Daily limit updated successfully"
        except ValueError:
            return "Invalid daily limit value. Please provide a numeric value."
    else:
        return "User not found"

####1111111#####
# anvil.server.call('get_username', self.user['phone'])
@anvil.server.callable
def get_username(phone_number):
    user = app_tables.wallet_users.get(phone=phone_number)
    return user['username'] if user else None



@anvil.server.callable
def get_balance_using_phone_number(phone_number, currency_type):
    # Convert the phone_number to a numeric type
    phone_number = int(phone_number)

    # Use query to filter rows based on both 'phone' and 'currency_type'
    account = app_tables.wallet_users_balance.search(
        phone=phone_number,
        currency_type=currency_type
    )

    try:
        return account[0]
    except IndexError:
        # If IndexError occurs (empty list), return a default value
        return {'balance': None, 'phone': phone_number, 'currency_type': currency_type}

# @anvil.server.callable
# def update_balance_transaction(phone_number, new_balance, currency_type):
#     # Convert the phone_number to a numeric type
#     phone_number = int(phone_number)

#     # Use search to get all rows matching the query
#     balances = app_tables.wallet_users_balance.search(
#         phone=phone_number,
#         currency_type=currency_type
#     )

#     # Iterate through the list of balances or choose the appropriate row based on your criteria
#     for balance in balances:
#         # Convert new_balance to the appropriate type (number)
#         new_balance = float(new_balance)
#         # Your existing logic to update the balance goes here
#         balance.update(balance=new_balance)

#     # If you want to handle the case where no rows matched the query
#     if not balances:
#         # Create a new row with the provided information
#         app_tables.wallet_users_balance.add_row(phone=phone_number, balance=new_balance, currency_type=currency_type)

@anvil.server.callable
def update_balance_transaction(phone_number, new_balance, currency_type):
    print(f"Updating balance for {phone_number} with new balance {new_balance} in currency {currency_type}")
    
    # Convert the phone_number to a numeric type
    phone_number = int(phone_number)

    # Use search to get all rows matching the query
    balances = app_tables.wallet_users_balance.search(
        phone=phone_number,
        currency_type=currency_type
    )

    # Iterate through the list of balances or choose the appropriate row based on your criteria
    for balance in balances:
        # Convert new_balance to the appropriate type (number)
        new_balance = float(new_balance)
        # Your existing logic to update the balance goes here
        balance.update(balance=new_balance)

    # If you want to handle the case where no rows matched the query
    if not balances:
        print("Adding a new row...")
        # Create a new row with the provided information
        app_tables.wallet_users_balance.add_row(phone=phone_number, balance=new_balance, currency_type=currency_type)
    else:
        print("Row already exists.")

    print("Update complete.")



@anvil.server.callable
def update_depositor_balance(depositor_phone_number, new_balance, currency_type):
    # Convert the depositor_phone_number to a numeric type
    depositor_phone_number = int(depositor_phone_number)

    # Use search to get all rows matching the query for depositor
    depositor_balances = app_tables.wallet_users_balance.search(
        phone=depositor_phone_number,
        currency_type=currency_type
    )

    # Iterate through the list of depositor_balances or choose the appropriate row based on your criteria
    for depositor_balance in depositor_balances:
        # Convert new_balance to the appropriate type (number)
        new_balance = float(new_balance)
        # Your existing logic to update the balance goes here
        depositor_balance.update(balance=new_balance)

    # If you want to handle the case where no rows matched the query for depositor
    if not depositor_balances:
        # Create a new row with the provided information for depositor
        app_tables.wallet_users_balance.add_row(phone=depositor_phone_number, balance=new_balance, currency_type=currency_type)


@anvil.server.callable
def update_receiver_balance(receiver_phone_number, new_balance, currency_type):
    # Convert the receiver_phone_number to a numeric type
    receiver_phone_number = int(receiver_phone_number)

    # Use search to get all rows matching the query for receiver
    receiver_balances = app_tables.wallet_users_balance.search(
        phone=receiver_phone_number,
        currency_type=currency_type
    )

    # Iterate through the list of receiver_balances or choose the appropriate row based on your criteria
    for receiver_balance in receiver_balances:
        # Convert new_balance to the appropriate type (number)
        new_balance = float(new_balance)
        # Your existing logic to update the balance goes here
        receiver_balance.update(balance=new_balance)

    # If you want to handle the case where no rows matched the query for receiver
    if not receiver_balances:
        # Create a new row with the provided information for receiver
        app_tables.wallet_users_balance.add_row(phone=receiver_phone_number, balance=new_balance, currency_type=currency_type)




# anvil.server.call('update_daily_limit', self.user['username'], str(answer))
@anvil.server.callable
def update_daily_limit(username, new_limit):
    user = app_tables.wallet_users.get(username=username)
    if user:
        user['limit'] = new_limit
        user.save()

# Additional function, assuming money_value is a variable not defined in the code snippet
# This function isn't called in your provided code, so please adjust accordingly.
@anvil.server.callable
def add_transaction_record(depositor_phone, money_value, current_datetime, transaction_type, transaction_status, receiver_phone):
    app_tables.wallet_users_transaction.add_row(
        phone=depositor_phone,
        fund=money_value,
        date=current_datetime,
        transaction_type=transaction_type,
        transaction_status=transaction_status,
        receiver_phone=receiver_phone
    )










#https://menu-email.anvil.app