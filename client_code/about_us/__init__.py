from ._anvil_designer import about_usTemplate
from anvil import *
import anvil.server

class about_us(about_usTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('login')

  def home_click(self, **event_args):
    open_form('Home')

  def about_us_click(self, **event_args):
    open_form('about_us')

  def products_click(self, **event_args):
    open_form('product')

  def contact_click(self, **event_args):
    open_form('contact_us')

  def help_click(self, **event_args):
    open_form('help')

  def primary_color_1_click(self, **event_args):
    open_form('login')
