from ._anvil_designer import ItemTemplate2Template
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate2(ItemTemplate2Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

    def update(self, bank_name, bank_icon_url):
        self.label_1.text = bank_name
        self.image_1.source = bank_icon_url

    def button_1_click(self, **event_args):
        """This method is called when the delete button is clicked"""
        # Get the bank name for this row
        bank_name = self.item.get('bank_name')
        
        if bank_name:
            # Call the server function to delete the bank from the database
            result = anvil.server.call('delete_bank', bank_name)
            
            # Refresh the parent form's repeating panel
            get_open_form().refresh_users()

            # Optionally, show an alert or notification
            alert(result)
        else:
            alert("Bank name not found.")

