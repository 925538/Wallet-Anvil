import anvil.server
from ._anvil_designer import admin_viewTemplate
from anvil import alert, open_form
from anvil.tables import app_tables
from datetime import datetime
import re

class admin_view(admin_viewTemplate):
    def __init__(self, user_data=None, phone_number=None, **properties):
        # self.user = user
        self.phone_number = phone_number
        self.init_components(**properties)
        self.edit_mode = False  # Initialize edit_mode attribute to False
        
        if phone_number is not None:
            self.text_box_13.text = phone_number  # Set textbox13 to display the phone number

            # Fetch all rows from wallet_users_balance table based on phone number
            user_balances = app_tables.wallet_users_balance.search(phone=phone_number)
            if user_balances:
                # Initialize balances for each currency type
                usd_balance = euro_balance = inr_balance = swiss_balance = None
                
                # Iterate over all matching rows
                for balance_row in user_balances:
                    # Check currency type and update corresponding balances
                    if balance_row['currency_type'] == 'USD':
                        usd_balance = balance_row['balance']
                    elif balance_row['currency_type'] == 'Euro':
                        euro_balance = balance_row['balance']
                    elif balance_row['currency_type'] == 'INR':
                        inr_balance = balance_row['balance']
                    elif balance_row['currency_type'] == 'Swiss':
                        swiss_balance = balance_row['balance']
                
                # Update text boxes with the retrieved balances
                self.text_box_8.text = str(usd_balance) if usd_balance is not None else "0"
                self.text_box_9.text = str(euro_balance) if euro_balance is not None else "0"
                self.text_box_10.text = str(inr_balance) if inr_balance is not None else "0"
                self.text_box_11.text = str(swiss_balance) if swiss_balance is not None else "0"
            else:
                # Set default value of 0 for all text boxes if no balances found
                self.text_box_8.text = "0"
                self.text_box_9.text = "0"
                self.text_box_10.text = "0"
                self.text_box_11.text = "0"
            
            user_data = app_tables.wallet_users.get(phone=phone_number)
            if user_data is not None:
                # Set text boxes with the retrieved user data
                self.text_box_1.text = user_data['username']  # Replace 'column1' with actual column names
                self.text_box_2.text = user_data['email']
                self.text_box_3.text = user_data['password']
                self.text_box_5.text = user_data['aadhar']
                self.text_box_6.text = user_data['pan']
                self.text_box_4.text = user_data['phone']
                self.text_box_7.text = user_data['address']
            else:
                # Set default value for text boxes if no user data found
                self.text_box_1.text = ""
                self.text_box_2.text = ""
                self.text_box_3.text = ""
                self.text_box_4.text = ""
                self.text_box_5.text = ""
                self.text_box_6.text = ""
                self.text_box_7.text = ""

            # Set button text based on the hold state
            self.set_button_text()

    def button_5_click(self, **event_args):
        username = self.text_box_1.text
        user_to_update = app_tables.wallet_users.get(username=username)
    
        if user_to_update is not None:
            # Check the current state of 'hold' column
            current_state = user_to_update['hold']
    
            # If 'hold' is None or 'true', user is considered frozen, otherwise unfrozen
            new_state = not current_state
    
            # Update the 'hold' column in the 'users' table
            user_to_update.update(hold=new_state if new_state else None)
    
            # Update button text based on the new state
            self.set_button_text()
    
            # Display alert based on the action
            alert_message = "User is frozen." if new_state else "User is unfrozen."
            alert(alert_message, title="Status")
    
            # Log the action
            self.log_action(username, [alert_message])
            print("Button 5 Clicked and action logged")  # Debug statement

    def set_button_text(self):
        username = self.text_box_1.text
        user_to_update = app_tables.wallet_users.get(username=username)
    
        # Get the current hold state from the database
        current_state = user_to_update['hold'] if user_to_update else None
    
        # Set the button text based on the current hold state
        self.button_5.text = "Unfreeze" if current_state else "Freeze"

    def button_2_click(self, **event_args):
      """This method is called when the button is clicked"""
      # Check if all text boxes 8, 9, 10, and 11 contain 0
      
      if (self.text_box_8.text == "0" and
          self.text_box_9.text == "0" and
          self.text_box_10.text == "0" and
          self.text_box_11.text == "0"):
          
          # Get the phone number from the form
          phone_number = self.phone_number
          
          row_to_delete = app_tables.wallet_users.get(phone=phone_number)
          if row_to_delete is not None:
              username = row_to_delete['username']  # Get the username before deleting the row
              row_to_delete.delete()
              
              # Log the deletion action
              self.log_action(username, ["User deleted"])
              
              # Optionally, display an alert to inform the user
              alert("Row deleted from wallet_users table.", title="Status")
      else:
          # If any of the text boxes contain values other than 0, inform the user
          alert("Values in text boxes 8, 9, 10, or 11 are not all 0.", title="Status")


    def toggle_edit_mode(self):
        # Toggle between view and edit modes
        self.edit_mode = not self.edit_mode
        self.text_box_1.enabled = self.edit_mode
        self.text_box_2.enabled = self.edit_mode
        self.text_box_3.enabled = self.edit_mode
        self.text_box_4.enabled = self.edit_mode
        self.text_box_5.enabled = False  # Aadhar (not editable during edit mode)
        self.text_box_6.enabled = False  # Pan (not editable during edit mode)
        self.text_box_7.enabled = self.edit_mode

        # Change button_1 text based on the mode
        self.button_1.text = 'Save Changes' if self.edit_mode else 'Edit'
        
    def is_valid_phone(self, phone):
        # Check if the phone number is not empty and has exactly 10 digits
        return bool(phone and re.match(r'^\d{10}$', str(phone)))
        
    def button_1_click(self, **event_args):
        if self.edit_mode:
            # Validate phone number
            if not self.is_valid_phone(self.text_box_4.text):
                alert("Please enter a valid 10-digit phone number.", title="Error")
                return

            # Save changes to the database
            username = self.text_box_1.text
            user_to_update = app_tables.wallet_users.get(username=username)

            if user_to_update is not None:
                changes_made = []
                # Check and log changes made by the admin
                if user_to_update['email'] != self.text_box_2.text:
                    changes_made.append(f"User '{username}' Email updated to '{self.text_box_2.text}'")
                if user_to_update['password'] != self.text_box_3.text:
                    changes_made.append(f"User '{username}' Password updated")
                if user_to_update['phone'] != self.text_box_4.text:
                    changes_made.append(f"User '{username}' Phone number updated to '{self.text_box_4.text}'")
                if user_to_update['address'] != self.text_box_7.text:
                    changes_made.append(f"User '{username}' Address updated to '{self.text_box_7.text}'")

                user_to_update.update(
                    email=self.text_box_2.text,
                    password=self.text_box_3.text,
                    phone=self.text_box_4.text,
                    aadhar=self.text_box_5.text,
                    pan=self.text_box_6.text,
                    address=self.text_box_7.text
                )

                # Log changes to 'actions' table if changes were made
                if changes_made:
                    self.log_action(username, changes_made)

                alert("Changes saved successfully.", title="Success")

                # Toggle back to view mode after saving changes
                self.toggle_edit_mode()
        else:
            # Toggle to edit mode
            self.toggle_edit_mode()

    def log_action(self, username, changes):
        # Log the action in the 'actions' table
        action = ", ".join(changes)
        app_tables.actions.add_row(username=username, changes=action, date=datetime.now())
        print("Action logged:", action)  # Debug statement
