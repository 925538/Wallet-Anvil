from ._anvil_designer import ItemTemplate3Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import base64
from datetime import datetime
class ItemTemplate3(ItemTemplate3Template):
  def __init__(self,  **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    existing_img = self.item['profile_pic']
    if existing_img != None:
      decoded = base64.b64decode(existing_img)
    # profile_pic_media = BytesMedia(existing_img)
      base_media = anvil.BlobMedia("image/png",decoded)
      self.image_1.source = base_media
    else:
      self.image_1.source = '_/theme/account.png'
    self.check_status()

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    # Access the data for the selected user
    selected_user = self.item  # Assuming you have set the 'item' property of the repeating panel to the user row
    
    # Extract the phone number from the second text box
    phone_number = selected_user['phone']  # Assuming 'phone_number' is the key for the phone number in your data
    
    # Open the admin_view form and pass the phone number
    open_form('admin.admin_view', phone_number=phone_number)

  def check_status(self):
      now = datetime.now(anvil.tz.tzlocal())
  # Parse the 'last_login' date string into a datetime object
      last_login = datetime.strptime(str(self.item['last_login']), '%Y-%m-%d %H:%M:%S.%f%z') 
      # Calculate the difference in days between the current date and the last login date
      diff_days = (now - last_login).days
      if diff_days > 90:
        self.text_box_4.text = 'Inactive'
        self.text_box_4.foreground = '#ff2800'
      else:
        self.text_box_4.text = 'Active'
        self.text_box_4.foreground = '#00fa9a'
