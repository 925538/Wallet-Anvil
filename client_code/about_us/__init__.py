from ._anvil_designer import about_usTemplate
from anvil import *
import anvil.server

class about_us(about_usTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.card_1_copy.visible = False
    self.card_3_copy.visible = False
    self.card_5_copy.visible = False

  def link_8_click(self, **event_args):
    self.card_1_copy.visible = not self.card_1_copy.visible
    self.card_3_copy.visible = False
    self.card_5_copy.visible = False

  def link_13_click(self, **event_args):
    self.card_3_copy.visible = not self.card_3_copy.visible
    self.card_1_copy.visible = False
    self.card_5_copy.visible = False

  def link_15_click(self, **event_args):
    self.card_5_copy.visible = not self.card_5_copy.visible
    self.card_1_copy.visible = False
    self.card_3_copy.visible = False

  def link_16_click(self, **event_args):
    pass

  def button_3_click(self, **event_args):
    open_form('Login')