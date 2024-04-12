from ._anvil_designer import issue_4Template
from anvil import *
import anvil.server

class issue_4(issue_4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    open_form('contact_us')

  def button_3_click(self, **event_args):
    open_form('Login')

  def link_8_click(self, **event_args):
    open_form('Home')

  def link_16_click(self, **event_args):
    open_form('contact_us')
