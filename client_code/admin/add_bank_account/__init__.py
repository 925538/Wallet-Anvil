from ._anvil_designer import add_bank_accountTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class add_bank_account(add_bank_accountTemplate):
  def __init__(self,user = None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = user
    self.flow_panel_1.visible = False
    self.refresh_users()

    # Any code you write here will run before the form opens.

  def refresh_users(self, bank_filter=None):
    if bank_filter:
      self.bank_type_filter = [user for user in app_tables.wallet_admins_add_bank.search()
                                  if user['admins_add_bank_names'].lower().startswith(bank_filter.lower())]
    else:
      self.bank_type_filter = [user for user in app_tables.wallet_admins_add_bank.search()]
    self.repeating_panel_1.items = self.bank_type_filter

  def button_1_click(self, **event_args):
    bank_filter = self.textbox_search.text
    self.refresh_users(bank_filter)

  def textbox_search_pressed_enter(self, **event_args):
    bank_filter = self.textbox_search.text
    self.refresh_users(bank_filter)

  def button_2_click(self,add_bank=None, **event_args):
    self.flow_panel_1.visible = True

  def button_3_click(self, **event_args):
    bank_name = self.text_box_1.text.strip()
    
    
    if bank_name:
        bank_name = bank_name.capitalize()
        print(bank_name)
        existing_bank = app_tables.wallet_admins_add_bank.search(admins_add_bank_names=bank_name) 
        
        if len(existing_bank) == 0:
            # Check if an image has been uploaded
            if self.file_loader_1.file:
                # Save the uploaded image to the bank_icon column
                new_currency = app_tables.wallet_admins_add_bank.add_row(
                    admins_add_bank_names=bank_name,
                    admins_add_bank_icons=self.file_loader_1.file
                )
            else:
                # If no image is uploaded, set bank_icon to None
                new_currency = app_tables.wallet_admins_add_bank.add_row(
                    admins_add_bank_names=bank_name,
                    admins_add_bank_icons=None
                )
            
            self.refresh_users()
            self.text_box_1.text = ''
            self.file_loader_1.clear()
            self.flow_panel_1.visible = False
                
            alert('Bank name added successfully')
        else:
            alert('Bank already exists')
    else:
        alert('Incorrect bank name')

  def link_8_copy_click(self, **event_args):
    open_form('admin', user=self.user)

  def link_8_click(self, **event_args):
    open_form('admin',user = self.user)

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.report_analysis',user = self.user)

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.account_management',user = self.user)

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.transaction_monitoring',user = self.user)

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.audit_trail',user = self.user)

  def link_10_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.add_currency',user = self.user)

  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.user_support',user = self.user)

  def link_6_copy_2_click(self, **event_args):
    open_form("admin.admin_add_user",user = self.user)

  def link_6_copy_3_click(self, **event_args):
    if self.user['users_usertype'] == 'super admin':
          # Open the admin creation form
          open_form("admin.create_admin", user=self.user)
    else:
          # Show an alert if the user is not a super admin
         alert("You're not a super admin. Only super admins can perform this action.")

  def link_6_copy_4_click(self, **event_args):
    open_form("admin.add_bank_account",user = self.user)

  