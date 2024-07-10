from ._anvil_designer import create_adminTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables
from datetime import datetime
import re

class create_admin(create_adminTemplate):
    def __init__(self, user=None, **properties):
        self.init_components(**properties)
        self.user = user
        self.label_12.text = datetime.now().strftime('%d %b %Y')
        self.which_admin_created_account = user['users_username']
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

        # Check if admin with this phone number already exists in wallet_users
        phone_number_exists = any(user['users_phone'] == phone_number for user in app_tables.wallet_users.search())

        if phone_number_exists:
            alert(f"Phone number '{self.text_box_4.text}' is already in use.")
            return
    
        # Check if email exists
        email = self.text_box_2.text.strip().lower()
        email_exists = any(user['users_email'].strip().lower() == email for user in app_tables.wallet_users.search())
        if email_exists:
            alert(f"Email '{self.text_box_2.text}' is already in use.")
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
            anvil.server.call(
                'add_admins_info',
                self.text_box_1.text,
                self.text_box_2.text,
                phone_number,
                self.text_box_5.text,
            )
            print('Admin credentials stored for login')
            app_tables.wallet_admins_create_admin_account.add_row(
                admins_username=self.text_box_1.text,
                admins_email=email,
                admins_phone=int(phone_number),
                admins_password=self.text_box_5.text,
                admins_date_of_birth=self.date_picker_1.date,
                admins_gender=self.drop_down_1.selected_value,
                which_admin_created_account=f'Admin - {self.which_admin_created_account}',
                date_of_admins_account_created=date_of_admins_account_created,
                admins_last_login=datetime.now()
            )
            alert(self.text_box_1.text + ' added')
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
        if self.user['users_usertype'] == 'super_admin':
            open_form("admin.create_admin", user=self.user)
        else:
            alert("You're not a super admin. Only super admins can perform this action.")

    def link_5_copy_4_click(self, **event_args):
        open_form("admin.user_support",user=self.user)

    def link_5_copy_5_click(self, **event_args):
        open_form("admin.add_bank_account",user=self.user)
