from ._anvil_designer import ItemTemplate4Template
from anvil import *
import anvil.server

class ItemTemplate4(ItemTemplate4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
