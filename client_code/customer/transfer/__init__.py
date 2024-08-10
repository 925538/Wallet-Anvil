from ._anvil_designer import transferTemplate
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

class transfer(transferTemplate):
    def __init__(self, user=None, **properties):
        # Initialize self.user as a dictionary 
        self.init_components(**properties) 
        self.user = user
        self.timer_1.interval = 3
        self.timer_1.enabled = False
        # Set Form properties and Data Bindings.
        username = anvil.server.call('get_username', self.user['users_phone'])
        #self.label_1.text = f"Welcome to Green Gate Financial, {username}"
        currencies=anvil.server.call('get_user_currency',self.user['users_phone'])
        self.drop_down_2.items= [str(row['users_balance_currency_type']) for row in currencies]
        self.display()
        self.populate_balances()
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
     

    def drop_down_1_change(self, **event_args):
      self.display()

    def display(self, **event_args):
      acc = self.drop_down_2.selected_value



    def currency_rate(self, currency_type, money):
        # Set API Endpoint and access key (replace 'API_KEY' with your actual API key)
        endpoint = 'convert'
        api_key = 'a2qfoReWfa7G3GiDHxeI1f9BFXYkZ2wT'
  
        # Set base currency and any other parameters (replace 'USD' with your desired base currency)
        base_currency = 'INR'
        target_currency = currency_type  # Replace with your desired target currency
        endpoint = 'convert'
        api_key = 'a2qfoReWfa7G3GiDHxeI1f9BFXYkZ2wT'
        # Set base currency and any other parameters 
        # base_currency = 'INR'
        # resp = anvil.http.request(f"https://api.currencybeacon.com/v1/{endpoint}?from={base_currency}&to={cur}&amount={money}&api_key={api_key}", json=True)
        # money_value=resp['response']['value']
        # Build the URL
        # url = f'https://api.currencybeacon.com/v1/{endpoint}?from={base_currency}&to={currency_type}&amount={money}&api_key={api_key}'
  
        try:
            # print(f"API URL: {url}")
            # Make the request
            resp = anvil.http.request(f"https://api.currencybeacon.com/v1/{endpoint}?from={base_currency}&to={target_currency}&amount={money}&api_key={api_key}", json=True)
            money_value=resp['response']['value']# Raise an HTTPError for bad responses
            print("gi",money_value)
            # Decode JSON response
            # exchange_rates = response.json()
            # print(f"Response: {exchange_rates}")
  
            return money_value
        except Exception as e:
           alert("error occured!!!.", buttons=[("OK", True)], large=True)
        # except Exception as e:
        #     print(e)
  
        # except anvil.http.request.exceptions.RequestException as err:
        #     print(f"Request Error: {err}")
        #     self.manager.show_notification('Alert!', 'An error occurred. Please try again.')
    
            # print(f"An unexpected error occurred: {e}")
            # self.manager.show_notification('Alert!', 'An error occurred. Please try again.')
  
    
    def top_up_if_balance_is_less(self):
      exchange_rate_value = None
      phone = self.user['users_phone']
      
      users_details = app_tables.wallet_users.get(users_phone=phone)
      default_primary = users_details['users_default_account']
      transactions = app_tables.wallet_users_account.get(users_account_number=int(default_primary))
  
      self.bank_name = transactions['users_account_bank_name']
      user_table = app_tables.wallet_users.get(users_phone=phone)
  
  
      today = datetime.today()
      formatted_date = today.strftime('%Y-%m-%d')
  
  
      if user_table['users_minimum_topup'] is True and  formatted_date <= str(user_table['users_auto_topup_expiry_date']):
          money = user_table['users_minimum_topup_amount']
          amount = float(money)
          if amount <= 0 or str(amount).startswith('0'):
                                
              return
          selected_money = int(user_table['users_minimum_topup_amount_below'])
          date = datetime.now()
          # currency_dropdown = self.parent.ids.currency_dropdown
          currency = users_details['users_defaultcurrency']
          rate_response = self.currency_rate(currency, amount)
          print(rate_response)
          try:
              if rate_response:
                  # Access the 'value' from the 'response' dictionary
                  exchange_rate_value =rate_response
                  print(f"The exchange rate value is: {exchange_rate_value}")
              else:
                alert("error occured!!!.", buttons=[("OK", True)], large=True)
                
          except Exception as e:
              
            pass
              # self.manager.show_notification('Alert!', 'An error occurred. Please try again.')
  
        
          phone = self.user['users_phone']
          balance_table = app_tables.wallet_users_balance.get(users_balance_phone=phone,
                                                              users_balance_currency_type=currency)
          print(balance_table)
  
          try:
              if balance_table is not None:
                  old_balance = balance_table['users_balance']
                  user_table['users_minimum_topup'] = True
  
                  if old_balance < float(selected_money):
  
  
  
                      new_balance = old_balance + exchange_rate_value
                      balance_table['users_balance'] = new_balance
                      balance_table.update()
                      # self.manager.show_notification('Success', 'Minimum-Topup Successful.')
                      app_tables.wallet_users_transaction.add_row(
                          users_transaction_receiver_phone=None,
                          users_transaction_phone=phone,
                          users_transaction_fund=exchange_rate_value,
                          users_transaction_date=date,
                          users_transaction_type=f"Auto Topup",
                          users_transaction_status="Minimum-Topup",
                          users_transaction_currency=currency,
                          users_transaction_bank_name=self.bank_name
                      )
                      # app = App.get_running_app()
                      # app.root.current = 'dashboard'
                      # self.ids.edit_topUp.text = "Edit"
  
                      users_text = f" {amount} Added Through AutoTopUp"
                      anvil.server.call('notify', users_text, date, phone, phone)
                  else:
                      pass
                      # user_table['users_minimum_topup_amount_below'] = int(selected_money)
                      # user_table['users_auto_topup_expiry_date'] = self.topup_expiry_date
                      #
                      # user_table.update()
                      # user_table['users_minimum_topup'] = False
                      # self.manager.show_notification('Success', 'Minimum-Topup Successful.')
                      # self.ids.edit_topUp.text = "Edit"
              else:
                  pass
                  # self.manager.show_notification('Alert!', f"Insufficient balance in currency {currency}")
                  # print(self.bank_details_display)
  
              # app_tables.wallet_users_transaction.add_row(
              #     users_transaction_receiver_phone=None,
              #     users_transaction_phone=phone,
              #     users_transaction_fund=self.exchange_rate_value,
              #     users_transaction_date=date,
              #     users_transaction_type=f"Auto Topup",
              #     users_transaction_status="Minimum-Topup",
              #     users_transaction_currency=currency,
              #     users_transaction_bank_name=self.bank_name
              # )
          except Exception as e:
              print(f"Error minimum-topup money: {e}")
              alert("error occured!!!.", buttons=[("OK", True)], large=True)
              # self.manager.show_notification('Alert!', 'An error occurred. Please try again.')
              # self.balance.text = ""
      else:
          pass
          # self.manager.show_notification('Alert!', 'Please enable the auto-topup switch to proceed.')
  
  

  
    def button_1_click(self, **event_args):
      current_datetime = datetime.now()
      receiver_phone_number = float(self.text_box_2.text)
      transfer_amount = float(self.text_box_3.text)
      cur = self.drop_down_2.selected_value
      depositor_phone_number = self.user['users_phone']
      
      
      
      # Use the entered phone number to identify the receiver's account
      receiver_balance = app_tables.wallet_users_balance.get(users_balance_phone=receiver_phone_number, users_balance_currency_type=cur)
      depositor_balance = app_tables.wallet_users_balance.get(users_balance_phone=depositor_phone_number, users_balance_currency_type=cur)
      if transfer_amount >0:
        if depositor_balance:
            depositor = app_tables.wallet_users.get(users_phone=depositor_phone_number)
            
            users_daily_limit = depositor['users_daily_limit']
            users_user_limit = depositor['users_user_limit']
            
            if transfer_amount > users_daily_limit:
                anvil.alert("Daily limit exceeded.")
            elif transfer_amount > users_user_limit:
                anvil.alert("Monthly limit exceeded.")
            else:
                money_value = transfer_amount if transfer_amount else 0.0
                if depositor_balance['users_balance'] >= money_value:
                    if receiver_balance:
                        depositor_balance['users_balance'] -= money_value
                        receiver_balance['users_balance'] += money_value
                    else:
                        receiver = app_tables.wallet_users.get(users_phone=receiver_phone_number)
                        if receiver:
                            depositor_balance['users_balance'] -= money_value
                            app_tables.wallet_users_balance.add_row(
                                users_balance_currency_type=cur,
                                users_balance=money_value,
                                users_balance_phone=receiver_phone_number
                            )
                        else:
                            anvil.alert("User does not exist")
                            return
                    
                    # new_transaction = app_tables.wallet_users_transaction.add_row(
                    #     users_transaction_phone=depositor_phone_number,
                    #     users_transaction_fund=money_value,
                    #     users_transaction_currency=cur,
                    #     users_transaction_date=current_datetime,
                    #     users_transaction_type="Debit",
                    #     users_transaction_status="transferred-to",
                    #     users_transaction_receiver_phone=receiver_phone_number
                    # )
                    # new_transaction = app_tables.wallet_users_transaction.add_row(
                    #     users_transaction_phone=receiver_phone_number,
                    #     users_transaction_fund=money_value,
                    #     users_transaction_currency=cur,
                    #     users_transaction_date=current_datetime,
                    #     users_transaction_type="Credit",
                    #     users_transaction_status="received-from",
                    #     users_transaction_receiver_phone=depositor_phone_number
                    # )
  
                    new_transaction = app_tables.wallet_users_transaction.add_row(
                        users_transaction_phone=depositor_phone_number,
                        users_transaction_fund=money_value,
                        users_transaction_currency=cur,
                        users_transaction_date=current_datetime,
                        users_transaction_type="Debit",
                        users_transaction_receiver_type="Credit",
                        users_transaction_status="transferred-to",
                        users_transaction_receiver_phone=receiver_phone_number,
                    )
          
                    users_text=f"You have received **{self.drop_down_2.selected_value} {self.text_box_3.text}**from {self.user['users_username']}"
                    anvil.server.call('notify',users_text,current_datetime,self.text_box_2.text,self.user['users_phone'])
                  
                    # Update the limits after successful transaction
                    depositor['users_daily_limit'] -= money_value
                    depositor['users_user_limit'] -= money_value
    
                    #self.label_4.text = "Money transferred successfully to the account"
                    alert("Money transferred successfully to the account")
                    self.populate_balances()
                    self.top_up_if_balance_is_less()
                else:
                    anvil.alert("Insufficient balance. Please add funds")
        else:
            #self.label_4.text = "Error: No matching accounts found for the user or invalid account number"
            alert("Error: No matching accounts found for the user or invalid account number")
    
        open_form('customer.transfer', user=self.user)
      else:
        alert(f"payment amount must be atleast 1 {cur}")
    def link_8_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.wallet",user=self.user)

    def link_2_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.deposit",user=self.user)

    def link_3_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.transactions",user=self.user)

    def link_4_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.transfer",user=self.user)

    def link_7_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.service",user=self.user)

    def link_1_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer",user=self.user)

    def link_13_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("Home")

    def link_10_click(self, **event_args):
      open_form('customer.deposit',user=self.user)

    def link_5_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.withdraw',user=self.user)

    def link_6_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.auto_topup',user=self.user)

    def text_box_2_pressed_enter(self, **event_args):
      """This method is called when the user presses Enter in this text box"""
      pass

    def link_8_copy_2_click(self, **event_args):
      open_form("customer.settings",user =self.user)

    def link_help_click(self, **event_args):
      open_form("help",user = self.user)

  

    def text_box_3_change(self, **event_args):
      """This method is called when the text in this text box is edited"""
      user_input = self.text_box_3.text
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
        self.text_box_3.text = filtered_text
        return
  
      try:
        processed_value = self.process_input(filtered_text)
        self.text_box_3.text = processed_value
      except ValueError:
        self.text_box_3.text = filtered_text
  
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




