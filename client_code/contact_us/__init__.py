from ._anvil_designer import contact_usTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .issue_1 import issue_1
# from .issue_2 import issue_2
from .issue_3 import issue_3
from .issue_4 import issue_4
from .issue_5 import issue_5

class contact_us(contact_usTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    
    self.tabs={
      "Tab 1":issue_1(),
      # "Tab 2":issue_2(),
      "Tab 3":issue_3(),
      "Tab 4":issue_4(),
      "Tab 5":issue_5()
    }
 
    self.button_1.set_event_handler('click', lambda **event_args: self.switch_tab("Tab 1"))
    # self.button_2.set_event_handler('click', lambda **event_args: self.switch_tab("Tab 2"))
    self.button_3.set_event_handler('click', lambda **event_args: self.switch_tab("Tab 3"))
    self.button_6.set_event_handler('click', lambda **event_args: self.switch_tab("Tab 4"))
    self.button_5.set_event_handler('click', lambda **event_args: self.switch_tab("Tab 5"))




    # self.button_1.set_event_handler('mouse_leave', lambda **event_args: self.mouse_leave_change_background_color())

    self.switch_tab("Tab 1")


  def mouse_enter_change_background_color(self):
    self.button_1.background = "#4CAF50"

  def mouse_leave_change_background_color(self):
    pass
  
  def switch_tab(self,tab_name):
    self.card.clear()
    self.card.add_component(self.tabs[tab_name])


  def set_card_overflow(self, **event_args):
    """This method sets the card's overflow to hidden"""
    self.card_1.role = "overflow-hidden"
    
  def link_8_click(self, **event_args):
    open_form('Home')

  def link_1_click(self, **event_args):
    open_form('contact_us.issue_1')

  def link_3_click(self, **event_args):
    open_form('contact_us.issue_2')

  def link_4_click(self, **event_args):
    open_form('contact_us.issue_3')

  def link_5_click(self, **event_args):
    open_form('contact_us.issue_4')

  def home_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Home')

  def about_us_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('about_us')

  def products_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('product')

  def help_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('help')

  def button_6_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def button_3_show(self, **event_args):
    """This method is called when the Button is shown on the screen"""
    pass

  def button_5_click(self, **event_args):
    open_form("contact_us.issue_5")

  def button_4_click(self, **event_args):
    open_form("login")
