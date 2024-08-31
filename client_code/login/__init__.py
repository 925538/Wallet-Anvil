from ._anvil_designer import loginTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables

class login(loginTemplate):

  def init(self, **properties):
    self.init_components(**properties)
    self.card_3.visible = False
    self.text_box_2.visible = False
    self.button_1.visible = False
    self.button_2.visible = False
    self.otp_sent = False

  def text_box_3_pressed_enter(self, **event_args):
    self.primary_color_1_click()

  def link_2_click(self, **event_args):
    open_form('signup')

  def link_1_click(self, **event_args):
    open_form('forgot_password')

  def primary_color_1_click(self, **event_args):
    login_input = self.text_box_1.text.strip()
    password = self.text_box_3.text.strip()

    if not login_input or not password:
      alert("Please enter both username and password.")
      return

    user = anvil.server.call('login_user', login_input, password)

    
      # if user['users_banned'] is not None and user['users_banned']:
      #   alert("This Account is Banned")
      #   open_form('login.banned_form', user=user)
      #   return

      # if user['users_hold'] is not None and user['users_hold']:
      #   alert("Your account is on hold/freeze. Please try again later.", title="Account On Hold")
      #   return

    user_type = user.get('user_type')

    if user_type in ['admin', 'super_admin']:
      open_form('admin', user=user)
    elif user_type == 'customer':
      open_form('customer', user=user)
    elif user is not None and user['user_password'] != password:
      self.card_3.visible = True
      self.label_4.visible = True
      self.label_5.visible = False
      self.label_6.visible = False
      self.text_box_3.text = ''
      self.text_box_3.focus()
    else:
      alert("Incorrect username or password. Please try again.")
      self.text_box_3.text = ''
      self.text_box_3.focus()

  def link_2_click(self, **event_args):
    open_form('signup')

  def link_1_click(self, **event_args):
    open_form('forgot_password')

  def link_3_click(self, **event_args):
    """This method is called when the link to login with OTP is clicked"""
    self.text_box_3.visible = False
    self.text_box_2.visible = True
    self.primary_color_1.visible = False
    self.button_1.visible = False
    self.link_1.visible = False 
    self.button_1.visible = True
    self.link_3.visible = False
    

  def button_1_click(self, **event_args):
    """This method is called when the send OTP button is clicked"""
    email = self.text_box_1.text.strip()
    if not email:
        alert("Please enter your email.")
        return

    # Check if the email is registered
    email_exists = anvil.server.call('check_email_exists', email)
    if not email_exists:
        alert("This email is not registered.")
        return

    # Send OTP
    self.otp = anvil.server.call('send_email_otp', email)
    if self.otp:
        alert(f"OTP has been sent to {email}")

    # Update UI elements
    self.primary_color_2.visible =True
    self.text_box_2.enabled = True
    self.button_1.visible = False
    self.button_2.visible = True




  def button_2_click(self, **event_args):
    entered_otp = self.text_box_2.text.strip()
    if str(self.otp) == entered_otp:
      alert('OTP verified successfully')
      self.primary_color_2.enabled=True
    else:
      alert("Invalid OTP")
    """This method is called when the verify OTP button is clicked"""

  def primary_color_2_click(self, **event_args):
    login_input = self.text_box_1.text.strip()

    if not login_input:
        alert("Please enter your email.")
        return

    user = anvil.server.call('get_user_for_login', login_input)

    if user is not None:
        # if user['users_banned'] is not None and user['users_banned']:
        #     alert("This Account is Banned")
        #     open_form('login.banned_form', user=user)
        #     return

        # if user['users_hold'] is not None and user['users_hold']:
        #     alert("Your account is on hold/freeze. Please try again later.", title="Account On Hold")
        #     return

        user_type = user.get('users_type')

        if user_type in ['admin', 'super_admin']:
            open_form('admin', user=user)
        elif user_type == 'customer':
            open_form('customer', user=user)
    
    else:
        alert("User not found. Please try again.")
# from ._anvil_designer import loginTemplate
# from anvil import *
# import anvil.users
# import anvil.server
# import anvil.tables as tables
# from anvil.tables import app_tables
# import anvil.js


# class login(loginTemplate):

#   def _init_(self, **properties):
#     self.init_components(**properties)
#     self.card_3.visible = False
#     self.text_box_2.visible = False
#     self.button_1.visible = False
#     self.button_2.visible = False
#     self.otp_sent = False

#   def text_box_3_pressed_enter(self, **event_args):
#     self.primary_color_1_click()

#   def link_2_click(self, **event_args):
#     open_form('signup')

#   def link_1_click(self, **event_args):
#     open_form('forgot_password')

#   def primary_color_1_click(self, **event_args):
#    login_input = self.text_box_1.text.strip()
#    password = self.text_box_3.text.strip()

#    if not login_input or not password:
#         alert("Please enter both username and password.")
#         return

#    user = anvil.server.call('get_user_for_login', login_input)

#    if user is not None and user['user_password'] == password:
#    #      if user['users_banned']:
#    #          alert("This Account is Banned")
#    #          open_form('login.banned_form', user=user)
#    #          return

#    #      if user['users_hold']:
#    #          alert("Your account is on hold/freeze. Please try again later.", title="Account On Hold")
#    #          return

#         user_type = user['user_type']

#         if user_type in ['admin', 'super_admin']:
#             open_form('admin', user=user)
#         elif user_type == 'customer':
#             open_form('customer', user=user)
#    elif user is not None and user['user_password'] != password:
#         self.card_3.visible = True
#         self.label_4.visible = True
#         self.label_5.visible = False
#         self.label_6.visible = False
#         self.text_box_3.text = ''
#         self.text_box_3.focus()
#    else:
#         alert("Incorrect username or password. Please try again.")
#         self.text_box_3.text = ''
#         self.text_box_3.focus()
#   def link_2_click(self, **event_args):
#     open_form('signup')

#   def link_1_click(self, **event_args):
#     open_form('forgot_password')

#   def link_3_click(self, **event_args):
#     """This method is called when the link to login with OTP is clicked"""
#     self.text_box_3.visible = False
#     self.text_box_2.visible = True
#     self.primary_color_1.visible = False
#     self.button_1.visible = False
#     self.link_1.visible = False 
#     self.button_1.visible = True
#     self.link_3.visible = False
    

#   def button_1_click(self, **event_args):
#     """This method is called when the send OTP button is clicked"""
#     email = self.text_box_1.text.strip()
#     if not email:
#         alert("Please enter your email.")
#         return

#     # Check if the email is registered
#     email_exists = anvil.server.call('check_email_exists', email)
#     if not email_exists:
#         alert("This email is not registered.")
#         return

#     # Send OTP
#     self.otp = anvil.server.call('send_email_otp', email)
#     if self.otp:
#         alert(f"OTP has been sent to {email}")

#     # Update UI elements
#     self.primary_color_2.visible =True
#     self.text_box_2.enabled = True
#     self.button_1.visible = False
#     self.button_2.visible = True




#   def button_2_click(self, **event_args):
#     entered_otp = self.text_box_2.text.strip()
#     if str(self.otp) == entered_otp:
#       alert('OTP verified successfully')
#       self.primary_color_2.enabled=True
#     else:
#       alert("Invalid OTP")
#     """This method is called when the verify OTP button is clicked"""

#   def primary_color_2_click(self, **event_args):
#     login_input = self.text_box_1.text.strip()

#     if not login_input:
#         alert("Please enter your email.")
#         return

#     user = anvil.server.call('get_user_for_login', login_input)

#     if user is not None:
#     #     if user['users_banned'] is not None and user['users_banned']:
#     #         alert("This Account is Banned")
#     #         open_form('login.banned_form', user=user)
#     #         return

#     #     if user['users_hold'] is not None and user['users_hold']:
#     #         alert("Your account is on hold/freeze. Please try again later.", title="Account On Hold")
#     #         return

#         user_type = user['user_type']

#         if user_type in ['admin', 'super admin']:
#             open_form('admin', user=user)
#         elif user_type == 'customer':
#             open_form('customer', user=user)
#     else:
#         alert("User not found. Please try again.")