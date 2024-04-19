from ._anvil_designer import forgot_passwordTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import random
from anvil import alert

class forgot_password(forgot_passwordTemplate):
    def button_1_click(self, **event_args):
        # Get the email entered by the user
        user_email = self.text_box_1.text
        
        # Query the wallet_users table to check if the email exists
        matching_users = app_tables.wallet_users.search(email=user_email)
        
        if matching_users:
            # Email exists, generate OTP and call the server function to send it
            otp = self.generate_otp()
            anvil.server.call('send_otp_email', user_email, otp)
            # Optionally, you can inform the user that the OTP has been sent
            alert("OTP has been sent to your email.")
        else:
            # Email doesn't exist, display an error message
            alert("Email not found. Please enter a valid email address.")
    
    def generate_otp(self):
        # Generate a 6-digit OTP
        otp = ''.join(random.choice('0123456789') for _ in range(6))
        return otp
    
    def text_box_2_pressed_enter(self, **event_args):
    # Get the entered OTP from text_box_2
    entered_otp = self.text_box_2.text
    
    # Get the stored OTP from the server
    stored_otp = anvil.server.call('get_stored_otp')
    
    print("Entered OTP:", entered_otp)
    print("Stored OTP:", stored_otp)
    
    # Check if the entered OTP matches the stored OTP
    if entered_otp == stored_otp:
        # OTP is valid, display success message in green color
        self.label_4.text = "OTP is valid"
        self.label_4.foreground = "#008000"  # Green color
    else:
        # OTP is invalid, display error message in red color
        self.label_4.text = "Invalid OTP"
        self.label_4.foreground = "#FF0000"  # Red color

    