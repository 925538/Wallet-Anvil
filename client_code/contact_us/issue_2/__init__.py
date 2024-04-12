from ._anvil_designer import issue_2Template
from anvil import *
import anvil.server

class issue_2(issue_2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    open_form('contact_us')

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def button_3_click(self, **event_args):
    open_form('Login')

  def link_8_click(self, **event_args):
    open_form('Home')

  def link_16_click(self, **event_args):
    open_form('contact_us')
