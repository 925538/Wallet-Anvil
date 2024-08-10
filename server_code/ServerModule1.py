import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timezone,timedelta
import anvil.server
from anvil import tables, app
import random
import anvil.email
import base64
from PIL import Image,ImageDraw
from io import BytesIO
import requests
# import anvil.tables as tables
# from datetime import datetime,
#import datetime



@anvil.server.callable
def check_and_topup_users(phone):

    
  today = datetime.now().date()
  user = app_tables.wallet_users.get(users_phone=phone)
  

  
  users_topup_duration = int(user['users_timely_topup_duration'])
  # last_topup_date is not None and
  balance = app_tables.wallet_users_balance.get(users_balance_phone = phone)
  if  users_topup_duration is not None and user['users_timely_topup'] is not False and today <= user['users_timely_topup_expiry_date'] :
      next_topup_date = today+timedelta(days = users_topup_duration)
      
      if today >= next_topup_date:
          # Perform the top-up
          balance['users_balance'] += user['users_timely_topup_amount']  # Add the top-up amount (change this value as needed)
          user['users_next_autotopup_time'] = next_topup_date  # Update the last top-up date
          user.update()
          users_text = f" {user['users_timely_topup_amount']} Added Through AutoTopUp"
          time = datetime.now().date()
          anvil.server.call('notify', users_text, time, phone, phone)
      else:
        user['users_next_autotopup_time'] = next_topup_date
        user.update()


    # today = datetime.now().date()
    # user = app_tables.wallet_users.get(users_phone=phone)
    

    # last_topup_date = user['last_topup_date']
    # users_topup_duration = user['users_timely_topup_duration']
    
    # if last_topup_date is not None and users_topup_duration is not None:
    #     next_topup_date = last_topup_date + timedelta(days=users_topup_duration)
    #     if today >= next_topup_date:
    #         # Perform the top-up
    #         user['balance'] += 100  # Add the top-up amount (change this value as needed)
    #         user['last_topup_date'] = today  # Update the last top-up date




@anvil.server.callable
def check_email_exists(email):
    user = app_tables.wallet_users.get(users_email=email)
    return user is not None

@anvil.server.callable
def get_user_for_login(login_input):
  user_by_username = app_tables.wallet_users.get(users_username=login_input)
  if login_input.isdigit():
    phone_number = int(login_input)
    user_by_phone = app_tables.wallet_users.get(users_phone=phone_number)
    return user_by_phone
    # Continue with the rest of your code
  else:
    print("Invalid phone number. Please enter a numeric value.")
  user_by_email = app_tables.wallet_users.get(users_email=login_input)
  if user_by_username:
            return user_by_username
  if user_by_email:
            return user_by_email 
  else:
            return None

@anvil.server.callable
def add_info(username, email, address, phone, aadhar, pan, password, currency):
    user_row = app_tables.wallet_users.add_row(
        users_username=username,
        users_email=email,
        users_address=address,
        users_phone=int(phone),
        users_aadhar=int(aadhar),
        users_pan=pan,
        users_password=password,
        users_usertype='customer',
        users_confirm_email=True,
        users_user_limit=100000,
        users_daily_limit=40000,
        users_last_login=datetime.now(),
        users_defaultcurrency=currency  # Store the currency
    )
    return user_row
@anvil.server.callable
def send_email_otp(email):
    otp = random.randint(100000, 999999)

    from_email = "gtpltechnologies@gmail.com"  # Use your verified email address
    subject = "OTP Verification"
    content = f"Your OTP is: {otp}"

    try:
        anvil.email.send(to=email, from_address=from_email, subject=subject, text=content)
        return otp  # If successful, return OTP
    except Exception as e:
        print(f"Error sending email: {e}")
        return str(e)  # Return error message

@anvil.server.callable
def get_currency_by_country(country_name):
    response = requests.get(f"https://restcountries.com/v3.1/name/{country_name}")
    if response.status_code == 200:
        data = response.json()
        if data:
            country_info = data[0]
            currency = list(country_info['currencies'].keys())[0]
            return currency
    return None
@anvil.server.callable
def get_acc_data(phone):
    user_accounts = app_tables.wallet_users_account.search(users_account_phone=phone)
    return [acc['users_account_account_number'] for acc in user_accounts]

@anvil.server.callable
def get_user_account_numbers(phone):
    user_accounts = app_tables.wallet_users_account.search(users_account_phone=phone)
    return [acc['users_account_account_number'] for acc in user_accounts]

@anvil.server.callable
def get_username(phone):
    user = app_tables.wallet_users.get(users_phone=phone)
    if user:
        return user['users_username']
    else:
        return "Username Not Found"      
      
@anvil.server.callable
def get_currency_code():
    currencies = app_tables.wallet_admins_add_currency.search()
    return [f"{currency['admins_add_currency_code']}" for currency in currencies]

@anvil.server.callable
def get_all_banks_name():
    banks = app_tables.wallet_admins_add_bank.search()
    return [f"{bank['admins_add_bank_names']}" for bank in banks]




# @anvil.server.callable
# def perform_top_up(phone, amount):
#     # Logic to perform top-up
#     # For example, update the user's balance in the database
#     # user = app_tables.wallet_users.get(user_phone=phone)
#     balance=app_tables.wallet_users_balance.get(users_balance_phone=phone)
#     if balance:
#         balance['users_balance'] += amount
#         return "Top-up successful"
#     else:
#         return "User not found"
# # In a background task (e.g., scheduled_top_up)


# @anvil.server.background_task
# def scheduled_top_up():
#     # Define the interval for the top-up (e.g., daily)
#     interval = timedelta(seconds=30)
#     next_run = datetime.now() + interval

#     while True:
#         # Perform top-up for all users (example logic)
#         for user in tables.app_tables.wallet_users.search():
#             anvil.server.call('perform_top_up', user['users_phone'], 100)  # Example: top-up with 100 units

#         # Sleep until the next run
#         anvil.server.wait_until(next_run)
#         next_run += interval

@anvil.server.callable
def total_users(customer):
    users = app_tables.wallet_users.search(users_usertype=customer)
    print(users)
    return len(users)

@anvil.server.callable
def add_admins_info(username, email, phone_number, password):
    admin_row = app_tables.wallet_users.add_row(
        users_username=username,
        users_email=email, 
        users_phone=phone_number,
        users_password=password,
        users_usertype='admin',
    )
    return admin_row


###

@anvil.server.callable
def get_user_by_phone(phone_number):
    try:
        phone_number = int(phone_number)  # Convert the phone_number to an integer
        users = app_tables.wallet_users.search(users_phone=phone_number)

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
  bank_names = app_tables.wallet_users_account.search(users_account_phone=phone)
  return bank_names
@anvil.server.callable
def get_username(phone):
  user = app_tables.wallet_users.get(users_phone=phone)
  return user['users_username'] 
@anvil.server.callable
def get_user_currency(phone):
  currency= app_tables.wallet_users_balance.search(users_balance_phone=phone)
  return currency

@anvil.server.callable
def get_admin_by_phone(phone_number):
    try:
        phone_number = int(phone_number)  # Convert the phone_number to an integer
        admins = app_tables.wallet_admins_create_admin_account.search(admins_phone=phone_number)

        if admins and len(admins) > 0:
            return admins[0]
        else:
            return None
    except ValueError:
        # Handle the case where the input cannot be converted to an integer
        return None

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
        if user_row['users_banned'] is None:
            status = 'Active'
        else:
            status = 'Non-Active'

        # Check the 'inactive' column to determine if the user is inactive
        if user_row['users_inactive'] is None:
            activity_status = 'Active'
        else:
            activity_status = 'Inactive'

        # Append user information to the list
        user_info = {
            'username': user_row['users_username'],
            'banned': user_row['users_banned'],
            'inactive': user_row['users_inactive'],
            'status': status,  # Include the 'status' information based on the 'banned' column
            'activity_status': activity_status  # Include the 'activity_status' information based on the 'inactive' column
        }
        user_list.append(user_info)

    return user_list

@anvil.server.callable
def update_daily_limit(name, emoney_value):
    user_row = app_tables.wallet_users.get(users_username=name)  # Use get() instead of search() if username is unique

    if user_row is not None:
        user_row['users_user_limit'] = emoney_value
        user_row.update()
        return "Daily limit updated successfully"
    else:
        return "User not found"
@anvil.server.callable
def user_detail(name, no):
    user_row = app_tables.wallet_users.get(users_username=name)
    
    if user_row is not None:
        try:
            # Try to convert 'no' to a numeric type
            numeric_no = float(no)
            user_row['users_daily_limit'] = numeric_no
            user_row.update()
            return "Daily limit updated successfully"
        except ValueError:
            return "Invalid daily limit value. Please provide a numeric value."
    else:
        return "User not found"


# anvil.server.call('get_username', self.user['phone'])
@anvil.server.callable
def get_username(phone_number):
    user = app_tables.wallet_users.get(users_phone=phone_number)
    return user['users_username'] if user else None

@anvil.server.callable
def get_inr_balance(phone):
  balance = app_tables.wallet_users_balance.search(users_balance_phone=phone)
  return balance

@anvil.server.callable
def get_balance_using_phone_number(phone_number, currency_type):
    # Convert the phone_number to a numeric type
    phone_number = int(phone_number)
    # Use query to filter rows based on both 'phone' and 'currency_type'
    account = app_tables.wallet_users_balance.search(
        users_balance_phone=phone_number,
        users_balance_currency_type=currency_type
    )
    try:
        return account[0]
    except IndexError:
        # If IndexError occurs (empty list), return a default value
        return {'balance': None, 'phone': phone_number, 'currency_type': currency_type}

@anvil.server.callable
def update_balance_transaction(phone_number, new_balance, currency_type):
    print(f"Updating balance for {phone_number} with new balance {new_balance} in currency {currency_type}")
    phone_number = int(phone_number)
    balances = app_tables.wallet_users_balance.search(
        users_balance_phone=phone_number,
        users_balance_currency_type=currency_type
    )
    # Iterate through the list of balances or choose the appropriate row based on your criteria
    for balance in balances:
        # Convert new_balance to the appropriate type (number)
        new_balance = float(new_balance)
        balance.update(users_balance=new_balance)
    # If you want to handle the case where no rows matched the query
    if not balances:
        print("Adding a new row...")
        # Create a new row with the provided information
        app_tables.wallet_users_balance.add_row(users_balance_phone=phone_number, users_balance=new_balance, users_balance_currency_type=currency_type)
    else:
        print("Row already exists.")
    print("Update complete.")



@anvil.server.callable
def update_depositor_balance(depositor_phone_number, new_balance, currency_type):
    # Convert the depositor_phone_number to a numeric type
    depositor_phone_number = int(depositor_phone_number)
    # Use search to get all rows matching the query for depositor
    depositor_balances = app_tables.wallet_users_balance.search(
        users_balance_phone=depositor_phone_number,
        users_balance_currency_type=currency_type
    )
    # Iterate through the list of depositor_balances or choose the appropriate row based on your criteria
    for depositor_balance in depositor_balances:
        new_balance = float(new_balance)
        depositor_balance.update(users_balance=new_balance)
    # If you want to handle the case where no rows matched the query for depositor
    if not depositor_balances:
        # Create a new row with the provided information for depositor
        app_tables.wallet_users_balance.add_row(users_balance_phone=depositor_phone_number, users_balance=new_balance, users_balance_currency_type=currency_type)


@anvil.server.callable
def update_receiver_balance(receiver_phone_number, new_balance, currency_type):
    # Convert the receiver_phone_number to a numeric type
    receiver_phone_number = int(receiver_phone_number)
    # Use search to get all rows matching the query for receiver
    receiver_balances = app_tables.wallet_users_balance.search(
        users_balance_phone=receiver_phone_number,
        users_balance_currency_type=currency_type
    )
    # Iterate through the list of receiver_balances or choose the appropriate row based on your criteria
    for receiver_balance in receiver_balances:
        new_balance = float(new_balance)
        receiver_balance.update(users_balance=new_balance)
    # If you want to handle the case where no rows matched the query for receiver
    if not receiver_balances:
        # Create a new row with the provided information for receiver
        app_tables.wallet_users_balance.add_row(users_balance_phone=receiver_phone_number, users_balance=new_balance, users_balance_currency_type=currency_type)

@anvil.server.callable
def get_currency_balance(user_phone, currency_type):
    # Retrieve the balance for the given user and currency type
    user_rows = app_tables.wallet_users_balance.search(users_balance_phone=user_phone, users_balance_currency_type=currency_type)
    
    if len(user_rows) > 0:
        # Assuming there's only one row per user and currency type, return the balance
        return user_rows[0]['users_balance']
    else:
        return None 
      
@anvil.server.callable
def send_otp_email(email, otp):
    """
    Sends an OTP to the specified email address and stores it in the server session.
    """
    # Check if the email exists in the database
    if validate_email(email):
        # Compose email message
        subject = "Your One Time Password (OTP)"
        message = f"Your OTP is: {otp}"
        
        # Send email
        anvil.email.send(
            to=email,
            subject=subject,
            text=message
        )

        # Store the OTP in the server session
        anvil.server.session['stored_otp'] = otp

        print("OTP sent:", otp)
    else:
        print("Email not found. OTP not sent.")

@anvil.server.callable
def get_stored_otp():
    """
    Returns the stored OTP from the server session.
    """
    return anvil.server.session.get('stored_otp')
@anvil.server.callable
def validate_email(email):
    """
    Validates if the provided email exists in the database.
    """
    matching_users = app_tables.wallet_users.search(users_email=email)
    return bool(matching_users)

@anvil.server.callable
def generate_otp():
    """
    Generates a 6-digit OTP.
    """
    return ''.join(random.choice('0123456789') for _ in range(6))

@anvil.server.callable
def resizing_image(image_file):
    try:
        from PIL import Image, ImageDraw
        from io import BytesIO
        
        # Open the image file
        image = Image.open(BytesIO(image_file.get_bytes()))
        
        # Resize the image to a smaller size
        max_size = (200, 200)  # Adjust the maximum dimensions as needed
        image.thumbnail(max_size, Image.LANCZOS)
        
        # Convert image to RGBA if it has a different mode
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGBA")
        
        # Create a circular mask
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + image.size, fill=255)
        
        # Apply the mask to the image
        output_image = Image.new("RGBA", image.size)
        output_image.paste(image, (0, 0), mask=mask)
        
        # Save the processed image to a BytesIO object
        output = BytesIO()
        output_image.save(output, format="PNG")
        
        # Return the processed image as a media object
        return anvil.BlobMedia("image/png", output.getvalue(), name="resized_image.png")
    except Exception as e:
        print(f"Error in resizing_image: {e}")
        return None






@anvil.server.callable
def update_active_status():
    # Get today's date
    today = datetime.now().date()
    
    # Query all users from wallet_users
    all_users = app_tables.wallet_users.search()
    
    # Iterate through each user
    for user in all_users:
        # Get the last login date for the user
        last_login = user['users_last_login']
        
        # Calculate the difference in days between last login and today
        if last_login is not None:
            days_difference = (today - last_login.date()).days
            
            # Check if the difference is greater than 90 days
            if days_difference > 90:
                # Update the active column to False
                user['users_inactive'] = True
            else:
                # Update the active column to True
                user['users_inactive'] = None
                
            # Save the changes to the table
            user.update()

@anvil.server.callable
def get_credit_debit(phone_number,default_currency):
  debit_details = app_tables.wallet_users_transaction.search(users_transaction_phone=phone_number,users_transaction_currency=default_currency,users_transaction_type='Debit')
  credit_details = app_tables.wallet_users_transaction.search(users_transaction_receiver_phone = phone_number,users_transaction_currency=default_currency,users_transaction_receiver_type='Credit')
  return {'debit_details':debit_details,'credit_details':credit_details}
@anvil.server.callable
def update_user_limit(phone_number, field_to_update, new_limit):
    user = app_tables.wallet_users.get(users_phone=phone_number)
    if user:
        user[field_to_update] = new_limit
        return "Limit updated successfully"
    else:
        return "User not found"


@anvil.server.callable
def update_user_limit_by_phone(phone, field, new_limit):
    user = app_tables.wallet_users.get(users_phone=phone)  # Assuming phone is a unique identifier in your users table
    if user:
        user[field] = new_limit
    else:
        raise ValueError("User not found")


@anvil.server.callable
def notify(users_text,datetime,receiver_phone,sender):
  notify = app_tables.wallet_users_notifications.add_row(users_notification_date_time=datetime,users_notification_text=users_text,users_notification_phone=int(receiver_phone),users_notification_sender=sender)

@anvil.server.callable
def get_notifications(user_phone):
  a=app_tables.wallet_users_notifications.search(users_notification_phone=user_phone)
  return a



@anvil.server.callable
def update_user_status(item_id):
    row = app_tables.wallet_users_service.get_by_id(item_id)
    if row:
        row['users_update'] = True
        return row['users_update']
    return False

@anvil.server.callable
def update_user_conclusion(item_id, conclusion):
    row = app_tables.wallet_users_service.get_by_id(item_id)
    if row:
        row['users_conclusion_about_query'] = conclusion
        return True
    return False