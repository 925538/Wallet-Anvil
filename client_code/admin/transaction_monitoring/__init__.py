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
      self.label_1.text=self.user['users_username']
      
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
      items = anvil.server.call('get_wallet_transactions')
      self.grouped_transactions = {}
      print('yes')
      if items:
        for item in items:
            print('yes1')
            # Extract date in YYYY-MM-DD format without time
            date_str = item['users_transaction_date'].strftime("%Y-%m-%d")
            if date_str not in self.grouped_transactions:
                self.grouped_transactions[date_str] = {'date': item['users_transaction_date'], 'transactions': []}
            self.grouped_transactions[date_str]['transactions'].append(item)
      else:
        return
  
      # Sort dates in descending order
      sorted_dates = sorted(self.grouped_transactions.keys(), reverse=True)
  
      # Create a list of dictionaries for repeating_panel_1
      # repeating_panel_items = []
      for date_str in sorted_dates:
          date_info = self.grouped_transactions[date_str]
          for transaction in reversed(date_info['transactions']):
              sender_phone=transaction['users_transaction_phone']
              sender_type=transaction['users_transaction_type']
              fund = transaction['users_transaction_fund']
              # transaction_type = transaction['users_transaction_type']
              # transaction_type=''
              # if sender_type=='Debit':
              #   transaction_type='Debit'
              # elif transaction['users_transaction_receiver_phone'] == current_user and transaction['users_transaction_receiver_type']=='Credit':
              #   transaction_type='Credit' 
              # elif transaction['users_transaction_phone'] == current_user and transaction['users_transaction_type']=='Withdrawn':
              #   transaction_type='Withdrawn'
              # elif transaction['users_transaction_phone'] == current_user and transaction['users_transaction_type']=='Deposited':
              #   transaction_type='Deposited'
              # elif transaction['users_transaction_phone'] == current_user and transaction['users_transaction_type']=='Auto Topup':
              #   transaction_type='Auto Topup'
                
              transaction_time = transaction['users_transaction_date'].strftime("%I:%M %p")
              profile_pic = '_/theme/account.png'
            
              if sender_type == 'Withdrawn' or sender_type == 'Deposited' or sender_type == 'Auto Topup':
                sent_userr = app_tables.wallet_users.get(users_phone=sender_phone)
                if sent_userr:
                  if sent_userr['users_profile_pic'] is not None:
                    profile_pic = sent_userr['users_profile_pic'] 
                  else:
                    profile_pic = '_/theme/account.png'
                    
              # if  transaction_type == 'Credit' : 
              #   trans_user = app_tables.wallet_users.get(users_phone = current_user)
              #   if trans_user :
              #     if trans_user['users_profile_pic'] is not None:
              #       profile_pic = trans_user['users_profile_pic'] 
              #     else:
              #       profile_pic = '_/theme/account.png'

              if sender_type == 'Debit':
                trans_user = app_tables.wallet_users.get(users_phone = sender_phone)
                if trans_user :
                  if trans_user['users_profile_pic'] is not None:
                    profile_pic = trans_user['users_profile_pic'] 
                  else:
                    profile_pic = '_/theme/account.png'
              # Fetch username from wallet_user table using receiver_phone
              sent_username=''
              if  sender_type == 'Debit' : 
                  _user = app_tables.wallet_users.get(users_phone=sender_phone)
                  sent_username = _user['users_username']
              # elif (transaction['users_transaction_receiver_phone']==current_user and transaction['users_transaction_receiver_type'] == 'Credit') :
              #     receiver_user = app_tables.wallet_users.get(users_phone=transaction['users_transaction_phone'])
              #     receiver_username = receiver_user['users_username']
              else:
                  _user = app_tables.wallet_users.get(users_phone=sender_phone)
                  sent_username = _user['users_username']
              
              if sender_type == 'Deposited' or sender_type == 'Auto Topup': # transaction_type == 'Credit' or transaction_type
                  fund_display = "+" + str(fund)
                  fund_color = "green"
              elif sender_type == 'Debit' or sender_type == 'Withdrawn':
                  fund_display = "-" + str(fund)
                  fund_color = "red"
              else:
                  fund_display = str(fund)
                  fund_color = "black"
              
              # Append transaction details with username instead of receiver_phone
              self.repeating_panel_items.append({'date': date_info['date'].strftime("%Y-%m-%d"),
                                              'fund': fund_display,
                                              'transaction_status': transaction['users_transaction_status'],
                                              'transaction_type':transaction['users_transaction_type'],
                                              'receiver_username': sent_username,
                                              'currency_type':transaction['users_transaction_currency'],
                                              'transaction_time':transaction_time,
                                              'profile_pic':profile_pic,
                                              'fund_color': fund_color})


      #for credits
              
              receiver=transaction['users_transaction_receiver_phone']
              receiver_type=transaction['users_transaction_receiver_type']
              # sender_phone=transaction['users_transaction_phone']
              # sender_type=transaction['users_transaction_type']
              # fund = transaction['users_transaction_fund']
              # transaction_type = transaction['users_transaction_type']
              # transaction_type=''
              # if sender_type=='Debit':
              #   transaction_type='Debit'
              # elif transaction['users_transaction_receiver_phone'] == current_user and transaction['users_transaction_receiver_type']=='Credit':
              #   transaction_type='Credit' 
              # elif transaction['users_transaction_phone'] == current_user and transaction['users_transaction_type']=='Withdrawn':
              #   transaction_type='Withdrawn'
              # elif transaction['users_transaction_phone'] == current_user and transaction['users_transaction_type']=='Deposited':
              #   transaction_type='Deposited'
              # elif transaction['users_transaction_phone'] == current_user and transaction['users_transaction_type']=='Auto Topup':
              #   transaction_type='Auto Topup'
                
              # receiver_phone = transaction['users_transaction_receiver_phone']
              # transaction_time = transaction['users_transaction_date'].strftime("%I:%M %p")
              # profile_pic = '_/theme/account.png'
            
              # if sender_type == 'Withdrawn' or sender_type == 'Deposited' or sender_type == 'Auto Topup':
              #   userr = app_tables.wallet_users.get(users_phone=sender_phone)
              #   if userr:
              #     if userr['users_profile_pic'] is not None:
              #       profile_pic = userr['users_profile_pic'] 
              #     else:
              #       profile_pic = '_/theme/account.png'
                    
              # if receiver_type == 'Credit' :
              print('coming inside')
              if receiver_type == 'Credit':
                received_user = app_tables.wallet_users.get(users_phone = receiver)
                if received_user :
                  if received_user['users_profile_pic'] is not None:
                    profile_pi = received_user['users_profile_pic'] 
                  else:
                    profile_pi = '_/theme/account.png'
  
                # if sender_type == 'Debit':
                #   trans_user = app_tables.wallet_users.get(users_phone = transaction['users_transaction_receiver_phone'])
                #   if trans_user :
                #     if trans_user['users_profile_pic'] is not None:
                #       profile_pic = trans_user['users_profile_pic'] 
                #     else:
                #       profile_pic = '_/theme/account.png'
                # Fetch username from wallet_user table using receiver_phone
                # received_username=''
                # if  sender_type == 'Debit' : 
                money_sent_user = app_tables.wallet_users.get(users_phone=receiver)
                received_username = money_sent_user['users_username']
                # elif (transaction['users_transaction_receiver_phone']==current_user and transaction['users_transaction_receiver_type'] == 'Credit') :
                #     receiver_user = app_tables.wallet_users.get(users_phone=transaction['users_transaction_phone'])
                #     receiver_username = receiver_user['users_username']
                
                
                if receiver_type == 'Credit' :
                    fund_display = "+" + str(fund)
                    fund_color = "green"
                else:
                    fund_display = str(fund)
                    fund_color = "black"
                
                # Append transaction details with username instead of receiver_phone
                self.repeating_panel_items.append({'date': date_info['date'].strftime("%Y-%m-%d"),
                                                'fund': fund_display,
                                                'transaction_status': transaction['users_transaction_status'],
                                                'transaction_type':receiver_type,
                                                'receiver_username': received_username,
                                                'currency_type':transaction['users_transaction_currency'],
                                                'transaction_time':transaction_time,
                                                'profile_pic':profile_pi,
                                                'fund_color': fund_color})
                print('appended')
  
      self.repeating_panel_1.items = self.repeating_panel_items
      
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
                                            'profile_pic':self.repeating_panel_items[i]['profile_pic'],
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
                                                  'profile_pic':self.repeating_panel_items[i]['profile_pic'],
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
                                                  'profile_pic':self.repeating_panel_items[i]['profile_pic'],
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
            if  self.repeating_panel_items[i]['transaction_type'] == 'Withdrawn' :
              withdraw.append({'date': self.repeating_panel_items[i]['date'],
                                                  'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                  'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                  'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                  'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                  'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                  'profile_pic':self.repeating_panel_items[i]['profile_pic'],
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
            if  self.repeating_panel_items[i]['transaction_type'] == 'Deposited' :
              deposit.append({'date': self.repeating_panel_items[i]['date'],
                                                  'fund':f"{self.repeating_panel_items[i]['fund']}",
                                                  'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                  'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                  'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                  'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                  'transaction_type':self.repeating_panel_items[i]['transaction_type'],
                                                  'profile_pic':self.repeating_panel_items[i]['profile_pic'],
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
                                                    'profile_pic':self.repeating_panel_items[i]['profile_pic'],
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
                                                    'profile_pic':self.repeating_panel_items[i]['profile_pic'],
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
                                                    'profile_pic':self.repeating_panel_items[i]['profile_pic'],
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
                                                    'profile_pic':self.repeating_panel_items[i]['profile_pic'],
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
                                                    'profile_pic':self.repeating_panel_items[i]['profile_pic'],
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
                                                    'profile_pic':self.repeating_panel_items[i]['profile_pic'],
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
                                                    'profile_pic':self.repeating_panel_items[i]['profile_pic'],
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
                                                    'profile_pic':self.repeating_panel_items[i]['profile_pic'],
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
                                                    'profile_pic':self.repeating_panel_items[i]['profile_pic'],
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
                                                    'profile_pic':self.repeating_panel_items[i]['profile_pic'],
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
                                                    'profile_pic':self.repeating_panel_items[i]['profile_pic'],
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
                                                    'profile_pic':self.repeating_panel_items[i]['profile_pic'],
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
                                                  'profile_pic':self.repeating_panel_items[i]['profile_pic'],
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
                                                  'profile_pic':self.repeating_panel_items[i]['profile_pic'],
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
      if self.user['users_usertype'] == 'super_admin':
          # Open the admin creation form
          open_form("admin.create_admin", user=self.user)
      else:
          # Show an alert if the user is not a super admin
          alert("You're not a super admin. Only super admins can perform this action.")

    def link6_copy_3_click(self, **event_args):
      open_form("admin.user_support",user = self.user)

    def link6_copy_4_click(self, **event_args):
     open_form("admin.add_bank_account",user = self.user)
    

    
    

    

    

    

    

    

  
