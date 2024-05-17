from ._anvil_designer import transaction_historyTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class transaction_history(transaction_historyTemplate):
    def __init__(self, user=None, **properties):
        # Initialize self.user as a dictionary 
        self.user = user
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # self.container_panel.overflow = "auto"

        # Convert LiveObjectProxy to dictionary
        user_dict = dict(self.user)

        # Assuming user has a 'phone' attribute
        phone_number = user_dict.get('phone', None)
        if phone_number is not None:
            # self.text_box_4.text = phone_number  # Set textbox13 to display the phone number

            # Fetch all rows from wallet_users_balance table based on phone number
            user_balances = app_tables.wallet_users_balance.search(phone=phone_number)
            if user_balances:
                # Initialize balances for each currency type
                usd_balance = euro_balance = inr_balance = swiss_balance = None
                
                # Iterate over all matching rows
                for balance_row in user_balances:
                    # Check currency type and update corresponding balances
                    if balance_row['currency_type'] == 'USD':
                        usd_balance = balance_row['balance']
                    elif balance_row['currency_type'] == 'EUR':
                        euro_balance = balance_row['balance']
                    elif balance_row['currency_type'] == 'INR':
                        inr_balance = balance_row['balance']
                    elif balance_row['currency_type'] == 'GBP':
                        swiss_balance = balance_row['balance']
                
                # Update text boxes with the retrieved balances
                self.label_12.text = str(usd_balance) if usd_balance is not None else "0"
                self.label_11.text = str(euro_balance) if euro_balance is not None else "0"
                self.label_10.text = str(inr_balance) if inr_balance is not None else "0"
                self.label_9.text = str(swiss_balance) if swiss_balance is not None else "0"
            else:
                # Set default value of 0 for all text boxes if no balances found
                self.label_10.text = "0"
                self.label_11.text = "0"
                self.label_12.text = "0"
                self.label_13.text = "0"
            
        if phone_number:
          # Get the username using the 'get_username' server function
          username = anvil.server.call('get_username', phone_number)
          self.label_1.text = f"Welcome to Green Gate Financial, {username}"
          self.label_4.text = username
                      
          # Search transactions based on the user's phone number
          items = app_tables.wallet_users_transaction.search(phone=phone_number)
      
          # Group transactions by date
          self.grouped_transactions = {}
          for item in items:
              # Extract date in YYYY-MM-DD format without time
              date_str = item['date'].strftime("%Y-%m-%d")
              if date_str not in self.grouped_transactions:
                  self.grouped_transactions[date_str] = {'date': item['date'], 'transactions': []}
              self.grouped_transactions[date_str]['transactions'].append(item)
      
          # Sort dates in descending order
          sorted_dates = sorted(self.grouped_transactions.keys(), reverse=True)
      
          # Create a list of dictionaries for repeating_panel_1
          repeating_panel_1_items = []
          for date_str in sorted_dates:
              date_info = self.grouped_transactions[date_str]
              for transaction in reversed(date_info['transactions']):
                  fund = transaction['fund']
                  transaction_type = transaction['transaction_type']
                  receiver_phone = transaction['receiver_phone']
                  
                  # Fetch username from wallet_user table using receiver_phone
                  receiver_user = app_tables.wallet_users.get(phone=receiver_phone)
                  if receiver_user:
                      receiver_username = receiver_user['username']
                  else:
                      receiver_username = "Unknown"
                  
                  if transaction_type == 'credit':
                      fund_display = "+" + str(fund)
                      fund_color = "green"
                  elif transaction_type == 'debit':
                      fund_display = "-" + str(fund)
                      fund_color = "red"
                  else:
                      fund_display = str(fund)
                      fund_color = "black"
                  
                  # Append transaction details with username instead of receiver_phone
                  repeating_panel_1_items.append({'date': date_info['date'].strftime("%Y-%m-%d"),
                                                  'fund': fund_display,
                                                  'transaction_status': transaction['transaction_status'],
                                                  'receiver_username': receiver_username,
                                                  'fund_color': fund_color})
      
          self.repeating_panel_1.items = repeating_panel_1_items

    def link_2_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form("customer.deposit",user=self.user)
    
    def link_3_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form("customer.transfer",user=self.user)
    
    def link_4_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form("customer.withdraw",user=self.user)
    
    def link_7_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form("customer.service",user=self.user)
    
    def link_13_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form("Home")
    
    def link_8_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form("customer.service",user=self.user)
    
    def button_3_click(self, **event_args):
        open_form('customer', user=self.user)

    def link_1_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('customer_page',user=self.user)

    def link_24_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('about_us')

    def link_25_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('product')

    def primary_color_8_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass

    def text_box_1_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        receiver_phone = self.text_box_1.text.strip()
        if receiver_phone:
            # Display transactions for the entered receiver's phone number
            self.update_transactions_by_receiver(receiver_phone)

    def update_transactions_by_receiver(self, receiver_phone):
        
        receiver_phone_number = int(receiver_phone)  # Convert string to integer
        """Update the transaction history based on the receiver's phone number"""
        receiver_user = app_tables.wallet_users.get(phone=receiver_phone_number)
        if receiver_user:
            receiver_username = receiver_user['username']
        else:
            receiver_username = "Unknown"
    
        items = app_tables.wallet_users_transaction.search(receiver_phone=receiver_phone_number)
        # Rest of the method remains the same...
        grouped_transactions = {}
        for item in items:
            # Extract date in YYYY-MM-DD format without time
            date_str = item['date'].strftime("%Y-%m-%d")
            if date_str not in grouped_transactions:
                grouped_transactions[date_str] = {'date': item['date'], 'transactions': []}
            grouped_transactions[date_str]['transactions'].append(item)

        # Sort dates in descending order
        sorted_dates = sorted(grouped_transactions.keys(), reverse=True)

        # Create a list of dictionaries for repeating_panel_1
        repeating_panel_1_items = []
        for date_str in sorted_dates:
            date_info = grouped_transactions[date_str]
            # repeating_panel_1_items.append({'date': date_info['date'].strftime("%Y-%m-%d")})  # Format date without time
            for transaction in reversed(date_info['transactions']):
                fund = transaction['fund']
                transaction_type = transaction['transaction_type']
                if transaction_type == 'credit':
                    fund_display = "+" + str(fund)
                    fund_color = "forestgreen"
                elif transaction_type == 'debit':
                    fund_display = "-" + str(fund)
                    fund_color = "red"
                else:
                    fund_display = str(fund)
                    fund_color = "black"
                repeating_panel_1_items.append({'date': date_info['date'].strftime("%Y-%m-%d"),'fund': fund_display,'transaction_status':transaction['transaction_status'], 'receiver_username': receiver_username, 'fund_color': fund_color})

        self.repeating_panel_1.items = repeating_panel_1_items

    def drop_down_1_change(self, **event_args):
        """This method is called when the month dropdown selection changes"""
        selected_month = self.drop_down_1.selected_value
        selected_year = self.drop_down_2.selected_value
        if selected_month and selected_year:
            self.update_repeating_panel(selected_month, selected_year)

    def drop_down_2_change(self, **event_args):
        """This method is called when the year dropdown selection changes"""
        selected_month = self.drop_down_1.selected_value
        selected_year = self.drop_down_2.selected_value
        if selected_month and selected_year:
            self.update_repeating_panel(selected_month, selected_year)

    def update_repeating_panel(self, selected_month, selected_year):
      """Update the repeating panel with transactions for the selected month and year"""
      repeating_panel_1_items = []
      selected_month = int(selected_month)
      selected_year = int(selected_year)
      for date_str, date_info in self.grouped_transactions.items():
          date = date_info['date']
          if date.month == selected_month and date.year == selected_year:
              for transaction in reversed(date_info['transactions']):
                  fund = transaction['fund']
                  transaction_type = transaction['transaction_type']
                  receiver_phone = transaction['receiver_phone']
                  
                  # Fetch username from wallet_user table using receiver_phone
                  receiver_user = app_tables.wallet_users.get(phone=receiver_phone)
                  if receiver_user:
                      receiver_username = receiver_user['username']
                  else:
                      receiver_username = "Unknown"
                  
                  if transaction_type == 'credit':
                      fund_display = "+" + str(fund)
                      fund_color = "green"
                  elif transaction_type == 'debit':
                      fund_display = "-" + str(fund)
                      fund_color = "red"
                  else:
                      fund_display = str(fund)
                      fund_color = "black"
                      
                  # Append transaction details with username instead of receiver_phone
                  repeating_panel_1_items.append({'date': date_info['date'].strftime("%Y-%m-%d"),
                                                  'fund': fund_display,
                                                  'transaction_status': transaction['transaction_status'],
                                                  'receiver_username': receiver_username,
                                                  'fund_color': fund_color})
      self.repeating_panel_1.items = repeating_panel_1_items

    def drop_down_3_change(self, **event_args):
      """This method is called when the transaction type dropdown selection changes"""
      selected_transaction_type = self.drop_down_3.selected_value
      
      # Update transactions based on the selected transaction type
      if selected_transaction_type:
          self.update_transactions_by_type(selected_transaction_type)
  
    def update_transactions_by_type(self, transaction_type):
      """Update the transaction history based on the selected transaction type"""
      # Convert the transaction_type to lowercase to match the stored format
      transaction_type_lower = transaction_type.lower()
      
      # Print out the transaction_type_lower to see what values are being checked
      print("Transaction Type:", transaction_type_lower)
      
      # Search for transactions with the lowercase transaction_type
      items = app_tables.wallet_users_transaction.search(transaction_type=transaction_type_lower)

      grouped_transactions = {}
      for item in items:
          # Extract date in YYYY-MM-DD format without time
          date_str = item['date'].strftime("%Y-%m-%d")
          if date_str not in grouped_transactions:
              grouped_transactions[date_str] = {'date': item['date'], 'transactions': []}
          grouped_transactions[date_str]['transactions'].append(item)
  
      # Sort dates in descending order
      sorted_dates = sorted(grouped_transactions.keys(), reverse=True)
  
      # Create a list of dictionaries for repeating_panel_1
      repeating_panel_1_items = []
      for date_str in sorted_dates:
          date_info = grouped_transactions[date_str]
          for transaction in reversed(date_info['transactions']):
              fund = transaction['fund']
              transaction_status = transaction['transaction_status']
              receiver_phone = transaction['receiver_phone']
              
              # Fetch username from wallet_user table using receiver_phone
              receiver_user = app_tables.wallet_users.get(phone=receiver_phone)
              if receiver_user:
                  receiver_username = receiver_user['username']
              else:
                  receiver_username = "Unknown"
              
              # Print out the actual transaction type to see what values are stored
              print("Actual Transaction Type:", transaction['transaction_type'])
              
              if transaction_type_lower == 'credit':
                  fund_display = "+" + str(fund)
                  fund_color = "green"
              elif transaction_type_lower == 'debit':
                  fund_display = "-" + str(fund)
                  fund_color = "red"
              else:
                  fund_display = str(fund)
                  fund_color = "black"
                  
              # Append transaction details with username instead of receiver_phone
              repeating_panel_1_items.append({'date': date_info['date'].strftime("%Y-%m-%d"),
                                              'fund': fund_display,
                                              'transaction_status': transaction_status,
                                              'receiver_username': receiver_username,
                                              'fund_color': fund_color})
  
      self.repeating_panel_1.items = repeating_panel_1_items

    def drop_down_4_change(self, **event_args):
      """This method is called when an item is selected"""
      selected_option = self.drop_down_4.selected_value
      
      if selected_option == "Type":
          # Show dropdown and card for Type
          self.drop_down_3.visible = True
          self.card_3.visible = True
          self.label_13.visible = True
          # Hide other elements
          self.label_5.visible = False
          self.label_2.visible = False
          self.drop_down_1.visible = False
          self.drop_down_2.visible = False
          self.label_3.visible = False
      elif selected_option == "Date":
          # Show elements for Date
          self.label_5.visible = True
          self.label_2.visible = True
          self.label_3.visible = True
          self.drop_down_1.visible = True
          self.drop_down_2.visible = True
          self.card_3.visible = True
          # Hide other elements
          self.drop_down_3.visible = False
          self.label_13.visible = False
      elif selected_option =="filter":
          self.drop_down_3.visible = False
          self.card_3.visible = False
          self.label_13.visible = False
          # Hide other elements
          self.label_5.visible = False
          self.label_2.visible = False
          self.drop_down_1.visible = False
          self.drop_down_2.visible = False
          self.label_3.visible = False
          

     
  
