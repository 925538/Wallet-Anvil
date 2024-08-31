from ._anvil_designer import user_supportTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class user_support(user_supportTemplate):
    def __init__(self, user=None, **properties):
        # Set Form properties and Data Bindings.
        self.user = user
        self.init_components(**properties)
        self.load_all_service_queries()

    def load_all_service_queries(self):
        """Load all service queries into the repeating panel."""
        # Call the server to get all queries
        queries = anvil.server.call('search_user_service_query', "")
        self.repeating_panel_1.items = queries
      
    def link_111_click(self, **event_args):
        """This method is called when the link is clicked"""
        # Filter to show only solved queries
        queries = anvil.server.call('search_user_service_query', "")
        solved_queries = [q for q in queries if q['users_update']]
        self.repeating_panel_1.items = solved_queries

    def link_2_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.report_analysis', user=self.user)

    def link_7_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.transaction_monitoring', user=self.user)

    def link_6_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.audit_trail', user=self.user)

    def link_5_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.add_currency', user=self.user)

    def link_4_click(self, **event_args):
        open_form('admin.admin_add_user', user=self.user)

    def link_3_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.account_management', user=self.user)

    def link_8_copy_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin', user=self.user)

    def button_8_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('Login')

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        username = self.text_box_1.text.strip()
        if username:
            # Call the server to search for the query by username
            results = anvil.server.call('search_user_service_query', username)
            if results:
                self.repeating_panel_2.items = results
            else:
                alert('User not found.')
                self.load_all_service_queries()
        else:
            alert('Please enter a username.')

    def link6_copy_click(self, **event_args):
        open_form("admin.transaction_monitoring", user=self.user)

    def link6_copy_2_click(self, **event_args):
        if self.user['users_usertype'] == 'super_admin':
            # Open the admin creation form
            open_form("admin.create_admin", user=self.user)
        else:
            # Show an alert if the user is not a super admin
            alert("You're not a super admin. Only super admins can perform this action.")

    def link6_copy_3_click(self, **event_args):
        open_form("admin.user_support", user=self.user)

    def link6_copy_4_click(self, **event_args):
        open_form("admin.add_bank_account", user=self.user)

    def link_12_click(self, **event_args):
        """This method is called when the link is clicked"""
        # Filter to show all queries
        self.load_all_service_queries()       
      
    def link_22_click(self, **event_args):
        """This method is called when the link is clicked"""
        # Filter to show only unsolved queries
        queries = anvil.server.call('search_user_service_query', "")
        unsolved_queries = [q for q in queries if not q['users_update']]
        self.repeating_panel_1.items = unsolved_queries
