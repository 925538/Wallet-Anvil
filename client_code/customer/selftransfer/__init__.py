from ._anvil_designer import selftransferTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class selftransfer(selftransferTemplate):
    def __init__(self, user=None, **properties):
        # Initialize self.user as a dictionary 
        self.init_components(**properties) 
        self.user = user
        # Set Form properties and Data Bindings.
        username = anvil.server.call('get_username', self.user['phone'])
        self.label_1.text = f"Welcome to Green Gate Financial, {username}"
        
        # Call the server function to get bank names based on the user's phone number
        bank_iterator = anvil.server.call('get_user_bank_name', self.user['phone'])
        
        # Extract bank names from the iterator
        self.bank_names = [row['bank_name'] for row in bank_iterator]
        
        # Ensure that bank_names is a list of strings
        if isinstance(self.bank_names, list) and all(isinstance(item, str) for item in self.bank_names):
            # Add "Select sending bank account" as the first item in drop_down_1
            self.drop_down_1.items = ["Select sending bank account"] + self.bank_names
            # Add "Select receiver bank account" as the first item in drop_down_2
            self.drop_down_2.items = ["Select receiver bank account"] + self.bank_names
        else:
            # Handle the case where bank_names is not a list of strings
            # You might need to debug this and see what type bank_names is and handle it accordingly
            print("Error: bank_names is not a list of strings:", self.bank_names)
        
        # Ensure the form is visible
        self.visible = True

    def drop_down_1_change(self, **event_args):
      """This method is called when an item is selected in drop_down_1"""
      selected_bank = self.drop_down_1.selected_value
      print("Selected bank:", selected_bank)
      # If a bank is selected, remove it from the options of drop_down_2
      if selected_bank != "Select sending bank account":
          filtered_banks = [bank for bank in self.bank_names if bank != selected_bank]
          print("Filtered banks:", filtered_banks)
          self.drop_down_2.items = ["Select receiver bank account"] + filtered_banks


    def button_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      sending_bank = self.drop_down_1.selected_value
      receiving_bank = self.drop_down_2.selected_value
      
      if sending_bank == receiving_bank:
          alert("Please select different banks for sending and receiving.")
          return
      
      if sending_bank != "Select sending bank account" and receiving_bank != "Select receiver bank account":
          self.label_6.text = "Transaction success"
          self.text_box_1.text = f"Transaction details:\nSending bank: {sending_bank}\nReceiving bank: {receiving_bank}"
          self.drop_down_1.selected_value = "Select sending bank account"
          self.drop_down_2.selected_value = "Select receiver bank account"
      else:
          alert("Please select both sending and receiving banks before proceeding.")

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

    def link_13_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('Home')

    def button_2_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('customer',user=self.user)
