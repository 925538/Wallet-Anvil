from ._anvil_designer import transaction_monitoringTemplate
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

class transaction_monitoring(transaction_monitoringTemplate):
    def __init__(self, user=None, **properties):
        # Set Form properties and Data Bindings.
      self.init_components(**properties)
      self.user = user
      self.label_1.text=self.user['user_fullname']
      
      self.link11_clicked = True
      self.link12_clicked = False
      self.link13_clicked = False
      self.link14_clicked = False
      self.link15_clicked = False
      self.repeating_panel_items = []
      self.button1_clicked=True
      self.button3_clicked=True
      self.button2_clicked=True
      #users transactions all
      self.all_transactions()
      # Any code you write here will run before the form opens.
  
    def date_picker_1_change(self, **event_args):
      """This method is called when the selected date changes"""
      self.date_filter()
  
    def date_picker_2_change(self, **event_args):
      """This method is called when the selected date changes"""
      print(self.date_picker_2.date)
      self.date_filter()
    def all_transactions(self):
        try:
            # Fetch transactions from the server
            items = anvil.server.call('get_wallet_transactions')
            self.grouped_transactions = {}
            
            if items:
                for item in items:
                    # Extract date in YYYY-MM-DD format without time
                    date_str = item['transaction_timestamp'].strftime("%Y-%m-%d")
                    if date_str not in self.grouped_transactions:
                        self.grouped_transactions[date_str] = {'date': item['transaction_timestamp'], 'transactions': []}
                    self.grouped_transactions[date_str]['transactions'].append(item)
            else:
                return
            
            # Sort dates in descending order
            sorted_dates = sorted(self.grouped_transactions.keys(), reverse=True)
            
            # Create a list of dictionaries for repeating_panel_1
            self.repeating_panel_items = []
            for date_str in sorted_dates:
                date_info = self.grouped_transactions[date_str]
                for transaction in reversed(date_info['transactions']):
                    sender_phone = transaction['sender_mobile_number']
                    transaction_type = transaction['transaction_type']
                    fund = transaction['transaction_amount']
                    transaction_time = transaction['transaction_timestamp'].strftime("%I:%M %p")
                    profile_photo = '_/theme/account.png'  # Default profile photo
                    
                    # Fetch sender user data
                    sender_user = anvil.server.call('get_user_data', sender_phone)
                    # print(f"Fetched sender data: {sender_user}")  # Log sender data to the console
                    
                    if sender_user:
                        profile_photo = sender_user.get('user_profile_photo', '_/theme/account.png')
                        sender_username = sender_user.get('user_fullname', 'Unknown')
                    else:
                        sender_username = 'Unknown'
                    
                    # Determine fund display and color based on transaction type
                    fund_display, fund_color = self.get_fund_display_and_color(transaction_type, fund)
                    if transaction_type == 'withdrawn':
                      print(f"Transaction Status for Withdrawn: {transaction['transaction_status']}")
                    # Append transaction details for the sender
                    transaction_details = {
                        'date': date_info['date'].strftime("%Y-%m-%d"),
                        'fund': fund_display,
                        'transaction_status': transaction['transaction_status'],
                        'transaction_type': transaction_type,
                        'receiver_username': sender_username,
                        'currency_type': transaction['transaction_currency'],
                        'transaction_time': transaction_time,
                        'profile_photo': profile_photo,
                        'fund_color': fund_color
                    }
                    self.repeating_panel_items.append(transaction_details)
                    # print(f"Appended transaction for sender: {transaction_details}")  # Log the transaction details
                    
                    # Fetch receiver user data if applicable
                    receiver_phone = transaction.get('receiver_mobile_number')
                    if receiver_phone:
                        receiver_user = anvil.server.call('get_user_data', receiver_phone)
                        print(f"Fetched receiver data: {receiver_user}")  # Log receiver data to the console
                        
                        if receiver_user:
                            profile_photo = receiver_user.get('user_profile_photo', '_/theme/account.png')
                            receiver_username = receiver_user.get('user_fullname', 'Unknown')
                        else:
                            receiver_username = 'Unknown'
                        
                        # Update fund display and color if transaction is a credit
                        if transaction_type == 'Credit':
                            fund_display = "+" + str(fund)
                            fund_color = "green"
                        
                        # Append transaction details for the receiver
                        receiver_transaction_details = {
                            'date': date_info['date'].strftime("%Y-%m-%d"),
                            'fund': fund_display,
                            'transaction_status': transaction['transaction_status'],
                            'transaction_type': transaction_type,
                            'receiver_username': receiver_username,
                            'currency_type': transaction['transaction_currency'],
                            'transaction_time': transaction_time,
                            'profile_photo': profile_photo,
                            'fund_color': fund_color
                        }
                        self.repeating_panel_items.append(receiver_transaction_details)
                        # print(f"Appended transaction for receiver: {receiver_transaction_details}")  # Log the receiver transaction details
            
            # Bind the items to the repeating panel
            self.repeating_panel_1.items = self.repeating_panel_items
            # print("Repeating panel items set successfully.")  # Log when items are set
            
        except Exception as e:
            print(f"Error loading transactions: {e}")
    
    def get_fund_display_and_color(self, transaction_type, fund):
        """Helper function to determine the fund display and color."""
        if transaction_type in ['deposited', 'Auto Topup']:
            return "+" + str(fund), "green"
        elif transaction_type in ['Debit', 'withdrawn']:
            return "-" + str(fund), "red"
        else:
            return str(fund), "black"
      
    def link_11_click(self, **event_args):
      """This method is called when the link is clicked"""
      #all transactions linked
      """This method is called when the button is clicked"""
      self.link_11.foreground = '#148efe'
      self.link_12.foreground = 'black'
      self.link_13.foreground = 'black'
      self.link_14.foreground = 'black'
      self.link_15.foreground = 'black'
      self.link11_clicked = True
      self.link12_clicked = False
      self.link13_clicked = False
      self.link14_clicked = False
      self.link15_clicked = False
      all=[]
      for i in range(len(self.repeating_panel_items)):
        all.append({'date': self.repeating_panel_items[i]['date'],
                                            'fund': self.repeating_panel_items[i]['fund'],
                                            'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                            'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                            'currency_type':self.repeating_panel_items[i]['currency_type'],
                                            'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                            'profile_photo':self.repeating_panel_items[i]['profile_photo'],
                                            'transaction_type':self.repeating_panel_items[i]['transaction_type'],
                                            'fund_color': self.repeating_panel_items[i]['fund_color']})
      self.repeating_panel_1.items = all
  
    def link_12_click(self, **event_args):
      """This method is called when the link is clicked"""
      self.link_11.foreground = 'black'
      self.link_12.foreground = '#148efe'
      self.link_13.foreground = 'black'
      self.link_14.foreground = 'black'
      self.link_15.foreground = 'black'
      self.link11_clicked = False
      self.link12_clicked = True
      self.link13_clicked = False
      self.link14_clicked = False
      self.link15_clicked = False
      received=[]
      #all transactions that are received from 
      for i in range(len(self.repeating_panel_items)):
            if  self.repeating_panel_items[i]['transaction_type'] == 'Credit' :
              received.append({'date': self.repeating_panel_items[i]['date'],
                                                  'fund': self.repeating_panel_items[i]['fund'],
                                                  'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                  'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                  'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                  'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                  'transaction_type':self.repeating_panel_items[i]['transaction_type'],
                                                  'profile_photo':self.repeating_panel_items[i]['profile_photo'],
                                                  'fund_color': self.repeating_panel_items[i]['fund_color']})
      self.repeating_panel_1.items = received
  
  
    def link_13_click(self, **event_args):
    
      """This method is called when the button is clicked"""
      self.link_11.foreground = 'black'
      self.link_12.foreground = 'black'
      self.link_13.foreground = '#148efe'
      self.link_14.foreground = 'black'
      self.link_15.foreground = 'black'
      self.link11_clicked = False
      self.link12_clicked = False
      self.link13_clicked = True
      self.link14_clicked = False
      self.link15_clicked = False
      transfer=[]
      #all transactions that are transfered to
      for i in range(len(self.repeating_panel_items)):
            if  self.repeating_panel_items[i]['transaction_type'] == 'Debit' :
              transfer.append({'date': self.repeating_panel_items[i]['date'],
                                                  'fund': self.repeating_panel_items[i]['fund'],
                                                  'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                  'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                  'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                  'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                  'transaction_type':self.repeating_panel_items[i]['transaction_type'],
                                                  'profile_photo':self.repeating_panel_items[i]['profile_photo'],
                                                  'fund_color': self.repeating_panel_items[i]['fund_color']})
      self.repeating_panel_1.items = transfer
  
    def link_14_click(self, **event_args):
      """This method is called when the link is clicked"""
      
      self.link_11.foreground = 'black'
      self.link_12.foreground = 'black'
      self.link_13.foreground = 'black'
      self.link_14.foreground = '#148efe'
      self.link_15.foreground = 'black'
      self.link11_clicked = False
      self.link12_clicked = False
      self.link13_clicked = False
      self.link14_clicked = True
      self.link15_clicked = False
      withdraw=[]
      for i in range(len(self.repeating_panel_items)):
            if  self.repeating_panel_items[i]['transaction_type'] == 'withdrawn' :
              withdraw.append({'date': self.repeating_panel_items[i]['date'],
                                                  'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                  'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                  'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                  'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                  'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                  'profile_photo':self.repeating_panel_items[i]['profile_photo'],
                                                  'transaction_type':self.repeating_panel_items[i]['transaction_type'],
                                                  'fund_color': self.repeating_panel_items[i]['fund_color']})
      self.repeating_panel_1.items = withdraw
  
    def link_15_click(self, **event_args):
      """This method is called when the link is clicked"""
      self.link_11.foreground = 'black'
      self.link_12.foreground = 'black'
      self.link_13.foreground = 'black'
      self.link_14.foreground = 'black'
      self.link_15.foreground = '#148efe'
      self.link11_clicked = False
      self.link12_clicked = False
      self.link13_clicked = False
      self.link14_clicked = False
      self.link15_clicked = True
      deposit=[]
      for i in range(len(self.repeating_panel_items)):
            if  self.repeating_panel_items[i]['transaction_type'] == 'deposited' :
              deposit.append({'date': self.repeating_panel_items[i]['date'],
                                                  'fund':f"{self.repeating_panel_items[i]['fund']}",
                                                  'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                  'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                  'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                  'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                  'transaction_type':self.repeating_panel_items[i]['transaction_type'],
                                                  'profile_photo':self.repeating_panel_items[i]['profile_photo'],
                                                  'fund_color': self.repeating_panel_items[i]['fund_color']})
      self.repeating_panel_1.items = deposit
    
    def date_filter(self):
      transaction_type = ''
      if self.link12_clicked:
        transaction_type='Credit'
      elif self.link13_clicked:
        transaction_type = 'Debit'
      elif self.link14_clicked:
        transaction_type='Withdrawn'
      elif self.link15_clicked:
        transaction_type = 'Deposited'
      else:
        print('11 is clicked')
  
      currency=''
      if self.drop_down_2.selected_value in ['INR','USD','GBP','EUR']:
        currency=self.drop_down_2.selected_value
      print(len(currency))
      if currency=='':
        
        print('yes you are right')
      datee=[]
      only_date=[]
      if self.link11_clicked:
        if self.date_picker_1.date and self.date_picker_2.date : 
          datee=[]
          if currency == '':
            for i in range(len(self.repeating_panel_items)):
              if  str(self.date_picker_1.date.strftime("%Y-%m-%d")) <= str(self.repeating_panel_items[i]['date']) <= str(self.date_picker_2.date.strftime("%Y-%m-%d")):# and self.repeating_panel_items[i]['currency_type']==currency:
                datee.append({'date': self.repeating_panel_items[i]['date'],
                                                    'fund': self.repeating_panel_items[i]['fund'],
                                                    'transaction_type':self.repeating_panel_items[i]['transaction_type'],
                                                    'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                    'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                    'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                    'profile_photo':self.repeating_panel_items[i]['profile_photo'],
                                                    'fund_color': self.repeating_panel_items[i]['fund_color']})
            self.repeating_panel_1.items = datee
            
          if currency != '':
            datee=[]
            for i in range(len(self.repeating_panel_items)):
              if  str(self.date_picker_1.date.strftime("%Y-%m-%d")) <= str(self.repeating_panel_items[i]['date']) <= str(self.date_picker_2.date.strftime("%Y-%m-%d")):# and self.repeating_panel_items[i]['currency_type']==currency:
                datee.append({'date': self.repeating_panel_items[i]['date'],
                                                    'fund': self.repeating_panel_items[i]['fund'],
                                                    'transaction_type':self.repeating_panel_items[i]['transaction_type'],
                                                    'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                    'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                    'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                    'profile_photo':self.repeating_panel_items[i]['profile_photo'],
                                                    'fund_color': self.repeating_panel_items[i]['fund_color']})
            self.repeating_panel_1.items = datee
          
        elif self.date_picker_1.date :
          only_date=[]
          if currency == '':
            for i in range(len(self.repeating_panel_items)):
              if  str(self.date_picker_1.date.strftime("%Y-%m-%d")) == str(self.repeating_panel_items[i]['date']):# and self.repeating_panel_items[i]['currency_type']==currency :
                only_date.append({'date': self.repeating_panel_items[i]['date'],
                                                    'fund': self.repeating_panel_items[i]['fund'],
                                                    'transaction_type':self.repeating_panel_items[i]['transaction_type'],
                                                    'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                    'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                    'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                    'profile_photo':self.repeating_panel_items[i]['profile_photo'],
                                                    'fund_color': self.repeating_panel_items[i]['fund_color']})
            self.repeating_panel_1.items = only_date
  
          if currency != '':
            for i in range(len(self.repeating_panel_items)):
              if  str(self.date_picker_1.date.strftime("%Y-%m-%d")) == str(self.repeating_panel_items[i]['date']) and self.repeating_panel_items[i]['currency_type']==currency :
                only_date.append({'date': self.repeating_panel_items[i]['date'],
                                                    'fund': self.repeating_panel_items[i]['fund'],
                                                    'transaction_type':self.repeating_panel_items[i]['transaction_type'],
                                                    'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                    'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                    'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                    'profile_photo':self.repeating_panel_items[i]['profile_photo'],
                                                    'fund_color': self.repeating_panel_items[i]['fund_color']})
            self.repeating_panel_1.items = only_date
        else:
            print('None')
          
      #filtering by dates in all transactions 
      else:
        if (self.date_picker_1.date and self.date_picker_2.date)  : 
          datee=[]
          if currency == '':
            for i in range(len(self.repeating_panel_items)):
              if  str(self.date_picker_1.date.strftime("%Y-%m-%d")) <= str(self.repeating_panel_items[i]['date']) <= str(self.date_picker_2.date.strftime("%Y-%m-%d")) and self.repeating_panel_items[i]['transaction_type'] == transaction_type:# and self.repeating_panel_items[i]['currency_type']==currency:
                datee.append({'date': self.repeating_panel_items[i]['date'],
                                                    'fund': self.repeating_panel_items[i]['fund'],
                                                    'transaction_type':self.repeating_panel_items[i]['transaction_type'],
                                                    'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                    'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                    'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                    'profile_photo':self.repeating_panel_items[i]['profile_photo'],
                                                    'fund_color': self.repeating_panel_items[i]['fund_color']})
            self.repeating_panel_1.items = datee
          if  currency != '':
            datee=[]
            for i in range(len(self.repeating_panel_items)):
              if  str(self.date_picker_1.date.strftime("%Y-%m-%d")) <= str(self.repeating_panel_items[i]['date']) <= str(self.date_picker_2.date.strftime("%Y-%m-%d")) and self.repeating_panel_items[i]['currency_type']==currency and self.repeating_panel_items[i]['transaction_type'] == transaction_type:
                datee.append({'date': self.repeating_panel_items[i]['date'],
                                                    'fund': self.repeating_panel_items[i]['fund'],
                                                    'transaction_type':self.repeating_panel_items[i]['transaction_type'],
                                                    'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                    'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                    'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                    'profile_photo':self.repeating_panel_items[i]['profile_photo'],
                                                    'fund_color': self.repeating_panel_items[i]['fund_color']})
            self.repeating_panel_1.items = datee
          
        elif (self.date_picker_1.date):
          only_date=[]
          if currency == '':
            for i in range(len(self.repeating_panel_items)):
              if  str(self.date_picker_1.date.strftime("%Y-%m-%d")) == str(self.repeating_panel_items[i]['date']) and self.repeating_panel_items[i]['transaction_type'] == transaction_type: # and self.repeating_panel_items[i]['currency_type']==currency :
                only_date.append({'date': self.repeating_panel_items[i]['date'],
                                                    'fund': self.repeating_panel_items[i]['fund'],
                                                    'transaction_type':self.repeating_panel_items[i]['transaction_type'],
                                                    'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                    'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                    'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                    'profile_photo':self.repeating_panel_items[i]['profile_photo'],
                                                    'fund_color': self.repeating_panel_items[i]['fund_color']})
            self.repeating_panel_1.items = only_date
          
          if currency != '':
            only_date=[]
            for i in range(len(self.repeating_panel_items)):
              if  str(self.date_picker_1.date.strftime("%Y-%m-%d")) == str(self.repeating_panel_items[i]['date']) and self.repeating_panel_items[i]['currency_type']==currency and self.repeating_panel_items[i]['transaction_type'] == transaction_type:
                only_date.append({'date': self.repeating_panel_items[i]['date'],
                                                    'fund': self.repeating_panel_items[i]['fund'],
                                                    'transaction_type':self.repeating_panel_items[i]['transaction_type'],
                                                    'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                    'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                    'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                    'profile_photo':self.repeating_panel_items[i]['profile_photo'],
                                                    'fund_color': self.repeating_panel_items[i]['fund_color']})
            self.repeating_panel_1.items = only_date
        else:
            print('None')
  
    def drop_down_1_change(self, **event_args):
      transaction_type = ''
      if self.link12_clicked:
        transaction_type='Credit'
      elif self.link13_clicked:
        transaction_type = 'Debit'
      elif self.link14_clicked:
        transaction_type='Withdrawn'
      elif self.link15_clicked:
        transaction_type = 'Deposited'
      else:
        print('11 is clicked')
  
      currency=''
      if self.drop_down_2.selected_value in ['INR','USD','GBP','EUR']:
        currency=self.drop_down_2.selected_value
  
      """This method is called when an item is selected"""
      current_date = datetime.date.today()
      current_date_str = current_date.strftime("%Y-%m-%d")
      print(current_date)
      day=''
      if self.drop_down_1.selected_value in ['past 30 days','past 60 days','past 90 days']:
        if self.drop_down_1.selected_value == 'past 30 days':
          day=30
        elif self.drop_down_1.selected_value == 'past 60 days':
          day = 60
        elif self.drop_down_1.selected_value == 'past 90 days':
          day = 90
      #all transactions
      days=[]
      days_currency=[]
      if self.link11_clicked:
        if self.drop_down_1.selected_value in ['past 30 days','past 60 days','past 90 days'] and currency == '':
          days=[]
          past_days = current_date - datetime.timedelta(days=int(day))
          print(past_days)
          for i in range(len(self.repeating_panel_items)):
              if  str(past_days) <= str(self.repeating_panel_items[i]['date']) <= str(current_date_str):
                days.append({'date': self.repeating_panel_items[i]['date'],
                                                    'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                    'transaction_type':self.repeating_panel_items[i]['transaction_type'],
                                                    'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                    'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                    'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                    'profile_photo':self.repeating_panel_items[i]['profile_photo'],
                                                    'fund_color': self.repeating_panel_items[i]['fund_color']})
          self.repeating_panel_1.items = days
          
        elif self.drop_down_1.selected_value in ['past 30 days','past 60 days','past 90 days'] and currency != '':
          days_currency=[]
          past_days = current_date - datetime.timedelta(days=int(day))
          print(past_days)
          for i in range(len(self.repeating_panel_items)):
              if  str(past_days) <= str(self.repeating_panel_items[i]['date']) <= str(current_date_str) and (self.repeating_panel_items[i]['currency_type'] == currency) :
                days_currency.append({'date': self.repeating_panel_items[i]['date'],
                                                    'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                    'transaction_type':self.repeating_panel_items[i]['transaction_type'],
                                                    'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                    'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                    'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                    'profile_photo':self.repeating_panel_items[i]['profile_photo'],
                                                    'fund_color': self.repeating_panel_items[i]['fund_color']})
          self.repeating_panel_1.items = days_currency
        else:
          print('hey there')
      else:
        if self.drop_down_1.selected_value in ['past 30 days','past 60 days','past 90 days'] and currency == '':
          days=[]
          past_days = current_date - datetime.timedelta(days=int(day))
          print(past_days)
          for i in range(len(self.repeating_panel_items)):
              if  str(past_days) <= str(self.repeating_panel_items[i]['date']) <= str(current_date_str) and self.repeating_panel_items[i]['transaction_type'] == transaction_type:
                days.append({'date': self.repeating_panel_items[i]['date'],
                                                    'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                    'transaction_type':self.repeating_panel_items[i]['transaction_type'],
                                                    'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                    'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                    'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                    'profile_photo':self.repeating_panel_items[i]['profile_photo'],
                                                    'fund_color': self.repeating_panel_items[i]['fund_color']})
          self.repeating_panel_1.items = days
          
        elif self.drop_down_1.selected_value in ['past 30 days','past 60 days','past 90 days'] and currency != '':
          days_currency=[]
          past_days = current_date - datetime.timedelta(days=int(day))
          print(past_days)
          for i in range(len(self.repeating_panel_items)):
              if  str(past_days) <= str(self.repeating_panel_items[i]['date']) <= str(current_date_str) and (self.repeating_panel_items[i]['currency_type'] == currency) and self.repeating_panel_items[i]['transaction_type'] == transaction_type :
                days_currency.append({'date': self.repeating_panel_items[i]['date'],
                                                    'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                    'transaction_type':self.repeating_panel_items[i]['transaction_type'],
                                                    'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                    'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                    'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                    'profile_photo':self.repeating_panel_items[i]['profile_photo'],
                                                    'fund_color': self.repeating_panel_items[i]['fund_color']})
          self.repeating_panel_1.items = days_currency
        else:
          print('hey there')

    def drop_down_2_change(self, **event_args):
      """This method is called when an item is selected"""
      print(self.drop_down_2.selected_value)
      selected_value = self.drop_down_2.selected_value
      
      if selected_value == 'Select Days':
        print('yes none')
      else:
        self.currency_filter(selected_value)

    def currency_filter(self,currency):
      transaction_type = ''
      if self.link12_clicked:
        transaction_type='Credit'
      elif self.link13_clicked:
        transaction_type = 'Debit'
      elif self.link14_clicked:
        transaction_type='Withdrawn'
      elif self.link15_clicked:
        transaction_type = 'Deposited'
      else:
        print('11 is clicked')
      all=[]
      if self.link11_clicked:
          for i in range(len(self.repeating_panel_items)):
            if self.repeating_panel_items[i]['currency_type'] == currency:
              all.append({'date': self.repeating_panel_items[i]['date'],
                                                  'fund': self.repeating_panel_items[i]['fund'],
                                                  'transaction_type':self.repeating_panel_items[i]['transaction_type'],
                                                  'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                  'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                  'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                  'profile_photo':self.repeating_panel_items[i]['profile_photo'],
                                                  'fund_color': self.repeating_panel_items[i]['fund_color']}),
                                              
          self.repeating_panel_1.items = all
      else:
          for i in range(len(self.repeating_panel_items)):
            if self.repeating_panel_items[i]['currency_type'] == currency and self.repeating_panel_items[i]['transaction_type'] == transaction_type:
              all.append({'date': self.repeating_panel_items[i]['date'],
                                                  'fund': self.repeating_panel_items[i]['fund'],
                                                  'transaction_type':self.repeating_panel_items[i]['transaction_type'],
                                                  'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                  'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                  'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                  'profile_photo':self.repeating_panel_items[i]['profile_photo'],
                                                  'fund_color': self.repeating_panel_items[i]['fund_color']}),
                                              
          self.repeating_panel_1.items = all


    def button_clicked(self, **event_args):
      if self.button1_clicked:
        self.drop_down_2.visible = True
        self.button1_clicked = False
      else:
        self.drop_down_2.visible = False
        self.button1_clicked = True
  
      if self.button1_clicked and self.button2_clicked and self.button3_clicked:
        self.spacer_8.visible = False
        self.spacer_9.visible = False
      else:
        self.spacer_8.visible = True
        self.spacer_9.visible = True

    def button_2_click(self, **event_args):
      """This method is called when the button is clicked"""
      if self.button2_clicked:
        self.date_picker_1.visible = True
        self.date_picker_2.visible = True
        self.button2_clicked = False
      else:
        self.date_picker_1.visible = False
        self.date_picker_2.visible = False
        self.button2_clicked = True
  
      if self.button1_clicked and self.button2_clicked and self.button3_clicked:
        self.spacer_8.visible = False
        self.spacer_9.visible = False
      else:
        self.spacer_8.visible = True
        self.spacer_9.visible = True
  
    def button_3_click(self, **event_args):
      """This method is called when the button is clicked"""
      if self.button3_clicked:
        self.drop_down_1.visible = True
        self.button3_clicked=False
      else:
        self.drop_down_1.visible = False
        self.button3_clicked=True
  
      if self.button1_clicked and self.button2_clicked and self.button3_clicked:
        self.spacer_8.visible = False
        self.spacer_9.visible = False
      else:
        self.spacer_8.visible = True
        self.spacer_9.visible = True
  
    def link_1_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin', user=self.user)
    def link_2_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.report_analysis', user=self.user)

    def link_3_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.account_management', user=self.user)
    def link_4_click(self, **event_args):
        open_form('admin.admin_add_user',user=self.user)

    def link_5_click(self, **event_args):
        open_form('admin.add_currency',user=self.user)

    def link_6_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.audit_trail', user=self.user)

    def link_7_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('Login')

    def button_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      pass

    def link_16_click(self, **event_args):
      open_form("admin.transaction_monitoring",user = self.user)

    def link6_copy_click(self, **event_args):
      """This method is called when the link is clicked"""
      pass

    def link6_copy_2_click(self, **event_args):
      if self.user['user_type'] == 'super_admin':
          # Open the admin creation form
          open_form("admin.create_admin", user=self.user)
      else:
          # Show an alert if the user is not a super admin
          alert("You're not a super admin. Only super admins can perform this action.")

    def link6_copy_3_click(self, **event_args):
      open_form("admin.user_support",user = self.user)

    def link6_copy_4_click(self, **event_args):
     open_form("admin.add_bank_account",user = self.user)