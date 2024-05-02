from ._anvil_designer import loginTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime 

class login(loginTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.card_3.visible = False
      
    def text_box_3_pressed_enter(self, **event_args):
        self.primary_color_1_click()

    def primary_color_1_click(self, **event_args):
        # Get the login input (username, phone number, or email)
        login_input = self.text_box_1.text.strip()
        # Get the password
        password = self.text_box_3.text.strip()

        # Check if either login input or password is not entered
        if not login_input or not password:
            alert("Please enter both username and password.")
            return

        # Get the user based on login input
        user = anvil.server.call('get_user_for_login', login_input)

        # Check if user exists and password matches
        if user is not None and user['password'] == password:
            # Check if the user is banned
            if user['banned'] is not None and user['banned']:
                open_form('LOGIN.banned_form')
                return

            # Check if the user is on hold/freeze
            if user['hold'] is not None and user['hold']:
                alert("Your account is on hold/freeze. Please try again later.", title="Account On Hold")
                return

            user_type = user['usertype']

            if user_type == 'admin':
                open_form('admin', user=user)
            elif user_type == 'customer':
                open_form('customer', user=user)
        elif user is not None and user['password'] != password:
            self.card_3.visible = True
            self.label_4.visible = True
            self.label_5.visible = False
            self.label_6.visible = False
            self.text_box_3.text = ''
            self.text_box_3.focus()
        else:
            # Alert if either username or password is incorrect
            alert("Incorrect username or password. Please try again.")
            self.text_box_3.text = ''
            self.text_box_3.focus()

    def link_2_click(self, **event_args):
      open_form('signup')

