from ._anvil_designer import set_limitTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class set_limit(set_limitTemplate):

    def __init__(self, user=None, **properties):
        # Initialize the base class
        self.init_components(**properties)
        self.user = user
        
        # Debugging statements
        if self.user is not None:
            print("DEBUG: User is present")
            self.phone_number = self.user['users_phone']  # Assuming 'users_phone' is the key for phone number in the user object
            print(f"DEBUG: User's phone number: {self.phone_number}")
        else:
            print("DEBUG: User is None")

    def primary_color_1_click(self, **event_args):
        new_limit = self._get_valid_limit()
        limit_type = self.drop_down_2.selected_value

        if new_limit is None or new_limit <=0:
            return  # Early return if limit is invalid

        # Determine which limit to update based on the selection
        field_to_update = self._get_field_to_update(limit_type)
        if field_to_update is None:
            return  # Early return if limit type is invalid

        try:
            # Call the server function to update the user's limit
            setter = anvil.server.call('update_user_limit_by_phone', self.phone_number, field_to_update, new_limit)
            anvil.alert(f"{field_to_update} updated to {new_limit} for user with phone {self.phone_number}")
        except Exception as e:
            anvil.alert(f"An error occurred: {str(e)}")

    def _get_valid_limit(self):
        try:
            return float(self.text_box_1.text)
        except ValueError:
            anvil.alert("Please enter a valid number for the limit.")
            return None

    def _get_field_to_update(self, limit_type):
        if limit_type == 'Daily':
            return 'users_daily_limit'
        elif limit_type == 'Monthly':
            return 'users_user_limit'
        else:
            anvil.alert("Invalid limit type selected")
            return None

    def link_8_copy_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin', user=self.user)

    def link_10_copy_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.user_support', user=self.user)

    def button_8_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('Login')

    def button_3_click(self, **event_args):
        open_form('admin.account_management', user=self.user)

    def link_1_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.report_analysis', user=self.user)

    def link_2_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.account_management', user=self.user)

    def link_7_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.transaction_monitoring', user=self.user)

    def link_6_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.admin_add_user', user=self.user)

    def link_5_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.audit_trail', user=self.user)

    def link_4_click(self, **event_args):
        """This method is called when the link is clicked"""
        serves_data = app_tables.services.search()
        user_support_form = open_form('admin.user_support', serves_data=serves_data, user=self.user)

    def link_3_click(self, **event_args):
        """This method is called when the link is clicked"""
        show_users_form = open_form('admin.show_users', user=self.user)

    def drop_down_2_show(self, **event_args):
        """This method is called when the DropDown is shown on the screen"""
        options_list = ['Daily', 'Monthly']
        self.drop_down_2.items = options_list

    def primary_color_2_click(self, user=None, **event_args):
        """This method is called when the button is clicked"""
        open_form('customer.walletbalance', user=self.user)

    def text_box_1_pressed_enter(self, **event_args):
      """This method is called when the user presses Enter in this text box"""
      pass

    def text_box_1_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        user_input = self.text_box_1.text
        print("Raw input:", user_input)
        
        allowed_characters = "0123456789."
    
        # Filter out any invalid characters and allow only one decimal point
        filtered_text = ''
        decimal_point_count = 0
        
        for char in user_input:
          if char in allowed_characters:
            if char == '.':
              decimal_point_count += 1
              if decimal_point_count > 1:
                continue
            filtered_text += char
    
        # Allow empty string and string with just a decimal point
        if filtered_text == '' or filtered_text == '.':
          self.text_box_1.text = filtered_text
          return
    
        try:
          processed_value = self.process_input(filtered_text)
          self.text_box_1.text = processed_value
        except ValueError:
          self.text_box_1.text = filtered_text
    
    def process_input(self, user_input):
      # Check if the input ends with a decimal point
      if user_input.endswith('.'):
        return user_input
      
      value = float(user_input)
      
      if value.is_integer():
        # If it's an integer, format without decimals
        formatted_value = '{:.0f}'.format(value)
      else:
        # If it's a float, format with significant digits
        formatted_value = '{:.15g}'.format(value)
  
      return formatted_value
