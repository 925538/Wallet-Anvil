from ._anvil_designer import ItemTemplate6Template
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate6(ItemTemplate6Template):
  user=None
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #test = self.user['users_username']
    print('hi admin test')
    

    # Set data bindings for label_3
    self.label_3.text = self.get_status_text()
    self.label_3.foreground = self.get_status_color()
    self.check_profile_pic()
  
  def check_profile_pic(self):
        # print(self.user)
        # print(self.user['users_email'],type(self.user['users_email']))
        # user_data = app_tables.wallet_users.get(users_email=str(self.user['users_email'])) #changed
        if self.item['user_profile_photo'] is not None:
            self.image_1.source =self.item['user_profile_photo']
        else:
          print('user image none')
  
  def get_status_text(self):
        if self.item['user_hold']:
            return "Hold"
        return "Inactive" if self.item['user_inactive'] else "Active"
  
  def get_status_color(self):
    # Check for hold status first
    if self.item['user_hold']:
        return "red"
    # Check for inactive status next
    elif self.item['user_inactive']:
        return "red"
    # If neither hold nor inactive, return green for active
    else:
        return "green"


  def button_1_click(self, **event_args):
    # Access the data for the selected user
    selected_user = self.item  # Assuming you have set the 'item' property of the repeating panel to the user row
    
    # Extract the phone number and username
    phone_number = selected_user['user_phone_number']
    print(phone_number)
    fullname = selected_user['user_fullname']
    print(fullname)
    
    # Open the admin_view form and pass the phone number and admin username
    open_form('admin.admin_view_user_details', user=self.user, phone_number=phone_number, fullname=fullname)

  # def button_1_click(self, **event_args):
  #   # Access the data for the selected user
  #   selected_user = self.item  # Assuming you have set the 'item' property of the repeating panel to the user row
    
  #   # Extract the phone number from the second text box
  #   phone_number = selected_user['users_phone']  # Assuming 'phone_number' is the key for the phone number in your data
    
  #   # Open the admin_view form and pass the phone number
  #   open_form('admin.admin_view_user_details',user =self.user, phone_number=phone_number)

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.button_1.visible=True
    
    
