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
    
    def __init__(self, user=None, user_data=None, **properties):
        # Initialize the base class
        self.init_components(**properties)
        self.user = user
        self.user_data = user_data
        
        # Debugging statements
        if self.user is not None:
            print("DEBUG: User is present")
            self.name = self.user['users_email']
            print(f"DEBUG: User's email: {self.name}")
        else:
            print("DEBUG: User is None")
        
        if self.user_data is not None:
            print(f"DEBUG: User data received: {self.user_data['users_username']}")
        else:
            print("DEBUG: User data is None")
    
    def primary_color_1_click(self, **event_args):
        phone_number = self.user_data['users_phone']
        new_limit = float(self.text_box_1.text)
        limit_type = self.drop_down_2.selected_value

        if new_limit == None or new_limit <=0:
          return 
        # Determine which limit to update based on the selection
        if limit_type == 'Daily':
            field_to_update = 'users_daily_limit'
            text='users daily limit'
        elif limit_type == 'Monthly':
            field_to_update = 'users_user_limit'
            text='users monthly limit'
        else:
            anvil.alert("Invalid limit type selected")
            return

        # Call the server function to update the user's limit
        setter = anvil.server.call('update_user_limit', phone_number, field_to_update, new_limit)
        
        # Log changes to 'actions' table
        changes_made = [f"{text} updated to {new_limit} by admin"]
        if self.user is not None:
            self.log_action(phone_number, changes_made, self.name)
        else:
            print("DEBUG: self.user is None - not logging action")
    
    def log_action(self, phone_number, changes, email):
        # Retrieve user by phone number
        user = app_tables.wallet_users.get(users_phone=phone_number)
        last_login = None
        
        if user and user['users_last_login']:
            last_login = user['users_last_login']
        
        # Log actions to 'actions' table if changes were made
        if changes:
            print("DEBUG: Changes to be logged")
            current_datetime = datetime.now()
            app_tables.wallet_admins_actions.add_row(
                admins_actions_name=self.user['users_username'],
                admins_actions_username=user['users_username'],
                # last_login=last_login,
                admins_actions=", ".join(changes),
                admins_actions_date=current_datetime,
                # admin_email= email
            )

    def link_5_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.account_management', user=self.user)
