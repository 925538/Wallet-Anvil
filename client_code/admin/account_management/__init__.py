from ._anvil_designer import account_managementTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .ItemTemplate6 import ItemTemplate6

class account_management(account_managementTemplate):
    def __init__(self, user=None, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.user = user
        if user is not None:
            self.label_656.text = user['users_username']
        
        self.refresh_users()  # Load all users initially
        ItemTemplate6.user = self.user

    def refresh_users(self, username_filter=None, phone_filter=None, status_filter=None, filter_usertype=None):
        # Fetch all users from the table
        users = app_tables.wallet_users.search()
        
        # Counters for different user types
        total_customers = 0
        total_admins = 0
        total_super_admins = 0
        
        # Count the users of each type
        for user in users:
            if user['users_usertype'] == 'customer':
                total_customers += 1
            elif user['users_usertype'] == 'admin':
                total_admins += 1
            elif user['users_usertype'] == 'super_admin':
                total_super_admins += 1

        # Filter users based on usertype if filter_usertype is provided
        if filter_usertype:
            users = [user for user in users if user['users_usertype'] == filter_usertype]

        # Filter users based on status if status filter is provided
        if status_filter == "Active":
            users = [user for user in users if user['users_inactive'] is None and user['users_hold'] is None]
        elif status_filter == "Inactive":
            users = [user for user in users if user['users_inactive'] is True]
        elif status_filter == "Hold":
            users = [user for user in users if user['users_hold'] is True]

        # Filter users based on username if username filter is provided
        if username_filter:
            users = [user for user in users if user['users_username'].lower().startswith(username_filter.lower())]

        # Filter users based on phone number if phone filter is provided
        if phone_filter:
            users = [user for user in users if str(user['users_phone']).startswith(phone_filter)]

        # Create a list of dictionaries with status color for display purposes
        user_list = []
        for user in users:
            user_dict = dict(user)
            if user['users_hold']:
                user_dict['status_color'] = 'red'
            elif user['users_inactive']:
                user_dict['status_color'] = 'gray'
            else:
                user_dict['status_color'] = 'green'
            user_list.append(user_dict)

        # Set items in the repeating panel
        self.repeating_panel_1.items = user_list
        
        self.label_5.text =  total_customers
        self.label_10.text =  total_admins
        self.label_12.text =  total_super_admins

    def link_8_click(self, **event_args):
        """This method is called when the link is clicked"""
        self.refresh_users(filter_usertype='customer')  # Filter for customers only

    def link_10_copy_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.user_support', user=self.user)

    def button_3_click(self, **event_args):
        open_form('admin.admin_add_user', user=self.user)

    def link_1_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin', user=self.user)

    def link_2_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.report_analysis', user=self.user)

    def link_7_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.transaction_monitoring', user=self.user)

    def link_6_click(self, **event_args):
        """This method is called when the link is clicked"""
        self.refresh_users()  # Display all users

    def link_5_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.add_currency', user=self.user)

    def link_4_click(self, **event_args):
        open_form('admin.admin_add_user', user=self.user)

    def link_3_click(self, **event_args):
        """This method is called when the link is clicked"""
        pass

    def drop_down_1_change(self, **event_args):
        """This method is called when an item is selected"""
        # Get the selected status filter
        status_filter = self.drop_down_1.selected_value

        # Refresh users based on the selected status filter
        self.refresh_users(status_filter=status_filter)

    def link_9_click(self, **event_args):
        """This method is called when the link is clicked"""
        self.refresh_users(filter_usertype='admin')  # Filter for admin users only

    def link_10_click(self, **event_args):
        """This method is called when the link is clicked"""
        self.refresh_users(filter_usertype='super_admin')  # Filter for super admin users only

    def text_box_1_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        search_value = self.text_box_1.text
        if search_value.isdigit():
            self.refresh_users(phone_filter=search_value)
        else:
            self.refresh_users(username_filter=search_value)

    def link6_copy_click(self, **event_args):
        open_form("admin.transaction_monitoring",user = self.user)

    def link6_copy_2_click(self, **event_args):
        # Check if the user is a super admin
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
