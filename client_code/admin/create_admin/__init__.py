from ._anvil_designer import create_adminTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables
from datetime import datetime
import re

class create_admin(create_adminTemplate):
    def _init_(self, user=None, **properties):
        self.init_components(**properties)
        self.user = user
        self.label_12.text = datetime.now().strftime('%d %b %Y')
        self.which_admin_created_account = user['user_fullname']
        print(self.which_admin_created_account)

    def button_1_click(self, **event_args):
        date_of_admins_account_created = datetime.now().date()

        # Validate phone number format
        phone_number = int(self.text_box_4.text)
        if not self.validate_phone_number(phone_number):
            self.label_13.visible = True
            self.label_13.foreground = "#990000"
            self.label_13.text = "Please check the entered phone number"
            self.text_box_4.text = ''
            self.text_box_4.focus()
            return
        else:
            self.label_13.visible = True
            self.label_13.foreground = "green"
            self.label_13.text = "Phone number is correct"

        # Check if admin with this phone number already exists
        phone_number_exists = anvil.server.call('get_user_by_phone', phone_number)
        if phone_number_exists:
            alert(f"Phone number '{phone_number}' is already in use.")
            return

        # Check if email exists
        email = self.text_box_2.text.strip().lower()
        email_exists = anvil.server.call('check_email_exists', email)
        if email_exists:
            alert(f"Email '{email}' is already in use.")
            return

        # Check if passwords match
        if self.text_box_5.text != self.text_box_6.text:
            self.label_9.visible = True
            self.label_9.foreground = "#990000"
            self.label_9.text = "Passwords don't match"
            self.text_box_5.text = ''
            self.text_box_6.text = ''
            self.text_box_5.focus()
            return
        else:
            self.label_9.visible = True
            self.label_9.foreground = "green"
            self.label_9.text = "Password matches"

        try:
            user_id = anvil.server.call('generate_user_id')  # Generate or fetch user ID if needed
            joined_date = datetime.now().date()

            # Ensure the dates are in the correct format
            dob_str = self.date_picker_1.date.strftime('%Y-%m-%d')
            joined_date_str = joined_date.strftime('%Y-%m-%d')

            anvil.server.call(
                'add_admins_info',
                user_id,
                self.text_box_1.text,  # Full name
                email,
                phone_number,
                self.text_box_5.text,  # Password
                dob_str,  # Date of Birth
                str(self.drop_down_1.selected_value),  # Gender
                joined_date_str  # Joined Date
            )

            print('Admin credentials stored for login')
            open_form('admin')
        except Exception as e:
            alert(f"Error adding admin: {str(e)}")

    def validate_phone_number(self, phone_number):
        pattern = r'^[6-9]\d{9}$'
        return re.match(pattern, str(phone_number))

    def link_8_copy_click(self, **event_args):
        open_form('admin', user=self.user)

    def link_8_click(self, **event_args):
        open_form('admin',user=self.user)

    def link_1_click(self, **event_args):
        open_form('admin.report_analysis',user=self.user)

    def link_2_click(self, **event_args):
        open_form('admin.account_management',user=self.user)

    def link_3_click(self, **event_args):
        open_form('admin.transaction_monitoring',user=self.user)

    def link_10_click(self, **event_args):
        open_form('admin.add_currency',user=self.user)

    def link_5_click(self, **event_args):
        open_form('admin.audit_trail',user=self.user)

    def link_6_click(self, **event_args):
        pass

    def link_5_copy_2_click(self, **event_args):
        open_form("admin.admin_add_user",user=self.user)

    def link_5_copy_3_click(self, **event_args):
        if self.user['user_type'] == 'super_admin':
            open_form("admin.create_admin", user=self.user)
        else:
            alert("You're not a super admin. Only super admins can perform this action.")

    def link_5_copy_4_click(self, **event_args):
        open_form("admin.user_support",user=self.user)

    def link_5_copy_5_click(self, **event_args):
        open_form("admin.add_bank_account",user=self.user)
# from ._anvil_designer import create_adminTemplate
# from anvil import *
# import anvil.server
# import anvil.tables as tables
# from anvil.tables import app_tables
# from datetime import datetime
# import re

# class create_admin(create_adminTemplate):
#     def __init__(self, user=None, **properties):
#         self.init_components(**properties)
#         self.user = user
#         self.label_12.text = datetime.now().strftime('%d %b %Y')
#         # self.which_admin_created_account = user['user_username']
#         # print(self.which_admin_created_account)

#     def button_1_click(self, **event_args):
#         # date_of_admins_account_created = datetime.now().date()

#         # Validate phone number format
#         phone_number = int(self.text_box_4.text)
#         if not self.validate_phone_number(phone_number):
#             self.label_13.visible = True
#             self.label_13.foreground = "#990000"
#             self.label_13.text = "Please check the entered phone number"
#             self.text_box_4.text = ''
#             self.text_box_4.focus()
#             return
#         else:
#             self.label_13.visible = True
#             self.label_13.foreground = "green"
#             self.label_13.text = "Phone number is correct"

       
#         phone_number_exists = anvil.server.call('check_phone_number_exists', phone_number)
#         if phone_number_exists:
#             alert(f"Phone number '{phone_number}' is already in use.")
#             return
    
    
#         # Check if email exists
#         email = self.text_box_2.text.strip().lower()
#         email_exists = anvil.server.call('check_email_exists', email)
#         if email_exists:
#             alert(f"Email '{email}' is already in use.")
#             return

#         # Check if passwords match
#         if self.text_box_5.text != self.text_box_6.text:
#             self.label_9.visible = True
#             self.label_9.foreground = "#990000"
#             self.label_9.text = "Passwords don't match"
#             self.text_box_5.text = ''
#             self.text_box_6.text = ''
#             self.text_box_5.focus()
#             return
#         else:
#             self.label_9.visible = True
#             self.label_9.foreground = "green"
#             self.label_9.text = "Password matches"

#         try:
#             user_id = anvil.server.call('generate_user_id')  # Call the server-side function
#             joined_date = datetime.now().date()

#             # Ensure the date is in the correct format
#             dob_str = self.date_picker_1.date.strftime('%Y-%m-%d')
#             joined_date_str = joined_date.strftime('%Y-%m-%d')


#             anvil.server.call(
#                 'add_admins_info',
#                 user_id,
#                 self.text_box_1.text,  # Full name
#                 email,
#                 phone_number,
#                 self.text_box_5.text,  # Password
#                 dob_str,  # Date of Birth
#                 str(self.drop_down_1.selected_value),
#                 joined_date_str  # Joined Date
#             )
#             print('Admin credentials stored for login')
#         except Exception as e:
#             alert(f"Error adding admin: {str(e)}")

#     def validate_phone_number(self, phone_number):
#         pattern = r'^[6-9]\d{9}$'
#         return re.match(pattern, str(phone_number))

#     def link_8_copy_click(self, **event_args):
#         open_form('admin', user=self.user)

#     def link_8_click(self, **event_args):
#         open_form('admin',user=self.user)

#     def link_1_click(self, **event_args):
#         open_form('admin.report_analysis',user=self.user)

#     def link_2_click(self, **event_args):
#         open_form('admin.account_management',user=self.user)

#     def link_3_click(self, **event_args):
#         open_form('admin.transaction_monitoring',user=self.user)

#     def link_10_click(self, **event_args):
#         open_form('admin.add_currency',user=self.user)

#     def link_5_click(self, **event_args):
#         open_form('admin.audit_trail',user=self.user)

#     def link_6_click(self, **event_args):
#         pass

#     def link_5_copy_2_click(self, **event_args):
#         open_form("admin.admin_add_user",user=self.user)

#     def link_5_copy_3_click(self, **event_args):
#         if self.user['user_type'] == 'super_admin':
#             open_form("admin.create_admin", user=self.user)
#         else:
#             alert("You're not a super admin. Only super admins can perform this action.")

#     def link_5_copy_4_click(self, **event_args):
#         open_form("admin.user_support",user=self.user)

#     def link_5_copy_5_click(self, **event_args):
#         open_form("admin.add_bank_account",user=self.user)
