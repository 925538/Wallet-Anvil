from ._anvil_designer import auto_topupTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
import anvil.http
from datetime import timezone, timedelta
class auto_topup(auto_topupTemplate):
    def __init__(self,user=None, **properties):
        # Initialize self.user as a dictionary
      self.init_components(**properties)
      self.user = user
      # Set Form properties and Data Bindings.
      username = anvil.server.call('get_username', self.user['users_phone'])
      #self.label_1.text = f"Welcome to Green Gate Financial, {username}"
      currencies = anvil.server.call('get_user_currency', self.user['users_phone'])
      self.drop_down_2.items= [str(row['users_balance_currency_type']) for row in currencies]
      self.display()
      self.card_2.visible =False
      self.button_5.visible=False
      self.label_4.visible=False
      self.card_3.visible = False
      self.button_6.visible= False
      self.label_5.visible=False
      self.button_off_visible = False
      self.button_on_visible= False
      if self.user['users_auto_topup'] is True:
        self.button_on.visible= False
      else:
        self.button_off.visible= False
        
    def display(self, **event_args):
        acc = self.drop_down_1.selected_value

    def button_1_click(self, **event_args):
      self.text_box_1.text = 100

    def button_2_click(self, **event_args):
      self.text_box_1.text = 200

    def button_3_click(self, **event_args):
      self.text_box_1.text = 500

    def button_4_click(self, **event_args):
      self.text_box_1.text = 1000

    def button_13_click(self, **event_args):
      self.text_box_2.text = 100

    def button_14_click(self, **event_args):
      self.text_box_2.text = 200

    def button_15_click(self, **event_args):
      self.text_box_2.text = 500
      
    def button_16_click(self, **event_args):
      self.text_box_2.text = 1000

    def button_5_click(self, **event_args):
      if self.user['users_auto_topup'] is True:
        if self.user['users_minimum_topup'] is True:
            current_datetime = datetime.now()
            w_bal = self.drop_down_1.selected_value
            cur= self.drop_down_2.selected_value
            money = float(self.text_box_1.text)
            endpoint = 'convert'
            api_key = 'a2qfoReWfa7G3GiDHxeI1f9BFXYkZ2wT'
            # Set base currency and any other parameters 
            base_currency = 'INR'
            resp = anvil.http.request(f"https://api.currencybeacon.com/v1/{endpoint}?from={base_currency}&to={cur}&amount={money}&api_key={api_key}", json=True)
            money_value=resp['response']['value']
            if money >0:
              if self.user :
                # Check if a balance row already exists for the user
                existing_balance = app_tables.wallet_users_balance.get(users_balance_phone=self.user['users_phone'],users_balance_currency_type=cur) 
                if existing_balance['users_balance'] < int(w_bal):
                  self.user['users_minimum_topup'] = True
                  
                  self.user['users_minimum_topup_amount_below']=int(self.drop_down_1.selected_value)
                  self.user['users_minimum_topup_amount'] = int(self.text_box_1.text)
                  self.user['users_auto_topup_expiry_date'] = self.date_picker_1.date
                  
                  existing_balance['users_balance'] += money_value
                  
                  new_transaction = app_tables.wallet_users_transaction.add_row(
                        users_transaction_phone=self.user['users_phone'],
                        users_transaction_fund=money_value,
                        users_transaction_date=current_datetime,
                        users_transaction_currency=cur,
                        users_transaction_type="Auto Topup",
                        users_transaction_status="Minimum-Topup",
                        users_transaction_receiver_phone=self.user['users_phone']
                    )
                  #self.label_4.text = "Minimum-topup payment has been successfully added to your account."
                  alert("minimum topup is added.")
                  self.text_box_1.text = ""
                  print("minimum topup added.") 
                  #open_form('customer_page', user=self.user)
                else:
                  # No minimum top-up required
                  self.user['users_minimum_topup'] = True
                  self.user['users_minimum_topup_amount_below']=int(self.drop_down_1.selected_value)
                  self.user['users_minimum_topup_amount'] = int(self.text_box_1.text)
                  self.user['users_auto_topup_expiry_date'] = self.date_picker_1.date
                  anvil.alert("minimum topup is added.")
                  # print("Your balance is not below the limit")
                  # open_form('customer', user=self.user)
              else:
                self.label_4.text = "Error: No matching accounts found for the user or invalid account number."
                #open_form('customer', user=self.user)
            else:
              alert(f"topup amount must be atleast 1{cur}")
        else:
          alert("Please enable the minimum auto-topup switch to proceed.")
      else:
        alert("Please enable the auto-topup switch to proceed.")
      
    def button_6_click(self, **event_args):
      
      phone = self.user['users_phone']
      details = app_tables.wallet_users.get(users_phone=phone)
      if details['users_auto_topup'] == True:
          if details['users_timely_autotopup'] == True:  
              frequency = self.drop_down_3.selected_value
              if frequency == "Every Week":
                  interval_days = 7
              elif frequency == "Every Month":
                  interval_days = 30 
              elif frequency == "Every 3 Months":
                  interval_days = 90  
              elif frequency == "Every 6 Months":
                  interval_days = 180  
              else:
                  interval_days = 0 
      
              now = datetime.now()
              next_topup = now + timedelta(days=interval_days)
              money = float(self.text_box_2.text)
              topup_expiry_date = self.date_picker_2.date
      
      
              phone = self.user['users_phone']
              details = app_tables.wallet_users.get(users_phone=phone)
      
      
              phone = self.user['users_phone']
      
              user = app_tables.wallet_users.get(users_phone=phone)
              user['users_timely_topup_duration'] = str(interval_days)
              user['users_timely_topup_amount'] = int(money)
              user['users_timely_topup_expiry_date'] = topup_expiry_date
              user.update()
              alert("timely topup is added.")
        
          else:
            alert("Please enable the timely auto-topup switch to proceed.")
            
      else:
            alert("Please enable the auto-topup switch to proceed.")
            
      

      # if self.user['users_auto_topup']== True:
      #   from datetime import datetime, timezone
      #   current_datetime = datetime.now().replace(tzinfo=timezone.utc)
      #   frequency = self.drop_down_3.selected_value
      #   cur= self.drop_down_2.selected_value
      #   money = float(self.text_box_2.text)
      #   endpoint = 'convert'
      #   api_key = 'a2qfoReWfa7G3GiDHxeI1f9BFXYkZ2wT'
      #   # Set base currency and any other parameters 
      #   base_currency = 'INR'
      #   resp = anvil.http.request(f"https://api.currencybeacon.com/v1/{endpoint}?from={base_currency}&to={cur}&amount={money}&api_key={api_key}", json=True)
      #   money_value=resp['response']['value']
      #   print(f"Your entered amount is {money_value}")
      #   if self.user :
      #     # Check if a balance row already exists for the user
      #     existing_balance = app_tables.wallet_users_balance.get(users_balance_phone=self.user['users_phone'],users_balance_currency_type=cur)         
          
      #     # Calculate the time interval based on the frequency
      #     if frequency == "Every Week":
      #         interval_days = 7
      #     elif frequency == "Every Month":
      #         interval_days = 30 
      #     elif frequency == "Every 3 Months":
      #         interval_days = 90  
      #     elif frequency == "Every 6 Months":
      #         interval_days = 180  
      #     else:
      #         interval_days = 0 
          
      #     # Check if the required time duration has elapsed or if the frequency is different
      #     if (self.user['last_auto_topup_time'] is None) or ((current_datetime - self.user['last_auto_topup_time']).days >= interval_days):
      #       self.user['users_timely_topup'] = True
      #       self.user['users_timely_topup_interval'] = frequency
      #       existing_balance['balance'] += money_value
      #       new_transaction = app_tables.wallet_users_transaction.add_row(
      #             users_transaction_phone=self.user['users_phone'],
      #             users_transaction_fund=money_value,
      #             users_transaction_date=current_datetime,
      #             users_transaction_type="Auto Topup",
      #             users_transaction_status="Timely-Topup",
      #             users_transaction_currency=cur,
      #             users_transaction_receiver_phone=self.user['users_phone']
      #         )
      #       self.label_5.text = f"{frequency}-topup payment has been successfully added to your account."
      #       # Update the last auto-topup time in user data
      #       self.user['users_last_auto_topup_time'] = current_datetime
      #       open_form('customer', user=self.user)  
      #     else:
      #       self.user['users_auto_topup'] = False
      #       anvil.alert("Auto-topup is inactive until the required time duration has expired.")
      #       print("Your balance is not below the limit")
      #       open_form('customer', user=self.user)  
      #   else:
      #     self.label_5.text = "Error: No matching accounts found for the user or invalid account number."
      # else:
      #   alert("Please enable the auto-topup switch to proceed.")    
        
    def button_off_click(self, **event_args):
      self.user['users_auto_topup']= False
      self.user.update()
      self.button_on.visible = True
      self.button_off.visible = False
  
    def button_on_click(self, **event_args):
      self.user['users_auto_topup']= True
      self.user.update()
      self.button_on.visible = False
      self.button_off.visible = True
      self.minimum_balance_topup.visible=True
      self.timely_topup.visible=True
      self.card_2.visible = False
      self.button_5.visible = False
      self.label_4.visible= False
      self.card_3.visible = False
      self.button_6.visible = False
      self.label_5.visible=False
      self.timely_topup.enabled=True
      self.minimum_balance_topup.enabled=True
     
    def link_1_click(self, **event_args):
      open_form('customer',user=self.user)

    def minimum_balance_topup_click(self, **event_args):
          if self.user['users_minimum_topup']:
            self.button_off_copy.visible = True
            self.button_on_copy.visible = False
          else:
            self.button_on_copy.visible = True
            self.button_off_copy.visible = False
          self.minimum_balance_topup.enabled=True
          self.timely_topup.enabled=False
          self.card_2.visible = True
          self.button_5.visible = True
          self.label_4.visible= True
          self.card_3.visible = False
          self.button_6.visible = False
          self.label_5.visible=False

    def timely_topup_click(self, **event_args):
      if self.user['users_timely_autotopup']:
        self.button_off_copy_2.visible = True
        self.button_on_copy_2.visible = False
      else:
        self.button_on_copy_2.visible = True
        self.button_off_copy_2.visible = False
      self.timely_topup.enabled=True
      self.minimum_balance_topup.enabled=False
      self.card_3.visible = True
      self.button_6.visible = True
      self.label_5.visible= True
      self.card_2.visible = False
      self.button_5.visible = False
      self.label_4.visible= False

    def link_2_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.walletbalance",user=self.user)

    def link_3_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.transactions',user=self.user)

    def link_4_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.transfer',user=self.user)

    def link_7_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.Viewprofile',user=self.user)

    def link_13_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("Home")

    def link_10_click(self, **event_args):
      open_form('customer.deposit',user=self.user)

    def link_5_click(self, **event_args):
      open_form('customer.withdraw',user=self.user)

    def link_8_click(self, **event_args):
      open_form('customer.settings',user=self.user)

    def link_5_withdraw_click(self, **event_args):
     open_form('customer.withdraw',user=self.user)


      

    def help_click(self, **event_args):
      open_form("help",user = self.user)

    def link_8_copy_2_click(self, **event_args):
      """This method is called when the link is clicked"""
      pass

    def add_bank_click(self, **event_args):
        open_form("customer.wallet",user = self.user)

    

    def text_box_1_change(self, **event_args):
      """This method is called when the text in this text box is edited"""
      user_input = self.text_box_1.text
      print("Raw input:", user_input)
      
      allowed_characters = "0123456789."
  
      # Filter out any invalid characters and allow only one decimal point
      filtered_text = ''
      decimal_point_count = 0
      
      for char in user_input:
        if char in allowed_characters:
          if char == '.':
            decimal_point_count += 1
            if decimal_point_count > 1:
              continue
          filtered_text += char
  
      # Allow empty string and string with just a decimal point
      if filtered_text == '' or filtered_text == '.':
        self.text_box_1.text = filtered_text
        return
  
      try:
        processed_value = self.process_input(filtered_text)
        self.text_box_1.text = processed_value
      except ValueError:
        self.text_box_1.text = filtered_text
  
    def process_input(self, user_input):
      # Check if the input ends with a decimal point
      if user_input.endswith('.'):
        return user_input
      
      value = float(user_input)
      
      if value.is_integer():
        # If it's an integer, format without decimals
        formatted_value = '{:.0f}'.format(value)
      else:
        # If it's a float, format with significant digits
        formatted_value = '{:.15g}'.format(value)
  
      return formatted_value

    def button_off_copy_click(self, **event_args):
      self.user['users_minimum_topup']= False
      self.user.update()
      self.button_off_copy.visible = False
      self.button_on_copy.visible = True
          

    def button_on_copy_click(self, **event_args):
      self.user['users_minimum_topup']= True
      self.user.update()
      self.button_on_copy.visible = False
      self.button_off_copy.visible = True

    def switch_on_timely_topup(self, **event_args):
      self.user['users_timely_autotopup']= False
      self.user.update()
      self.button_off_copy_2.visible = False
      self.button_on_copy_2.visible = True
      
    def switch_off_timely_topup(self, **event_args):
      self.user['users_timely_autotopup']= True
      self.user.update()
      self.button_off_copy_2.visible = True
      self.button_on_copy_2.visible = False

   
 
