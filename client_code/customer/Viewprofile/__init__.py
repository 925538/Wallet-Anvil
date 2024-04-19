from ._anvil_designer import ViewprofileTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import alert, open_form
import re

class Viewprofile(ViewprofileTemplate):
    def __init__(self, user=None, **properties):
        self.init_components(**properties)
        self.user = user
        self.edit_mode = False  # Initial edit mode is set to False
        if user:
            self.label_8.text = f"Welcome to Green Gate Financial, {user['username']}"
            self.display_user_profile(user)  # Display user profile on form load

    def toggle_edit_mode_components(self):
        # Show/hide text boxes based on edit mode
        for i in range(1, 5):
            textbox = getattr(self, f'text_box_{i}')
            textbox.visible = self.edit_mode

        self.button_1.text = "Edit Profile" if not self.edit_mode else "Save Changes"

    def display_user_profile(self, user):
        # Fetch and display data for the logged-in user
        # You can customize this based on your table structure
        user_data = app_tables.wallet_users.get(phone=user['phone'])
        self.text_box_1.text = f"{user_data['email']}"
        self.text_box_2.text = f"{user_data['phone']}"
        self.text_box_3.text = f"{user_data['pan']}"
        self.text_box_4.text = f"{user_data['aadhar']}"



    def button_1_click(self, **event_args):
        if not self.edit_mode:
            # Toggle to edit mode
            self.edit_mode = True
            self.toggle_edit_mode_components()
        else:
            # Save changes and toggle back to view mode
            user_data = app_tables.wallet_users.get(phone=self.user['phone'])
            count=0
            
            phone_number= self.text_box_2.text
            if self.validate_phone_number(phone_number):
                  count=count+1
            aadhar_card = self.text_box_4.text
            if len(str(aadhar_card)) == 12:
                  count=count+1 
            converted_text = self.text_box_3.text 
            if self.is_pan_card_detail(converted_text):
                  count=count+1
                   
            if user_data is not None and count==3:
              user_data['email'] = self.text_box_1.text
              user_data['phone'] = self.text_box_2.text
              user_data['aadhar'] = self.text_box_4.text
              user_data['pan']= self.text_box_3.text
                
              alert("User details updated successfully.", title="Success")
            else:
              alert("Please check the entered details to proceed")

            # Toggle back to view mode
            self.edit_mode = False
            self.display_user_profile(self.user)
            self.button_1.text = "Edit Profile" if not self.edit_mode else "Save Changes"
      
    def validate_phone_number(self, phone_number):
      pattern = r'^[6-9]\d{9}$'
      if re.match(pattern, str(phone_number)):
        return True  
      else:
        return False    # Remove leading/trailing whitespace
        
    def is_pan_card_detail(self, text):
        if (
            len(text) == 10 and
            text[:5].isalpha() and
            text[5:9].isdigit() and
            text[9].isalpha()
        ):
          return True
        else:
          return False

    def text_box_3_change(self, **event_args):
      current_text = self.text_box_3.text
      converted_text = current_text.upper()
      self.text_box_3.text = converted_text

    def text_box_2_pressed_enter(self, **event_args):
      phone_number = self.text_box_2.text.strip()

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

    def link_13_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("Home")

    def link_1_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer",user=self.user)

    # def link_8_click(self, **event_args):
    #   """This method is called when the link is clicked"""
    #   open_form("service",user=self.user)

    def button_2_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('Reset_password',user=self.user)







