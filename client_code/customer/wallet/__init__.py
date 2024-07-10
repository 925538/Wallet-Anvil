from ._anvil_designer import walletTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import alert, get_open_form
import random

class wallet(walletTemplate):
    global  count
    def __init__(self, user=None, **properties):
        self.init_components(**properties)
        self.user = user
        
        #self.label_1.text = f"Welcome to Green Gate Financial, {user['users_username']}"
        self.bank_details_visible = False
        self.label_bank_details_error = Label(text="", role="alert")
        self.label_bank_name.visible = False
        self.drop_down_2.visible = False
        self.label_account_number.visible = False
        self.textbox_account_number.visible = False
        self.label_ifsc_code.visible = False
        self.textbox_ifsc_code.visible = False
        self.label_bank_details_error.visible = False
        self.button_save_bank_details.visible = False
        self.label_333.visible=False
        self.label_4444.visible=False
        # self.label_555.visible=False
        self.text_box_1.visible=False
        self.text_box_2.visible=False
        # self.drop_down_1.visible=False
        self.populate_balances()
    def populate_balances(self):
      try:
          # Retrieve accounts for the current user
          user_phone = self.user['users_phone']
          user_accounts = app_tables.wallet_users_account.search(users_account_phone=user_phone)
  
          # Print the retrieved data
          print("Retrieved accounts:", user_accounts)
  
          # Initialize index for card and components
          card_index = 1
          label_index = 1  # Start from label_1
          account_label_index = 50  # Start from label_50 for account number
          image_index = 1
  
          # Iterate over user accounts and update card components
          for account in user_accounts:
              bank_name = account['users_account_bank_name']
              account_number = account['users_account_number']
  
              # Lookup the bank icon in the wallet_admins_add_bank table
              bank_record = app_tables.wallet_admins_add_bank.get(admins_add_bank_names=bank_name)
              bank_icon = bank_record['admins_add_bank_icons'] if bank_record else None
  
              # Get card and components for the current index
              card = getattr(self, f'card_{card_index}', None)
              label_bank_name = getattr(self, f'label_{label_index}', None)
              label_account_number = getattr(self, f'label_{account_label_index}', None)
              image_icon = getattr(self, f'image_icon_{image_index}', None)
  
              if card and label_bank_name and label_account_number and image_icon:
                  # Update card components with account data
                  label_bank_name.text = bank_name
                  label_account_number.text = account_number
                  image_icon.source = bank_icon
  
                  # Set card visibility to True
                  card.visible = True
  
                  # Increment indices for the next iteration
                  card_index += 1
                  label_index += 2
                  account_label_index += 1
                  image_index += 1
  
          # Set visibility of remaining cards to False if no data
          while card_index <= 12:
              card = getattr(self, f'card_{card_index}', None)
              if card:
                  card.visible = False
              card_index += 1
  
      except Exception as e:
          # Print any exception that occurs during the process
          print("Error occurred during population of accounts:", e)


    def button_add_bank_details_click_click(self, **event_args):
       # Toggle the visibility of bank details labels and textboxes
        self.bank_details_visible = not self.bank_details_visible
        self.label_bank_name.visible = self.bank_details_visible
        self.drop_down_2.visible = self.bank_details_visible
        self.label_account_number.visible = self.bank_details_visible
        self.textbox_account_number.visible = self.bank_details_visible
        self.label_ifsc_code.visible = self.bank_details_visible
        self.textbox_ifsc_code.visible = self.bank_details_visible
        self.button_save_bank_details.visible = self.bank_details_visible
        self.label_333.visible=self.bank_details_visible
        self.label_4444.visible=self.bank_details_visible
        # self.label_555.visible=self.bank_details_visible
        self.text_box_1.visible=self.bank_details_visible
        self.text_box_2.visible=self.bank_details_visible
        # self.drop_down_1.visible=self.bank_details_visible
        self.drop_down_2.items = anvil.server.call('get_all_banks_name')
        
        self.label_bank_details_error.text = ""
       
    def button_save_bank_details_click(self, **event_args):
      bank_name = self.drop_down_2.selected_value
      account_number = self.textbox_account_number.text
      ifsc_code = self.textbox_ifsc_code.text
      account_holder_name = self.text_box_1.text
      branch_name = self.text_box_2.text
      
  
      if not (bank_name and account_number and ifsc_code and account_holder_name and branch_name):
          anvil.alert("Please fill in all bank details.", title="", large=True)
          return
  
      # Validate account number
      try:
          account_number = int(account_number)
          if len(str(account_number)) < 11 or len(str(account_number)) > 16:
              anvil.alert("Account number must be between 11 and 16 digits.", title="", large=True)
              return
      except ValueError:
          anvil.alert("Account number must be a valid number.", title="", large=True)
          return
  
      # Validate IFSC code (assuming standard format of 4 letters followed by 7 digits)
      if not (len(ifsc_code) == 11 and ifsc_code[:4].isalpha() and ifsc_code[4] == '0' and ifsc_code[5:].isalnum()):
          anvil.alert("IFSC code must be 11 characters long, with the first 4 letters alphabetic, the 5th character '0', and the last 6 alphanumeric.", title="", large=True)
          return
  
      # Check for duplicate bank name and account number for the current user
      user_accounts = app_tables.wallet_users_account.search(users_account_phone=self.user['users_phone'])
      for account in user_accounts:
          if account['users_account_bank_name'] == bank_name:
              anvil.alert("Bank already exists.", title=" Bank Name", large=True)
              return
  
      # Check for duplicate account number in the entire table
      duplicate_account = app_tables.wallet_users_account.get(users_account_number=account_number)
      if duplicate_account:
          anvil.alert("Account number already exists.", title="Duplicate Account Number", large=True)
          return
  
      # Add the new account if no duplicates are found
      new_account = app_tables.wallet_users_account.add_row(
          users_account_phone=self.user['users_phone'],
          users_account_number=int(account_number),
          users_account_bank_name=bank_name, 
          users_account_ifsc_code=ifsc_code,
          users_account_holder_name=account_holder_name,
          users_account_branch_name=branch_name,
          users_account_type="savings",
          users_account_status_confirm=True
      )
  
      anvil.alert("Bank details saved successfully.", title="", large=True)
      open_form('customer.wallet', user=self.user)
  


    def link_2_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.walletbalance",user=self.user)

    def link_3_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.transactions",user=self.user)

    def link_4_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.transfer",user=self.user)

    def link_7_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.Viewprofile",user=self.user)

    def link_1_click(self, **event_args):
      if self.card_3000.visible:
          self.card_3000.visible = False
          self.link_1.text = 'Open'
          self.link_1.icon = 'fa:angle-double-down'
      else:
          self.card_3000.visible = True
          self.link_1.text = 'Close'
          self.link_1.icon = 'fa:angle-double-up'


    def link_13_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("Home")

    def link_8_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.wallet",user=self.user)

    def link_10_click(self, **event_args):
      open_form('customer.deposit',user=self.user)

    def link_5_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.withdraw',user=self.user)

    def link_6_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.auto_topup',user=self.user)


    def link_1_copy_copyclick(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer',user=self.user)


    def link_1_dashboard_click(self, **event_args):
      open_form("customer",user  = self.user)

    def link_8_copy_2_click(self, **event_args):
      open_form("customer.settings",user = self.user)

    def link_8_copy_3_click(self, **event_args):
       open_form("help",user = self.user)
      





