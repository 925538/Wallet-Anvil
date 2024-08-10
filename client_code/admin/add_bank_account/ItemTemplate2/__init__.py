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

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the delete button is clicked"""
    # Get the row item for this button
    row = self.item
    # Delete the row from the database
    row.delete()
    # Refresh the parent form's repeating panel
    get_open_form().refresh_users()
