from ._anvil_designer import helpTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class help(helpTemplate):
    def __init__(self, user=None, **properties):
        # Set Form properties and Data Bindings.
        self.user = user
        self.init_components(**properties)
        self.card_4.visible=False
        
        if user is not None:
            # Fetch and display data from wallet_users_service table
            self.refresh_repeating_panel()

    def refresh_repeating_panel(self):
        # Fetch data from wallet_users_service for the current user and display in repeating panel
        if self.user:
            user_phone = self.user['users_phone']
            user_queries = app_tables.wallet_users_service.search(users_service_phone=user_phone)
            self.repeating_panel_1.items = user_queries
        else:
            self.repeating_panel_1.items = []

    def button_1_click(self, **event_args):
        """This method is called when button 1 is clicked"""
        query = self.text_area_1.text
        
        # Fetch user information from wallet_users table
        user_info = app_tables.wallet_users.get(users_phone=self.user['users_phone'])

        if user_info is not None:
            # Add query to wallet_users_service table
            app_tables.wallet_users_service.add_row(
                users_service_username=user_info['users_username'],
                users_service_phone=user_info['users_phone'],
                users_service_query=query,
                users_service_email=user_info['users_email']
            )
            alert("Your query has been submitted. Our Technical Executive will get in touch with you.")
            
            # Refresh the repeating panel to show updated data
            self.refresh_repeating_panel()
        else:
            alert("User information not found.")

    def link_2_click(self, **event_args):
        """This method is called when link 2 is clicked"""
        open_form("customer.deposit", user=self.user)

    def link_3_click(self, **event_args):
        """This method is called when link 3 is clicked"""
        open_form("customer.transfer", user=self.user)

    def link_4_click(self, **event_args):
        """This method is called when link 4 is clicked"""
        open_form("customer.withdraw", user=self.user)

    def link_7_click(self, **event_args):
        """This method is called when link 7 is clicked"""
        open_form("customer", user=self.user)

    def link_13_click(self, **event_args):
        """This method is called when link 13 is clicked"""
        open_form("Home")

    def link_1_copy_click(self, **event_args):
        """This method is called when link 1 copy is clicked"""
        open_form('customer.interaction', user=self.user)

    def link_1_copy_copy_click(self, **event_args):
        """This method is called when link 1 copy copy is clicked"""
        open_form('customer.report_bug', user=self.user)

    def link_26_click(self, **event_args):
        """This method is called when link 26 is clicked"""
        open_form('FAQ')

    def link_1_click(self, **event_args):
      """This method is called when the link is clicked"""
      self.card_4.visible=True
