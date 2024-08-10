from ._anvil_designer import admin_view_user_detailsTemplate
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
import re
import base64

class admin_view_user_details(admin_view_user_detailsTemplate):
    def __init__(self, user_data=None, phone_number=None, user=None, **properties):
        self.admin = user
        self.phone_number = phone_number
        self.init_components(**properties)
        # self.user = user
        if self.admin is not None:
            self.label_6566.text = self.admin['users_username']
            # if 'users_username' in self.user:
            #     self.label_6566.text = self.user['users_username']
            # else:
            #     print("users_username not found in user object")
        
        # self.check_profile_pic()
        self.populate_balances()
        self.edit_mode = False
        self.user = user_data
        # if self.user is not None:
        #     self.label_6566.text = self.user['users_username']

        if phone_number is not None:
            self.label_401.text = phone_number

            user_data = app_tables.wallet_users.get(users_phone=phone_number)
            if user_data is not None:
                self.label_100.text = user_data['users_username']
                self.label_201.text = user_data['users_email']
                self.label_501.text = user_data['users_aadhar']
                self.label_601.text = user_data['users_pan']
                self.label_401.text = user_data['users_phone']
                self.label_801.text = user_data['users_address']
                self.label_701.text = user_data['users_address']
                
                # Set the status label
                self.set_status_label(user_data)

            else:
                self.label_100.text = ""
                self.label_201.text = ""
                self.label_401.text = ""
                self.label_501.text = ""
                self.label_601.text = ""
                self.label_701.text = ""
                self.label_801.text = ""
                self.label_901.text = ""

            self.set_button_text()
        self.check_profile_pic()

    def check_profile_pic(self):
          # print(self.user['users_email'],type(self.user['users_email']))
          user_data = app_tables.wallet_users.get(users_phone = self.phone_number) #changed
          if user_data:
            existing_img = user_data['users_profile_pic']
            if existing_img != None:
              self.image_1.source = existing_img
            else: 
              print('no pic')
          else:
            print('none')

    def set_status_label(self, user_data):
      if user_data:
          if user_data['users_banned']:
              self.label_901.text = "Hold"
              self.label_901.foreground = "red"
          
          elif user_data['users_inactive']:
              self.label_901.text = "Inactive"
              self.label_901.foreground = "red"
          else:
              self.label_901.text = "Active   "
              self.label_901.foreground = "green"
      else:
          self.label_901.text = "No Data"
          self.label_901.foreground = "gray"

  





    def populate_balances(self):
      try:
          # Retrieve balances for the current user based on phone number
          user_phone = self.phone_number
          user_balances = app_tables.wallet_users_balance.search(users_balance_phone=user_phone)
  
          # Print the retrieved data for debugging
          print("Retrieved balances:", list(user_balances))
  
          # Check if no balances are found
          if not list(user_balances):
              self.label_1000.text = "User doesn't have any balance"
              return
  
          # Initialize index for card and components
          card_index = 1
          label_index = 1  # Start from label_1
          country_label_index = 50  # Start from label_50 for country
          image_index = 1
  
          # Iterate over user balances and update card components
          for balance in user_balances:
              currency_type = balance['users_balance_currency_type']
              balance_amount = balance['users_balance']
  
              # Lookup the currency icon, symbol, and country in the wallet_currency table
              currency_record = app_tables.wallet_admins_add_currency.get(admins_add_currency_code=currency_type)
              currency_icon = currency_record['admins_add_currency_icon'] if currency_record else None
              country = currency_record['admins_add_currency_country'] if currency_record else None
  
              # Get card and components for the current index
              card = getattr(self, f'card_{card_index}', None)
              label_curr_type = getattr(self, f'label_{label_index}', None)
              label_balance = getattr(self, f'label_{label_index + 1}', None)
              label_country = getattr(self, f'label_{country_label_index}', None)
              image_icon = getattr(self, f'image_icon_{image_index}', None)
  
              # Debugging output for components
              print(f"Card {card_index}: {card}")
              print(f"Label Curr Type {label_index}: {label_curr_type}")
              print(f"Label Balance {label_index + 1}: {label_balance}")
              print(f"Label Country {country_label_index}: {label_country}")
              print(f"Image Icon {image_index}: {image_icon}")
  
              if card and label_curr_type and label_balance and image_icon and label_country:
                  # Update card components with balance data
                  label_curr_type.text = currency_type
                  label_balance.text = f"{balance_amount:.2f}"  # Format balance amount to 2 decimal places
                  label_country.text = country
                  label_balance.icon = f"fa:{currency_type.lower()}"
  
                  # Ensure image_icon exists and update if it does
                  if image_icon:
                      image_icon.source = currency_icon
  
                  # Set card visibility to True
                  card.visible = True
  
                  # Increment indices for the next iteration
                  card_index += 1
                  label_index += 2
                  country_label_index += 1
                  image_index += 1
  
          # Set visibility of remaining cards to False if no data
          while card_index <= 12:
              card = getattr(self, f'card_{card_index}', None)
              if card:
                  card.visible = False
              card_index += 1
  
      except Exception as e:
          # Print any exception that occurs during the process
          print("Error occurred during population of balances:", e)
  


    # def fetch_and_display_balance(self, currency_type):
    #     if not currency_type:
    #         # If the text box is empty, display all balances
    #         self.populate_balances()
    #         return

    #     try:
    #         # Convert the currency type to uppercase
    #         currency_type = currency_type.upper()

    #         # Retrieve balance for the entered currency type
    #         user_phone = self.phone_number
    #         balance_record = app_tables.wallet_users_balance.get(phone=user_phone, currency_type=currency_type)

    #         if balance_record:
    #             balance_amount = balance_record['balance']

    #             # Lookup the currency icon, symbol, and country in the wallet_currency table
    #             currency_record = app_tables.wallet_currency.get(currency_code=currency_type)
    #             currency_icon = currency_record['currency_icon'] if currency_record else None
    #             country = currency_record['country'] if currency_record else None

    #             # Update card_1 components with balance data
    #             self.label_1.text = currency_type
    #             self.label_2.text = f"{balance_amount}"
    #             self.label_2.icon = f"fa:{currency_type.lower()}"
    #             self.label_50.text = country
    #             self.image_icon_1.source = currency_icon

    #             # Set card_1 visibility to True
    #             self.card_1.visible = True
    #         else:
    #             # If no balance found, hide card_1
    #             self.card_1.visible = False

    #         # Hide all other cards
    #         for i in range(2, 13):
    #             card = getattr(self, f'card_{i}', None)
    #             if card:
    #                 card.visible = False

    #     except Exception as e:
    #         # Print any exception that occurs during the process
    #         print("Error occurred during fetching and displaying balance:", e)

    def button_5_click(self, **event_args):
        username = self.label_100.text
        user_to_update = app_tables.wallet_users.get(users_phone=self.phone_number)

        if user_to_update is not None:
            # Check the current state of 'hold' column
            current_state = user_to_update['users_hold']

            # If 'hold' is None or 'true', user is considered frozen, otherwise unfrozen
            new_state = not current_state

            # Update the 'hold' column in the 'users' table
            user_to_update.update(users_hold=new_state if new_state else None)
            
            # Update the 'banned' column based on freeze/unfreeze action
            user_to_update.update(users_banned=True if new_state else None)

            # Update button text based on the new state
            self.set_button_text()
            self.set_status_label(user_to_update)

            # Display alert based on the action
            alert_message = "User is frozen." if new_state else "User is unfrozen."
            alert(alert_message, title="Status")

            # Log the action
            self.log_action(username, [alert_message])
            print("Button 5 Clicked and action logged")  # Debug statement

    def set_button_text(self):
        username = self.label_100.text
        user_to_update = app_tables.wallet_users.get(users_phone=self.phone_number)

        # Get the current hold state from the database
        current_state = user_to_update['users_hold'] if user_to_update else None


        # Set the button text based on the current hold state
        self.button_5.text = "Unfreeze" if current_state else "Freeze"

    def button_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        # Check if the user has balances
        if not self.has_balances():
            # Get the phone number from the form
            phone_number = self.phone_number
            
            # Retrieve the user based on phone number
            user_to_delete = app_tables.wallet_users.get(users_phone=phone_number)
            
            if user_to_delete is not None:
                username = user_to_delete['users_username']  # Get the username before deleting the row
                user_to_delete.delete()
                
                # Log the deletion action
                self.log_action(username,["User deleted"])
                
                # Open the admin.account_management form
                open_form('admin.account_management', user=self.admin)
                
                # Optionally, display an alert to inform the user
                alert("User deleted successfully.", title="Status")
        else:
            # If the user has balances, inform the admin that they cannot delete the user
            alert("User has balances. Please clear the balances before deleting.", title="Status")

    def log_action(self, username, actions):
    # Log the action to the app_tables.wallet_admins_actions table
      timestamp = datetime.now()
      action_log = ", ".join(actions)
  
      # Retrieve user data based on phone number
      user_data = app_tables.wallet_users.get(users_phone=self.phone_number)
  
      if user_data:
          # Insert the log entry into the table using user's phone number and username
          app_tables.wallet_admins_actions.add_row(
              admins_actions_name=self.admin['users_username'],
              admins_actions_username=username,  # Use provided username
              admins_actions_phone=user_data['users_phone'],  # Use user's phone number
              admins_actions_date=timestamp,
              admins_actions=action_log
          )
      else:
          print(f"User with phone number {self.phone_number} not found.")  # Handle case where user data is not found

      # def check_profile_pic(self):
      #     phone_number = self.phone_number
      #     user_data = app_tables.wallet_users.get(users_phone=phone_number)
          
      #     if user_data and user_data['users_profile_pic']:
      #         self.image_1.source = user_data['users_profile_pic']
  
      # def upload_file_1_change(self, file, **event_args):
      #     if file is not None:
      #         phone_number = self.phone_number
      #         user_data = app_tables.wallet_users.get(users_phone=phone_number)
              
      #         if user_data is not None:
      #             # Store the uploaded file in the database
      #             user_data.update(users_profile_pic=file)
                  
      #             # Update the profile picture in the form
      #             self.image_1.source = file

    def button_6_click(self, **event_args):
        phone_number = self.phone_number
        user_data = app_tables.wallet_users.get(users_phone=phone_number)
        
        if user_data is not None:
            user_data.update(users_profile_pic=None)
            self.image_1.source = None

    def has_balances(self):
        user_phone = self.phone_number
        user_balances = app_tables.wallet_users_balance.search(users_balance_phone=user_phone)
        
        # Check if there are any balances for the user
        return bool(list(user_balances))

    def button_8_click(self, **event_args):
        self.edit_mode = not self.edit_mode

        if self.edit_mode:
            # Save current values for later comparison
            self.old_values = {
                'users_username': self.label_100.text,
                'users_email': self.label_201.text,
                'users_aadhar': self.label_501.text,
                'users_pan': self.label_601.text,
                'users_phone': self.label_401.text,
                'users_address': self.label_701.text,
                'users_country': self.label_801.text
            }

            self.text_box_1.text = self.label_100.text
            self.text_box_2.text = self.label_201.text
            self.text_box_3.text = self.label_501.text
            self.text_box_4.text = self.label_601.text
            self.text_box_5.text = self.label_401.text
            self.text_box_6.text = self.label_701.text
            self.text_box_7.text = self.label_801.text

            self.text_box_1.visible = True
            self.text_box_2.visible = True
            self.text_box_3.visible = True
            self.text_box_4.visible = True
            self.text_box_5.visible = True
            self.text_box_6.visible = True
            self.text_box_7.visible = True

            self.label_100.visible = False
            self.label_201.visible = False
            self.label_501.visible = False
            self.label_601.visible = False
            self.label_401.visible = False
            self.label_701.visible = False
            self.label_801.visible = False

            self.button_8.text = "Save"
        else:
            # Get new values from text boxes
            new_values = {
                'users_username': self.text_box_1.text,
                'users_email': self.text_box_2.text,
                'users_aadhar': self.text_box_3.text,
                'users_pan': self.text_box_4.text,
                'users_phone': self.text_box_5.text,
                'users_address': self.text_box_6.text,
                'users_country': self.text_box_7.text
            }

            # Check if there are any changes
            changes = {}
            for key, old_value in self.old_values.items():
                new_value = new_values[key]
                if old_value != new_value:
                    changes[key] = new_value

            if changes:
                user_data = app_tables.wallet_users.get(users_phone=self.phone_number)
                if user_data:
                    user_data.update(**changes)

                # Log the changes
                log_messages = [f"{key} changed from {self.old_values[key]} to {new_value}" for key, new_value in changes.items()]
                self.log_action(self.label_100.text, log_messages)

            self.label_100.text = self.text_box_1.text
            self.label_201.text = self.text_box_2.text
            self.label_501.text = self.text_box_3.text
            self.label_601.text = self.text_box_4.text
            self.label_401.text = self.text_box_5.text
            self.label_701.text = self.text_box_6.text
            self.label_801.text = self.text_box_7.text

            self.text_box_1.visible = False
            self.text_box_2.visible = False
            self.text_box_3.visible = False
            self.text_box_4.visible = False
            self.text_box_5.visible = False
            self.text_box_6.visible = False
            self.text_box_7.visible = False

            self.label_100.visible = True
            self.label_201.visible = True
            self.label_501.visible = True
            self.label_601.visible = True
            self.label_401.visible = True
            self.label_701.visible = True
            self.label_801.visible = True

            self.button_8.text = "Edit"

    def button_7_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.card_51.visible = True
      self.label_1000.visible = True

    def button_4_click(self, **event_args):
      """This method is called when the button is clicked"""
      username = self.label_100.text
      user_data = app_tables.wallet_users.get(users_phone=self.phone_number)  # Retrieve user_data
      
      # Log the action
      # self.log_action(username,self.label_100.text, ["User Setlimt changed"])
      
      # Open the admin.set_limit form with user and user_data
      open_form('admin.set_limit', user=self.admin, user_data=user_data)

    def link_2_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('admin.report_analysis',user=self.admin)

    def link_3_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('admin.account_management',user=self.admin)

    def link_5_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('admin.add_currency',user=self.admin)

    def link_6_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('admin.audit_trail',user=self.admin)

    def link_1_click(self, **event_args):
      open_form('admin',user=self.admin)

    def link_4_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('admin.admin_add_user',user=self.admin)

    def link6_copy_click(self, **event_args):
      open_form("admin.transaction_monitoring",user = self.user)

    def link6_copy_2_click(self, **event_args):
      if self.user['users_usertype'] == 'super_admin':
          # Open the admin creation form
          open_form("admin.create_admin", user=self.user)
      else:
          # Show an alert if the user is not a super admin
          alert("You're not a super admin. Only super admins can perform this action.")

    def link6_copy_3_click(self, **event_args):
      open_form("admin.user_support",user = self.user)

    def link6_copy_4_click(self, **event_args):
      open_form("admin.add_bank_account",user = self.user)

    