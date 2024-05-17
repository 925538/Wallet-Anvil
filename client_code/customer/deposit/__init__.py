from ._anvil_designer import depositTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
import anvil.http
class deposit(depositTemplate):
    def __init__(self,user=None, **properties):
        # Initialize self.user as a dictionary
      self.init_components(**properties)
      self.user = user
      # Set Form properties and Data Bindings.
      username = anvil.server.call('get_username', self.user['phone'])
      self.label_1.text = f"Welcome to Green Gate Financial, {username}"
      bank_names = anvil.server.call('get_user_bank_name', self.user['phone'])
      self.drop_down_1.items = [str(row['bank_name']) for row in bank_names]
      self.drop_down_2.items= anvil.server.call('get_currency_code')
      self.display()

    def button_1_click(self, **event_args):
        current_datetime = datetime.now()
        acc = self.drop_down_1.selected_value
        cur=self.drop_down_2.selected_value
        money=float(self.text_box_2.text)
        endpoint = 'convert'
        api_key = 'a2qfoReWfa7G3GiDHxeI1f9BFXYkZ2wT'
        # Set base currency and any other parameters (replace 'USD' with your desired base currency)
        base_currency = 'INR'
        resp = anvil.http.request(f"https://api.currencybeacon.com/v1/{endpoint}?from={base_currency}&to={cur}&amount={money}&api_key={api_key}", json=True)
        money_value=resp['response']['value']
        if self.user :
            # Check if a balance row already exists for the user
            existing_balance = app_tables.wallet_users_balance.get(phone=self.user['phone'],currency_type=cur)

            if existing_balance:
                # Update the existing balance
                existing_balance['balance'] += money_value
            else:
                # Add a new row for the user if no existing balance
                balance = app_tables.wallet_users_balance.add_row(
                    currency_type=cur,  # Replace with the actual currency type
                    balance=money_value,
                    phone=self.user['phone']
                )

            # Add a new transaction row
            new_transaction = app_tables.wallet_users_transaction.add_row(
                phone=self.user['phone'],
                fund=money_value,
                currency=cur,
                date=current_datetime,
                transaction_type="Deposited",
                transaction_status="Wallet-Topup",
                receiver_phone=None
            )

            self.label_2.text = "Money added successfully to the account."
        else:
            self.label_2.text = "Error: No matching accounts found for the user or invalid account number."

    def drop_down_1_change(self, **event_args):
        self.display()

    def display(self, **event_args):
        acc = self.drop_down_1.selected_value

    def display(self, **event_args):
          acc=self.drop_down_1.selected_value
        
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

    def link_1_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer_page",user=self.user)

    def link_13_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("Home")

    def link_8_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.service",user=self.user)
    def label_7_copy_2_copy(self, **event_args):
      open_form("customer",user=self.user)
