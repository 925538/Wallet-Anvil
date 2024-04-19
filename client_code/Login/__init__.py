from ._anvil_designer import LoginTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime 

class Login(LoginTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
    def text_box_2_pressed_enter(self, **event_args):
        self.button_1_click()

    def button_1_click(self, **event_args):
        # Get the login input (username, phone number, or email)
        login_input = self.text_box_1.text.strip()
      
        # Get the password
        password = self.text_box_2.text.strip()

        # Get the user based on login input
        user = anvil.server.call('get_user_for_login', login_input)

        # Check if user exists and password matches
        if user is not None and user['password'] == password:
            # Check if the user is banned
            if user['banned'] is not None and user['banned']:
                # Display a popup message informing the user they are banned
                anvil.alert("Sorry, you are banned from accessing this service.your amount will credit to your primary account")
                return
              
            user_type = user['usertype']

            if user_type == 'admin':
                open_form('admin', user=user)
            elif user_type == 'customer':
                open_form('customer', user=user)
        else:
            self.label_9.text = "Invalid login credentials"
            self.text_box_1.text = ''
            self.text_box_1.focus()
            self.text_box_2.text = ''
            self.text_box_2.focus()
          
    def button_2_click(self, **event_args):
        open_form('Signup')

    def button_3_click(self, **event_args):
        open_form('Home')

    def link_11_copy_click(self, **event_args):
        open_form('Home')

    def link_1_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('forgot_password')

    

    




