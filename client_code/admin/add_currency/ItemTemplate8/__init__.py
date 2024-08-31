from ._anvil_designer import ItemTemplate8Template
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate8(ItemTemplate8Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.user_count_displayed = False

  def view_user_click(self, **event_args):
        if not self.user_count_displayed:
            selected_currency = self.item
            currency_code = selected_currency['code']
            
            # Call server function to get the user count for the selected currency
            try:
                count_of_users = anvil.server.call('get_user_count_by_currency', currency_code)
                self.view_user.text = f"{count_of_users} Users"
                self.user_count_displayed = True
            except Exception as e:
                alert(f"Error fetching user count: {e}")
        else:
            # Reset the display text
            self.view_user.text = "View number of users"
            self.user_count_displayed = False
    # if not self.user_count_displayed:
    #   selected_currency = self.item
    #   currency_code = selected_currency['admins_add_currency_code']
    #   currency_type_matches = app_tables.wallet_users_balance.search(users_balance_currency_type=currency_code)
    #   count_of_users = len(currency_type_matches)
    #   self.view_user.text = f"{count_of_users} Users"
    #   self.user_count_displayed = True
    # else:
    #   self.view_user.text = "view number of user"
    #   self.user_count_displayed = False

 

  def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        selected_currency = self.item
        currency_code = selected_currency['code']
        
        # Call server function to delete the currency type
        try:
            success = anvil.server.call('delete_currency_by_code', currency_code)
            if success:
                alert(f"Deleted currency type {currency_code}")
            else:
                alert(f"Currency type {currency_code} not found")
            
            # Call the refresh method in the parent form to update the displayed data
            parent_form = get_open_form()
            if hasattr(parent_form, 'refresh_currency_data'):
                parent_form.refresh_currency_data()
        except Exception as e:
            alert(f"Error deleting currency: {e}")
    # selected_currency = self.item
    # currency_code = selected_currency['admins_add_currency_code']
    
    # # Find and delete the currency type
    # currency_type_record = app_tables.wallet_admins_add_currency.get(admins_add_currency_code=currency_code)
    
    # if currency_type_record:
    #   currency_type_record.delete()
    #   alert(f"Deleted currency type {currency_code}")
    # else:
    #   alert(f"Currency type {currency_code} not found")
    
    # # Call the refresh method in the parent form
    # get_open_form().refresh_currency_data()

 
