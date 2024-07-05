from ._anvil_designer import ItemTemplate7Template
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate7(ItemTemplate7Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Assign the properties to the labels and text area.
    self.label_1.text = self.item['users_service_username']
    self.label_2.text = self.item['users_service_phone']
    self.label_3.text = self.item['users_service_email']
    self.text_area_1.text = self.item['users_service_query']
    
    # Fetch the profile photo based on the phone number.
    self.fetch_profile_photo(self.item['users_service_phone'])
    
    # Set the button text and color based on the 'users_update' field.
    self.update_button_text()

  def fetch_profile_photo(self, phone_number):
    print(f"Fetching profile photo for phone number: {phone_number}")

    # Query the wallet_users table for the user with the given phone number.
    user_row = app_tables.wallet_users.get(users_phone=phone_number)
    
    if user_row:
      print(f"User row found: {user_row}")
      try:
        profile_photo = user_row['users_profile_pic']
        if profile_photo:
          print("Profile photo column found.")
          # If a user is found and has a profile photo, display it.
          self.image_1.source = profile_photo
          print(f"Profile photo set: {profile_photo}")
        else:
          # Log that the profile picture column is empty.
          self.image_1.source = 'path/to/default/image.png'  # Optional: Add a default image path here
          print("Profile photo column is empty.")
      except KeyError:
        # Log that the profile picture column is missing.
        self.image_1.source = 'path/to/default/image.png'  # Optional: Add a default image path here
        print("Profile photo column missing.")
    else:
      # Log that no user was found for the provided phone number.
      self.image_1.source = 'path/to/default/image.png'  # Optional: Add a default image path here
      print("No user found for the provided phone number.")

    # Optionally, you can also provide user feedback in the UI.
    if self.image_1.source == 'path/to/default/image.png':
      Notification("User data is incomplete or missing", title="Error", style="error").show()
  
  def update_button_text(self):
    if self.item['users_update']:
      self.button_1.text = "Solved"
      self.button_1.foreground = "green"
    else:
      self.button_1.text = "Unsolved"
      self.button_1.foreground = "red"

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
