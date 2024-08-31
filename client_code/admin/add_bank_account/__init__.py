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
    # Call the server function to get the list of bank names and icons
    bank_data = anvil.server.call('get_bank_names')

    # If a filter is provided, filter the bank data
    if bank_filter:
        bank_data = [bank for bank in bank_data if bank_filter.lower() in bank['bank_name'].lower()]

    # Set the items for the RepeatingPanel to display the bank names and icons
    self.repeating_panel_1.items = bank_data

    # Assign the bank data to the repeating panel or any other component

  def button_1_click(self, **event_args):
      bank_filter = self.textbox_search.text
      self.refresh_users(bank_filter)

  def textbox_search_pressed_enter(self, **event_args):
      bank_filter = self.textbox_search.text
      self.refresh_users(bank_filter)

  def button_2_click(self, **event_args):
      self.flow_panel_1.visible = True

  def button_3_click(self, **event_args):
    # Retrieve the bank name from the text box
    bank_name = self.text_box_1.text.strip()
    
    if bank_name:
        bank_name = bank_name.capitalize()

        # Get the bank icon from the file loader, if provided
        bank_icon_media = self.file_loader_1.file if self.file_loader_1.file else None
        
        # Call the server function to store the bank data
        result = anvil.server.call('fetch_and_store_bank_data', bank_name, bank_icon_media)
        
        # Refresh the UI and show the message returned by the server
        self.refresh_users()  # Assuming this function updates your UI
        self.text_box_1.text = ''
        self.file_loader_1.clear()
        self.flow_panel_1.visible = False
        alert(result)
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
    if self.user['user_type'] == 'super admin':
          # Open the admin creation form
          open_form("admin.create_admin", user=self.user)
    else:
          # Show an alert if the user is not a super admin
         alert("You're not a super admin. Only super admins can perform this action.")

  def link_6_copy_4_click(self, **event_args):
    open_form("admin.add_bank_account",user = self.user)

  