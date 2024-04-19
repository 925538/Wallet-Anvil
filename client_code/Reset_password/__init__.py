from ._anvil_designer import Reset_passwordTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import re

class Reset_password(Reset_passwordTemplate):
    def __init__(self, user=None, **properties):
        self.user = user
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.label_3.visible = False  # Initially hide the email error message label
        self.label_4.visible = False  # Initially hide the password error message label
        self.label_5.visible = False  # Initially hide the new password error message label

    def text_box_1_change(self, **event_args):
        # Get the entered email from text_box_1
        entered_email = self.text_box_1.text

        # Check if the entered email matches the user's email
        if entered_email == self.user['email']:
            # Email is correct, hide the email error message label
            self.label_3.text = ""  # Clear any existing error message
            self.label_3.visible = False
        else:
            # Email is incorrect, display email error message label
            self.label_3.text = "Email is incorrect"
            self.label_3.foreground = "#FF0000"  # Set text color to red
            self.label_3.visible = True

    def text_box_2_change(self, **event_args):
        # Get the entered old password from text_box_2
        entered_old_password = self.text_box_2.text

        # Check if the entered old password matches the user's actual old password
        if entered_old_password == self.user['password']:
            # Old password is correct, hide the password error message label
            self.label_4.text = ""  # Clear any existing error message
            self.label_4.visible = False
        else:
            # Old password is incorrect, display password error message label
            self.label_4.text = "Password is incorrect"
            self.label_4.foreground = "#FF0000"  # Set text color to red
            self.label_4.visible = True

    def text_box_3_change(self, **event_args):
        # Get the entered new password from text_box_3
        entered_new_password = self.text_box_3.text

        # Check if the entered confirm password from text_box_4
        entered_confirm_password = self.text_box_4.text

        # Check if the entered new passwords match
        if entered_new_password == entered_confirm_password:
            # New passwords match, hide the new password error message label
            self.label_5.text = ""  # Clear any existing error message
            self.label_5.visible = False
        else:
            # New passwords don't match, display new password error message label
            self.label_5.text = "New passwords don't match"
            self.label_5.foreground = "#FF0000"  # Set text color to red
            self.label_5.visible = True

        # Validate the strength of the new password
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', entered_new_password):
            # If the password does not meet the criteria, display an error message
            self.label_5.text = "Password must contain at least 1 character, 1 number, and 1 symbol"
            self.label_5.foreground = "#FF0000"  # Set text color to red
            self.label_5.visible = True

    def primary_color_1_click(self, **event_args):
        # This method is called when the button primary_color_1 is clicked
        # Call the text_box_1_change, text_box_2_change, and text_box_3_change methods to trigger checks
        self.text_box_1_change()
        self.text_box_2_change()
        self.text_box_3_change()

        # Check if all checks pass (email, old password, new passwords match, and new password strength)
        if not self.label_3.visible and not self.label_4.visible and not self.label_5.visible:
            # Update the user's password to the new password
            self.user['password'] = self.text_box_4.text
            self.user.update()
            # Show a success message (you can replace this with any desired action)
            alert("Password updated successfully!")
            open_form('Login')
