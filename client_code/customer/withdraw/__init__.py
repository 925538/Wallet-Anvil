from ._anvil_designer import withdrawTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class withdraw(withdrawTemplate):
  def __init__(self, user=None, **properties):
    # Initialize self.user as a dictionary
    self.init_components(**properties)
    self.user = user
    # Set Form properties and Data Bindings.
    username = anvil.server.call('get_username', self.user['users_phone'])
    self.timer_1.interval = 3
    self.timer_1.enabled = False
    #self.label_1.text = f"Welcome to Green Gate Financial, {username}"
    bank_names = anvil.server.call('get_user_bank_name', self.user['users_phone'])
    
    currencies=anvil.server.call('get_user_currency',self.user['users_phone'])
    self.drop_down_1.items = [str(row['users_account_bank_name']) for row in bank_names]
    self.drop_down_2.items= [str(row['users_balance_currency_type']) for row in currencies]
    self.display()
    self.populate_balances()
    
  def drop_down_1_change(self, **event_args):
    self.display()
  def populate_balances(self):
      try:
          # Retrieve balances for the current user
          user_phone = self.user['users_phone']
          user_balances = app_tables.wallet_users_balance.search(users_balance_phone=user_phone)
  
          # Print the retrieved data
          print("Retrieved balances:", user_balances)
  
          # Initialize index for card and components
          card_index = 1
          label_index = 1  # Start from label_1
          country_label_index = 50  # Start from label_50 for country
          image_index = 1
  
          # Iterate over user balances and update card components
          for balance in user_balances:
             
              currency_type = balance['users_balance_currency_type']
              balance_amount = round(balance['users_balance'], 2)  # Round to 2 decimal places
  
              # Lookup the currency icon, symbol, and country in the wallet_currency table
              currency_record = app_tables.wallet_admins_add_currency.get(admins_add_currency_code=currency_type)
              currency_icon = currency_record['admins_add_currency_icon'] if currency_record else None
              country = currency_record['admins_add_currency_country'] if currency_record else None
                   
              # Get card and components for the current index
              card = getattr(self, f'card_{card_index}', None)
              label_curr_type = getattr(self, f'label_{label_index}', None)
              label_balance = getattr(self, f'label_{label_index + 1}', None)
              label_country = getattr(self, f'label_{country_label_index}', None)
              image_icon = getattr(self, f'image_icon_{image_index}', None)
  
              if card and label_curr_type and label_balance and image_icon and label_country:
                  # Update card components with balance data
                  label_curr_type.text = currency_type
                  label_balance.text = f"{balance_amount:.2f}"  # Format to 2 decimal places
                  label_balance.icon = f"fa:{currency_type.lower()}"
                  label_country.text = country
                  image_icon.source = currency_icon
  
                  # Align icon and text closer together if possible
                  # Adjust layout properties depending on your framework
                  # Example: label_balance.icon_style = "margin-right: 5px;"  # Adjust as needed
  
                  # Set card visibility to True
                  card.visible = True
  
                  # Increment indices for the next iteration
                  card_index += 1
                  label_index += 2
                  country_label_index += 1
                  image_index += 1
  
          # Set visibility of remaining cards to False if no data
          while card_index <= 12:
              card = getattr(self, f'card_{card_index}', None)
              if card:
                  card.visible = False
              card_index += 1
  
      except Exception as e:
          # Print any exception that occurs during the process
          print("Error occurred during population of balances:", e)
  def display(self, **event_args):
    acc = self.drop_down_1.selected_value

  def button_1_click(self, **event_args):
    current_datetime = datetime.now()
    acc = self.drop_down_1.selected_value
    cur = self.drop_down_2.selected_value
    money_value = float(self.text_box_2.text)

    if money_value >0:
      if acc is None or cur is None:
          alert('Please enter bank details')
      else:
          if self.user:
              # Retrieve user data
              user_data = app_tables.wallet_users.get(users_phone=self.user['users_phone'])
              if not user_data:
                  self.label_2.text = "Error: No matching accounts found for the user."
                  return
              
              users_daily_limit = user_data['users_daily_limit']
              users_user_limit = user_data['users_user_limit']
  
              # Check the limits
              if money_value > users_daily_limit:
                  alert("Daily limit exceeded.", buttons=[("OK", True)], large=True)
                  open_form('customer', user=self.user)
                  return
              elif money_value > users_user_limit:
                  alert("Monthly limit exceeded.", buttons=[("OK", True)], large=True)
                  open_form('customer', user=self.user)
                  return
              
              # Check if a balance row already exists for the user
              existing_balance = app_tables.wallet_users_balance.get(users_balance_phone=self.user['users_phone'], users_balance_currency_type=cur)
  
              if existing_balance and existing_balance['users_balance'] >= money_value:
                  # Update the existing balance
                  existing_balance['users_balance'] -= money_value
  
                  # Add a new transaction row
                  app_tables.wallet_users_transaction.add_row(
                      users_transaction_phone=self.user['users_phone'],
                      users_transaction_fund=money_value,
                      users_transaction_currency=cur,
                      users_transaction_date=current_datetime,
                      users_transaction_bank_name=acc,
                      users_transaction_type="Withdrawn",
                      users_transaction_status="Wallet-Withdraw",
                      users_transaction_receiver_phone=self.user['users_phone']
                  )
                  alert("Money withdrawn successfully from the account")
              else:
                  alert("Withdraw amount is more than the available balance")
  
              # Update the limits
              user_data['users_daily_limit'] -= money_value
              user_data['users_user_limit'] -= money_value
  
              self.populate_balances()
          else:
              alert("Error: No matching accounts found for the user or invalid account number.")

    else:
      alert(f"withdraw amount must be atleast 1 {cur}")
  def link_2_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.walletbalance",user=self.user)

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer.transactions",user=self.user)

  def link_7_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer.Viewprofile",user=self.user)

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer",user=self.user)

  def link_13_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("Home")

  def link_8_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer.wallet",user=self.user)  # Any code you write here will run before the form opens.

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('customer.transfer',user=self.user)

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('customer.wallet',user=self.user)

  def link_10_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('customer.deposit',user=self.user)

  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('customer.auto_topup',user=self.user)

  def link_5_copy_click(self, **event_args):
    open_form("help",user=self.user)

  def link_9_click(self, **event_args):
    open_form("customer.settings",user = self.user)

  def link_5_click(self, **event_args):
    open_form("customer.withdraw",user = self.user)

  def text_box_2_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    user_input = self.text_box_2.text
    print("Raw input:", user_input)
    
    allowed_characters = "0123456789."

    # Filter out any invalid characters and allow only one decimal point
    filtered_text = ''
    decimal_point_count = 0
    
    for char in user_input:
      if char in allowed_characters:
        if char == '.':
          decimal_point_count += 1
          if decimal_point_count > 1:
            continue
        filtered_text += char

    # Allow empty string and string with just a decimal point
    if filtered_text == '' or filtered_text == '.':
      self.text_box_2.text = filtered_text
      return

    try:
      processed_value = self.process_input(filtered_text)
      self.text_box_2.text = processed_value
    except ValueError:
      self.text_box_2.text = filtered_text

  def process_input(self, user_input):
    # Check if the input ends with a decimal point
    if user_input.endswith('.'):
      return user_input
    
    value = float(user_input)
    
    if value.is_integer():
      # If it's an integer, format without decimals
      formatted_value = '{:.0f}'.format(value)
    else:
      # If it's a float, format with significant digits
      formatted_value = '{:.15g}'.format(value)

    return formatted_value

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    pass

 

