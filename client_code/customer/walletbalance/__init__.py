from ._anvil_designer import walletbalanceTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class walletbalance(walletbalanceTemplate):
    def __init__(self, user=None, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.user = user

        username = anvil.server.call('get_username', self.user['phone'])
        self.label_6.text = f"Welcome to Green Gate Financial, {username}"

        # Populate balances for different currencies
        self.populate_balances()

    def populate_balances(self):
        # Retrieve balances for different currencies
        user_phone = self.user['phone']
        
        # Retrieve balance for INR
        inr_balance = anvil.server.call('get_currency_balance', user_phone, 'INR')
        self.text_box_1.text = str(inr_balance) if inr_balance is not None else '0'
        
        # Retrieve balance for USD
        usd_balance = anvil.server.call('get_currency_balance', user_phone, 'USD')
        self.text_box_2.text = str(usd_balance) if usd_balance is not None else '0'
        
        # Retrieve balance for EUR
        eur_balance = anvil.server.call('get_currency_balance', user_phone, 'EUR')
        self.text_box_3.text = str(eur_balance) if eur_balance is not None else '0'
        
        # Retrieve balance for GBP
        gbp_balance = anvil.server.call('get_currency_balance', user_phone, 'GBP')
        self.text_box_4.text = str(gbp_balance) if gbp_balance is not None else '0'

    def button_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('customer.deposit',user=self.user)

    def link_2_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.deposit',user=self.user)

    def link_3_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.transfer',user=self.user)

    def link_4_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.withdraw',user=self.user)

    def link_7_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.service',user=self.user)

    def link_1_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer',user=self.user)

    def link_13_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('Home')
