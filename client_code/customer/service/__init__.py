from ._anvil_designer import serviceTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class service(serviceTemplate):
    def __init__(self,user=None,**properties):
        self.init_components(**properties)
        self.user = user

    def button_1_click(self, **event_args):
        query = self.text_box_1.text
        # Fetch user information from the "users" table
        user_info = app_tables.wallet_users.get(phone=self.user['phone'])

        if user_info is not None:
            # Update the "Services" table with the query and user information
            app_tables.wallet_users_service.add_row(
                username=user_info['username'],
                phone=user_info['phone'],
                query=query
            )
            alert("Your query has been submitted, and our Technical Executive will get in touch with you")
        else:
            alert("User information not found.")

    def link_2_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.deposit",user=self.user)

    def link_3_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.transfer",user=self.user)

    def link_4_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.withdraw",user=self.user)

    def link_7_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer", user=self.user)

    def link_13_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("Home")

    def link_1_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.service",user=self.user)
