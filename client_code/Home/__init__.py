from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.js.window
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# from anvil.Clock import Clock
class Home(HomeTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    anvil.server.call('update_active_status')
  def link_16_click(self, **event_args):
    pass

  def button_3_click(self, **event_args):
    open_form('signup')

  def button_1_click(self, **event_args):
    open_form('signup')

  def button_2_click(self, **event_args):
    open_form('signup')

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

  def button_4_click(self, **event_args):
    open_form('login')

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    facebook_link = "https://www.facebook.com"
    anvil.js.window.open(facebook_link)


  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    linkedin_link = "https://www.linkedin.com/company/ascend-defi-labs/"
    anvil.js.window.open(linkedin_link)


  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    instagram_link = "https://www.instagram.com/ascenddefi/"
    anvil.js.window.open(instagram_link)

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    twitter_link = "https://www.x.com"
    anvil.js.window.open(twitter_link)

  


