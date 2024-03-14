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

        # Convert LiveObjectProxy to dictionary
        user_dict = dict(self.user)

        # Assuming user has a 'phone' attribute
        phone_number = user_dict.get('phone', None)

        if phone_number:
            # Get the username using the 'get_username' server function
            username = anvil.server.call('get_username', phone_number)
            self.label_1.text = f"Welcome to Green Gate Financial, {username}"

            # Search transactions based on the user's phone number
            items = app_tables.wallet_users_transaction.search(phone=phone_number)

            # Sort the items based on the 'date' column in descending order
            sorted_items = sorted(items, key=lambda x: x['date'], reverse=True)

            # Assuming these columns exist in 'wallet_users_transaction'
            transaction_history_list = [
                {
                    'date': item['date'],
                    'fund': item['fund'],
                    'transaction_type': item['transaction_type'],
                    'transaction_status': item['transaction_status'],
                    'receiver_phone': item['receiver_phone'],
                    'phone': item['phone']
                }
                for item in sorted_items
            ]
            
            self.repeating_panel_1.items = transaction_history_list

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
  
    def link_1_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer',user=self.user)

    def button_3_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('customer',user=self.user)
