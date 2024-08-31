from ._anvil_designer import ItemTemplate13Template
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime


class ItemTemplate13(ItemTemplate13Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.label_1.text = self.item['receiver_username']
    self.label_5.text = f"at {self.item['transaction_time']}"
    
    #date string
    try:
    # Parse the date string
      date_obj = datetime.datetime.strptime(self.item['date'], "%Y-%m-%d")
      date_string = f"{date_obj.day} {date_obj.strftime('%B')} {date_obj.year}"
      self.label_2.text = date_string
    except Exception as e:
      print("Invalid date format. Please use DD-MM-YYYY.")
      print(e)
      return None

    #time string
    
    
    
    try:
      print(self.item['fund'])
      if int(self.item['fund']) :
        self.label_3.text = f"{self.item['fund']}"          
    except Exception as e:
      print(e)
      try:
        print(self.item['fund'])
        if float(self.item['fund']):
          
          self.label_3.text = f"{float(self.item['fund']):.2f}"
      except Exception as e:
        print(e)
    # self.label_3.icon = f"fa:{self.item['currency_type'].lower()}"
    # self.label_3.foreground = self.item['fund_color']
    if self.item['currency_type'] is not None:
      self.label_3.icon = f"fa:{self.item['currency_type'].lower()}"
    else:
      self.label_3.icon = "fa:default-icon"  # Set a default icon or handle the case where currency_type is None

    self.label_3.foreground = self.item.get('fund_color', 'default-color')  # Default color if fund_color is not provided
    
    
    if self.item['transaction_type'] == 'Debit':
      self.label_4.text = 'Transfer'
    if self.item['transaction_type'] == 'Credit':
      self.label_4.text = 'Received'
    if self.item['transaction_type'] == 'Deposited':
      self.label_4.text='Topup'
    if self.item['transaction_type'] == 'Withdrawn':
      self.label_4.text = 'Withdraw'
    if self.item['transaction_type'] == 'Auto Topup':
      self.label_4.text = 'Auto Topup'
    self.label_4.foreground = self.item['fund_color']

    self.image_1.source = self.item['profile_photo']

    # Any code you write here will run before the form opens.
