from ._anvil_designer import add_currencyTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class add_currency(add_currencyTemplate):
  def __init__(self, user=None, **properties):
    self.user = user
    self.init_components(**properties)
    
    self.flow_panel_1.visible = False
    self.refresh_currency_data()
    # self.image_1.source = self.item['icon_path']
    

  def refresh_currency_data(self, country_filter=None):
    try:
      # Fetch currency data from server
      currency_data = anvil.server.call('get_currency_data')
      print("Fetched currency data:", currency_data)  # Debugging
      
      # Ensure the data is a list of dictionaries
      if isinstance(currency_data, list) and all(isinstance(item, dict) for item in currency_data):
        if country_filter:
          # Apply the filter if provided
          self.country_type_filter = [currency for currency in currency_data
                                      if country_filter.lower() in currency['country'].lower()]
        else:
          self.country_type_filter = currency_data
        
        print("Filtered country data:", self.country_type_filter)  # Debugging
        
        # Update repeating panel with filtered data
        # self.repeating_panel_1.items = self.country_type_filter
        self.repeating_panel_1.items = [
                {
                    "country": item['country'],
                    "code": item['code'],
                    "icon": item['icon']
                }
                for item in self.country_type_filter
            ]
        # Debugging: Check if items are set correctly
        print("Repeating panel items set.")
      else:
        print("Error: Currency data is not in the expected format.")
    
    except Exception as e:
      print(f"An error occurred while fetching or filtering data: {e}")
    # if country_filter:
    #   self.country_type_filter = [user for user in app_tables.wallet_admins_add_currency.search()
    #                               if user['admins_add_currency_country'].lower().startswith(country_filter.lower())]
    # else:
    #   self.country_type_filter = [user for user in app_tables.wallet_admins_add_currency.search()]
    # self.repeating_panel_1.items = self.country_type_filter

  def button_1_click(self, **event_args):
    country_filter = self.textbox_search.text
    self.refresh_currency_data(country_filter)

  def textbox_search_pressed_enter(self, **event_args):
    country_filter = self.textbox_search.text
    self.refresh_currency_data(country_filter)

  def button_2_click(self, **event_args):
    self.flow_panel_1.visible = True

  def button_3_click(self, **event_args):
        country_name = self.text_box_1.text.strip()
        currency_code = self.text_box_2.text.strip()
        currency_icon_media = self.file_loader_1.file
        
        if country_name and currency_code:
            country_name = country_name.capitalize()
            if len(currency_code) == 3 and currency_code.isalpha():
                success, message = anvil.server.call('add_currency', country_name, currency_code.upper(),currency_icon_media)
                
                if success:
                    self.refresh_currency_data()
                    self.text_box_1.text = ''
                    self.text_box_2.text = ''
                    self.file_loader_1.clear()  # Clear the file loader after submission
                    self.flow_panel_1.visible = False
                    alert(message)
                else:
                    alert(message)
            else:
                alert('Invalid currency code')
  

    # country_name = self.text_box_1.text.strip()
    # currency_code = self.text_box_2.text.strip()
    
    # if country_name and currency_code:
    #     country_name = country_name.capitalize()
    #     print(country_name)
        
    #     if len(currency_code) == 3 and currency_code.isalpha():
    #         existing_entry = app_tables.wallet_admins_add_currency.search(
    #             admins_add_currency_country=country_name,
    #             admins_add_currency_code=currency_code.upper()
    #         )
            
    #         if len(existing_entry) == 0:
    #             # Check if an image has been uploaded
    #             if self.file_loader_1.file:
    #                 # Save the uploaded image to the currency_icon column
    #                 new_currency = app_tables.wallet_admins_add_currency.add_row(
    #                     admins_add_currency_country=country_name,
    #                     admins_add_currency_code=currency_code.upper(),
    #                     admins_add_currency_icon=self.file_loader_1.file
    #                 )
    #             else:
    #                 # If no image is uploaded, set currency_icon to None
    #                 new_currency = app_tables.wallet_admins_add_currency.add_row(
    #                     admins_add_currency_country=country_name,
    #                     admins_add_currency_code=currency_code.upper(),
    #                     admins_add_currency_icon=None
    #                 )
                
    #             self.refresh_currency_data()
    #             self.text_box_1.text = ''
    #             self.text_box_2.text = ''
    #             self.flow_panel_1.visible = False
    #             alert('Currency added successfully')
    #         else:
    #             alert('Country with this currency code already exists')
    #     else:
    #         alert('Invalid currency code')

  def link_8_copy_click(self, **event_args):
    open_form('admin', user=self.user)

  def link_8_click(self, **event_args):
    open_form('admin', user=self.user)

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.report_analysis', user=self.user)

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.account_management', user=self.user)

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.transaction_monitoring', user=self.user)

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.admin_add_user', user=self.user)

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.audit_trail', user=self.user)

  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.user_support', user=self.user)

  def link_6_copy_2_click(self, **event_args):
    if self.user['users_usertype'] == 'super admin':
          # Open the admin creation form
          open_form("admin.create_admin", user=self.user)
    else:
          # Show an alert if the user is not a super admin
         alert("You're not a super admin. Only super admins can perform this action.")

  def link_6_copy_3_click(self, **event_args):
    open_form("admin.add_currency", user=self.user)

  def link_6_copy_4_click(self, **event_args):
    open_form("admin.add_bank_account", user=self.user)

 
