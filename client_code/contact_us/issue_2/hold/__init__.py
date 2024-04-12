from ._anvil_designer import holdTemplate
from anvil import *
import anvil.server

class hold(holdTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.card_3.visible = False
    self.card_5.visible = False

  def link_8_click(self, **event_args):
    open_form('Home')

  def link_13_click(self, **event_args):
    self.card_3.visible = not self.card_3.visible
    #self.card_1.visible = False
    self.card_5.visible = False

  def link_15_click(self, **event_args):
    self.card_5.visible = not self.card_5.visible
    #self.card_1.visible = False
    self.card_3.visible = False

  def link_16_click(self, **event_args):
    self.card_5.visible = False
    #self.card_1.visible = False
    self.card_3.visible = False
  def link_1_click(self, **event_args):
    open_form('contact_us.issue_2')

  def link_8_click(self, **event_args):
    open_form('Home')

  def link_16_click(self, **event_args):
    open_form('contact_us')

  def button_3_click(self, **event_args):
    open_form('Login')