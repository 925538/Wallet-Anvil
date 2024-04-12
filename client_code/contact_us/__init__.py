from ._anvil_designer import contact_usTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class contact_us(contact_usTemplate):
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
    open_form('contact_us.issue_1')

  def link_3_click(self, **event_args):
    open_form('contact_us.issue_2')

  def link_4_click(self, **event_args):
    open_form('contact_us.issue_3')

  def link_5_click(self, **event_args):
    open_form('contact_us.issue_4')

