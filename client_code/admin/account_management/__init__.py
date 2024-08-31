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
            self.label_656.text = user['user_fullname']
        
        # Set initial page number and page size
        self.page_number = 1
        self.page_size = 5

        # Initialize filter variables
        self.fullname_filter = None
        self.phone_number_filter = None
        self.status_filter = None
        self.filter_user_type = None
        
        self.refresh_users()  # Load all users initially
        ItemTemplate6.user = self.user

    def refresh_users(self):
        # Fetch all users from the table
        users = anvil.server.call('get_users_from_db')
    
        # If users is None, initialize it as an empty list to avoid TypeError
        if users is None:
            users = []
    
        # Counters for different user types
        total_customers = 0
        total_admins = 0
        total_super_admins = 0
    
        # Create a list of dictionaries with status color for display purposes
        user_list = []
        for user in users:
            # Unpack tuple values from the query result
            (user_fullname, user_phone_number, user_type, user_email, 
            user_profile_photo, user_inactive, user_hold) = user
    
            # Count the users of each type
            if user_type == 'customer':
                total_customers += 1
            elif user_type == 'admin':
                total_admins += 1
            elif user_type == 'super_admin':
                total_super_admins += 1
    
            # Create a dictionary for each user with status color
            user_dict = {
                'user_fullname': user_fullname,
                'user_phone_number': user_phone_number,
                'user_type': user_type,
                'user_email': user_email,
                'user_profile_photo': user_profile_photo,
                'user_inactive': user_inactive,
                'user_hold': user_hold,
                'status_color': 'green' if not user_hold and not user_inactive else ('red' if user_hold else 'gray')
            }
            user_list.append(user_dict)
    
        # Filter users based on usertype if filter_user_type is provided
        if self.filter_user_type:
            user_list = [user for user in user_list if user['user_type'] == self.filter_user_type]
    
        # Filter users based on status if status filter is provided
        if self.status_filter == "Active":
            user_list = [user for user in user_list if user['user_inactive'] is None and user['user_hold'] is None]
        elif self.status_filter == "Inactive":
            user_list = [user for user in user_list if user['user_inactive'] is True]
        elif self.status_filter == "Hold":
            user_list = [user for user in user_list if user['user_hold'] is True]
    
        # Filter users based on fullname if fullname filter is provided
        if self.fullname_filter and isinstance(self.fullname_filter, str):
            user_list = [user for user in user_list if user['user_fullname'] and user['user_fullname'].lower().startswith(self.fullname_filter.lower())]
    
        # Filter users based on phone number if phone filter is provided
        if self.phone_number_filter and isinstance(self.phone_number_filter, str):
            user_list = [user for user in user_list if user['user_phone_number'] and str(user['user_phone_number']).startswith(self.phone_number_filter)]
    
        # Pagination
        total_pages = (len(user_list) + self.page_size - 1) // self.page_size
        start_index = (self.page_number - 1) * self.page_size
        end_index = start_index + self.page_size
        paginated_users = user_list[start_index:end_index]
    
        # Set items in the repeating panel
        self.repeating_panel_1.items = paginated_users
    
        # Update user type counters
        self.label_5.text = str(total_customers)
        self.label_10.text = str(total_admins)
        self.label_12.text = str(total_super_admins)
        self.text_box_2.text = str(self.page_number)
    
        # Update pagination buttons
        self.update_buttons(total_pages)


    def update_buttons(self, total_pages):
        self.button_111.enabled = self.page_number > 1
        self.button_222.enabled = self.page_number < total_pages

    def link_8_click(self, **event_args):
        """This method is called when the link is clicked"""
        self.page_number = 1
        self.filter_user_type = 'customer'
        self.refresh_users()  # Filter for customers only

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
        self.page_number = 1
        self.filter_user_type = None
        self.status_filter = None
        self.fullname_filter = None
        self.phone_number_filter = None
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
        self.page_number = 1
        self.status_filter = self.drop_down_1.selected_value

        # Refresh users based on the selected status filter
        self.refresh_users()

    def link_9_click(self, **event_args):
        """This method is called when the link is clicked"""
        self.page_number = 1
        self.filter_user_type = 'admin'
        self.refresh_users()  # Filter for admin users only

    def link_10_click(self, **event_args):
        """This method is called when the link is clicked"""
        self.page_number = 1
        self.filter_user_type = 'super_admin'
        self.refresh_users()  # Filter for super admin users only

    def text_box_1_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        self.page_number = 1
        search_value = self.text_box_1.text
        if search_value.isdigit():
            self.phone_number_filter = search_value
            self.fullname_filter = None
        else:
            self.fullname_filter = search_value
            self.phone_number_filter = None
        self.refresh_users()

    def link6_copy_click(self, **event_args):
        open_form("admin.transaction_monitoring",user = self.user)

    def link6_copy_2_click(self, **event_args):
        # Check if the user is a super admin
        if self.user['user_type'] == 'super_admin':
            # Open the admin creation form
            open_form("admin.create_admin", user=self.user)
        else:
            # Show an alert if the user is not a super admin
            alert("You're not a super admin. Only super admins can perform this action.")

    def link6_copy_3_click(self, **event_args):
        open_form("admin.user_support",user = self.user)

    def link6_copy_4_click(self, **event_args):
        open_form("admin.add_bank_account",user = self.user)

    def button_111_click(self, **event_args):
        """This method is called when the previous page button is clicked"""
        if self.page_number > 1:
            self.page_number -= 1
            self.refresh_users()

    def button_222_click(self, **event_args):
        """This method is called when the next page button is clicked"""
        self.page_number += 1
        self.refresh_users()
