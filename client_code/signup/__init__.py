from ._anvil_designer import signupTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import re

class signup(signupTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.card_4.visible = False
    self.phone_card.visible = False
    self.aadhar_card.visible = False
    self.pan_card.visible= False 
    self.pass_card.visible = False 
    #self.text_box_3.text=anvil.server.call('load_secret_data')

  def primary_color_1_click(self, **event_args):
        existing_user = anvil.server.call('get_user_by_phone', str(self.text_box_3.text).strip())

        if existing_user:
            self.card_4.visible = True
            self.text_box_3.text=''
        else:
            count = 0
            phone_number = str(self.text_box_3.text).strip()
            if self.validate_phone_number(phone_number):
                count += 1
                self.label_15.text ="Phone number is correct"
                self.label_15.foreground = "#008000"
            else:
                self.phone_card.visible = True
                self.label_15.text ="Invalid Phone Number"
                self.label_15.foreground = "#990000"
                self.text_box_3.text=''
                self.text_box_3.focus()

            aadhar = int(self.text_box_7.text)
            if len(str(aadhar)) == 12:
                count += 1
                self.label_16.text ="Aadhar details correct"
                self.label_16.foreground = "#008000"
            else:
                self.aadhar_card.visible = True
                self.label_16.text ="Please verify the entered Aadhar details"
                self.label_16.foreground = "#990000"
                self.text_box_7.text=''
                self.text_box_7.focus()

            converted_text = self.text_box_8.text
            if self.is_pan_card_detail(converted_text):
                self.label_14.text ="Pan card is valid"
                self.label_14.foreground = "#008000"
                count += 1
            else:
                self.pan_card.visible = True
                self.label_14.text ="Please verify the entered pan card details"
                self.label_14.foreground = "#990000"
                self.text_box_8.text=''
                self.text_box_8.focus()

            password = self.text_box_5.text
            if self.validate_password(password):
                count += 1
                self.label_17.text = "Password meets criteria"
                self.label_17.foreground = "#008000"
        
                # Proceed with password match validation
                if self.text_box_5.text != '' and self.text_box_5.text == self.text_box_6.text:
                    count += 1
                else:
                    self.pass_card.visible = True
                    self.label_17.text = "Passwords don't match"
                    self.label_17.foreground = "#990000"
                    self.text_box_5.text =''
                    self.text_box_5.focus()
                    self.text_box_6.text =''
                    self.text_box_6.focus()
            else:
                self.pass_card.visible = True
                self.label_17.text = "Password must have at least 1 number, 1 character, 1 symbol, and be at least 8 characters long."
                self.label_17.foreground = "#990000"
                self.text_box_5.text = ''
                self.text_box_6.text = ''
                self.text_box_5.focus()
            if not self.text_box_9.visible:
                alert("verify your email")
            else:
                # If email verification is not yet completed, wait for it to complete
                if not self.email_verified:
                    return
                else:
                    # Email verified, proceed with account creation
                    anvil.server.call(
                        'add_info',
                        self.text_box_1.text,
                        self.text_box_2.text,
                        self.drop_down_1.selected_value,
                        self.text_box_3.text,
                        self.text_box_7.text,
                        self.text_box_8.text,
                        self.text_box_6.text
                    )
                    alert("Thank you " + self.text_box_1.text + ", for signing up! Your account has been successfully created")
                    open_form('login')
  def link_1_click(self, **event_args):
    open_form('Home')

  def text_box_8_change(self, **event_args):
    current_text = self.text_box_8.text
    converted_text = current_text.upper()
    self.text_box_8.text = converted_text
    
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

  def validate_button_click(self, **event_args):
    phone_number = str(self.text_box_3.text).strip()  
  
  def validate_phone_number(self, phone_number):
    pattern = r'^[6-9]\d{9}$'
    if re.match(pattern, str(phone_number)):
        return True  
    else:
        return False 

  def validate_button_click(self, **event_args):
        password = self.text_box_5.text
        if self.validate_password(password):
            self.label_17.text = "Password is valid"
            self.label_17.foreground = "#008000"
        else:
            self.label_17.text = "Password must have at least 1 number, 1 character, 1 symbol, and be at least 8 characters long."
            self.label_17.foreground = "#FF0000"

  def validate_password(self, password):
        pattern = r'^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if re.match(pattern, password):
            return True
        else:
            return False

  def button_1_click(self, **event_args):
        

        user_email = self.text_box_2.text
        
        # Check if the email exists in the database
        matching_users = app_tables.wallet_users.search(email=user_email)
        
        if matching_users:
            # Email exists, generate OTP
            otp = anvil.server.call('generate_otp')
            
            # Call the server function to send OTP via email
            anvil.server.call('send_otp_email', user_email, otp)
            
            # Inform the user that the OTP has been sent
            alert("OTP has been sent to your email.")
            
            # Hide text_box_2 and label_4, and show text_box_3
            self.text_box_9.visible=True
            self.label_3.visible=True
            
        else:
            # Email doesn't exist, display an error message
            alert("Email not found. Please enter a valid email address.")
            

  def text_box_9_pressed_enter(self, **event_args):
        # Wait for a short duration before each attempt
        entered_otp = self.text_box_9.text
        
        # Get the stored OTP from the server
        stored_otp = anvil.server.call('get_stored_otp')
        
        # Check if the entered OTP matches the stored OTP
        if entered_otp == stored_otp:
            # OTP is valid, display success message in green color
            self.label_3.text = "OTP is valid"
            self.label_3.foreground = "#008000"  # Green color
            
            # Hide text_box_3 and show text_box_4
            
        else:
            # OTP is invalid, display a message
            self.label_3.text = "Invalid OTP. Please try again."

      
            self.label_3.foreground = "#FF0000"  # Red color
            