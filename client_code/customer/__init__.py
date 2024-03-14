import anvil.server
from ._anvil_designer import customerTemplate
from anvil import open_form
from datetime import datetime

class customer(customerTemplate):
    def __init__(self, user=None, **properties):
        self.init_components(**properties)
        self.user = user  # Set the user attribute
        now = datetime.now()
        if now != self.user['last_login']:
            if self.user['daily_limit'] is None:
                self.user['user_limit'] = 100000
            else:
                self.user['user_limit'] = self.user['daily_limit']
            self.user['last_login'] = now
            self.user.update()

        if user:
            # Use the information from the logged-in user
            self.label_1.text = f"Welcome to Green Gate Financial, {user['username']}"

    def button_1_click(self, **event_args):
        # Open the Viewprofile form and pass the user information
        open_form('customer.Viewprofile', user=self.user)

    def button_6_click(self, **event_args):
      open_form('customer.wallet', user=self.user)

    def link_4_click(self, **event_args):
      open_form('customer.withdraw',user=self.user)


    def link_2_click(self, **event_args):
      open_form('customer.deposit',user=self.user)
     

    def link_7_click(self, **event_args):
      """This method is called when the link is clicked"""
      pass



    def button_3_click(self, **event_args):
        open_form('customer.transaction_history',user=self.user)

    def link_3_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.transfer',user=self.user)

    def button_2_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('customer.walletbalance',user=self.user)

    def button_4_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('customer.selftransfer',user=self.user)

    def link_13_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('Home')

    def button_5_click(self, **event_args):
      """This method is called when the button is clicked"""
      pass

