from ._anvil_designer import customerTemplate
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime
# from datetime import datetime
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
from datetime import  timedelta

import time
        
class customer(customerTemplate):
    def __init__(self, user=None, password=None, **properties):
        # Initialize the form
        self.init_components(**properties)
        
        self.user = user
       
        self.timer_1.interval = 60
        self.timer_1.enabled = True
        
        self.password = password
        self.link_clicked = True  # changed
        self.notifications()
        user_dict = dict(self.user)
        self.refresh_data()
        self.get_credit_debit_details()
        print(user_dict)
        self.check_profile_pic()
        self.greet_based_on_time()

        # Assuming user has a 'phone' attribute
        phone_number = user_dict.get('users_phone', None)
        default_currency = 'INR'
        users_def_currency = app_tables.wallet_users.get(users_phone=self.user['users_phone'])
        if users_def_currency['users_defaultcurrency'] is not None:
            default_currency = users_def_currency['users_defaultcurrency']

        if phone_number:
            # Search transactions based on the user's phone number
            items = app_tables.wallet_users_transaction.search(
                q.any_of(
                    users_transaction_phone=self.user['users_phone'],
                    users_transaction_receiver_phone=self.user['users_phone']
                ), users_transaction_currency=default_currency
            )

            # Sort transactions by date in descending order
            sorted_transactions = sorted(items, key=lambda x: x['users_transaction_date'], reverse=True)

            # Check if there are any transactions
            if not sorted_transactions:
                self.repeating_panel_2.items = [{
                    'fund': "",
                    'receiver_username': "You're a new user, make some activity!",
                    'transaction_text': "",
                    'transaction_time': "",
                    'fund_color': "black"
                }]
                self.spacer_2.height = 293.34112548828125
            else:
                # Process transactions as before
                self.repeating_panel_2_items = []
                max_history_entries = 4  # Maximum number of history entries to display
                for transaction in sorted_transactions:
                    fund = transaction['users_transaction_fund']
                    receiver_phone = transaction['users_transaction_receiver_phone']
                    transaction_time = transaction['users_transaction_date'].strftime("%a-%I:%M %p")  # Concatenate day with time (e.g., Mon-06:20 PM)
                    profile_pic = '_/theme/account.png'

                    if (transaction['users_transaction_type'] == 'Withdrawn' or
                        transaction['users_transaction_type'] == 'Deposited' or
                        transaction['users_transaction_type'] == 'Auto Topup') and transaction['users_transaction_phone'] == self.user['users_phone']:
                        bank_name = transaction['users_transaction_bank_name']
                        bank_record = app_tables.wallet_admins_add_bank.get(admins_add_bank_names=bank_name)
                        if bank_record:
                            profile_pic = bank_record['admins_add_bank_icons']
                        else:
                            profile_pic = '_/theme/account.png'
                    
                    if transaction['users_transaction_type'] == 'Debit' and transaction['users_transaction_phone'] == self.user['users_phone']:
                        trans_user = app_tables.wallet_users.get(users_phone=transaction['users_transaction_receiver_phone'])
                        if trans_user:
                            if trans_user['users_profile_pic']:
                                profile_pic = trans_user['users_profile_pic']
                            else:
                                profile_pic = '_/theme/account.png'
                    
                    if transaction['users_transaction_receiver_type'] == 'Credit' and transaction['users_transaction_receiver_phone'] == self.user['users_phone']:
                        trans_user = app_tables.wallet_users.get(users_phone=transaction['users_transaction_phone'])
                        if trans_user:
                            if trans_user['users_profile_pic']:
                                profile_pic = trans_user['users_profile_pic']
                            else:
                                profile_pic = '_/theme/account.png'

                    # Fetch username from wallet_user table using receiver_phone
                    if (transaction['users_transaction_phone'] == self.user['users_phone'] and transaction['users_transaction_type'] == 'Debit'):
                        receiver_user = app_tables.wallet_users.get(users_phone=receiver_phone)
                        receiver_username = receiver_user['users_username']
                    elif (transaction['users_transaction_receiver_phone'] == self.user['users_phone'] and transaction['users_transaction_receiver_type'] == 'Credit'):
                        receiver_user = app_tables.wallet_users.get(users_phone=transaction['users_transaction_phone'])
                        receiver_username = receiver_user['users_username']
                    else:
                        receiver_username = self.user['users_username']

                    # Set the transaction text and color based on transaction type
                    if transaction['users_transaction_receiver_type'] == 'Credit' and transaction['users_transaction_receiver_phone'] == self.user['users_phone']:
                        transaction_text = "Received"
                        fund_display = "+" + str(fund)
                        fund_color = "green"
                    elif transaction['users_transaction_phone'] == self.user['users_phone'] and transaction['users_transaction_type'] == 'Debit':
                        transaction_text = "Sent"
                        fund_display = "-" + str(fund)
                        fund_color = "red"
                    elif transaction['users_transaction_type'] == 'Deposited':
                        transaction_text = "TopUp"
                        fund_display = "+" + str(fund)
                        fund_color = "green"
                    elif transaction['users_transaction_type'] == 'Auto Topup':
                        transaction_text = "Auto Topup"
                        fund_display = "+" + str(fund)
                        fund_color = "green"
                    elif transaction['users_transaction_type'] == 'Withdrawn':
                        transaction_text = "Withdrawn"
                        fund_display = "-" + str(fund)
                        fund_color = "red"
                    else:
                        transaction_text = "Unknown"
                        fund_display = str(fund)
                        fund_color = "black"

                    # Append transaction details with username, transaction text, time, and day
                    self.repeating_panel_2_items.append({
                        'fund': fund_display,
                        'receiver_username': receiver_username,
                        'transaction_text': transaction_text,
                        'transaction_time': transaction_time,
                        'fund_color': fund_color,
                        'default_currency': default_currency,
                        'profile_pic': profile_pic,
                        'bank_name': transaction['users_transaction_bank_name']
                    })

                    # Limit the maximum number of history entries to display
                    if len(self.repeating_panel_2_items) >= max_history_entries:
                        break

                # Update spacer heights based on the number of history entries
                if len(self.repeating_panel_2_items) == 1:
                    self.spacer_3.visible = True
                    self.spacer_3.height = 9.051422119140625
                    self.spacer_2.height = 268.2103271484375
                elif len(self.repeating_panel_2_items) == 2:
                    self.spacer_2.height = 204.65887451171875
                elif len(self.repeating_panel_2_items) == 3:
                    self.spacer_2.height = 105.59344482421875
                    self.spacer_3.visible = True
                    self.spacer_3.height = 3.45
                elif len(self.repeating_panel_2_items) == 4:
                    self.spacer_2.height = 26.799102783203125
                elif len(self.repeating_panel_2_items) == 5:
                    self.spacer_2.visible = False

                self.repeating_panel_2.items = self.repeating_panel_2_items

    def inr_balance(self, balance, currency_type):
        # Iterate through the iterator to find the balance for the specified currency_type
        for row in balance:
            if row['users_balance_currency_type'] == currency_type:
                return row['users_balance']  # Return the balance for INR
        return '0'  # Fallback in case the currency_type is not found

  
    def timer_1_tick(self, **event_args):
        
        # Call the background task to check and perform top-ups
        anvil.server.call('check_and_topup_users',self.user['users_phone'])
    

    def link_10_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form("customer.deposit", user=self.user)

    def init_graph(self):
        # Create an empty figure
        fig = go.Figure()

        # Update plot with the empty figure
        self.plot_1.data = fig.data
        self.plot_1.layout = fig.layout


    def timer_1_tick(self, **event_args):
        # Call the background task to check and perform top-ups
       
        anvil.server.call('check_and_topup_users',self.user['users_phone'])
    
    def greet_based_on_time(self):
        from datetime import datetime
        current_time = datetime.now().time()
        
        if current_time < datetime.strptime('12:00:00', '%H:%M:%S').time():
          self.label_19_copy.text = "Good Morning"
            
        elif current_time > datetime.strptime('12:00:00', '%H:%M:%S').time() and current_time < datetime.strptime('16:00:00', '%H:%M:%S').time():
            self.label_19_copy.text = "Good Afternoon"
        elif current_time > datetime.strptime('16:00:00', '%H:%M:%S').time() and current_time < datetime.strptime('18:00:00', '%H:%M:%S').time():
          self.label_19_copy.text = "Good Evening"
        else:
          self.label_19_copy.text = "Good Night"
        


    def refresh_data(self):
    # Get the user's phone number
      phone_number = self.user['users_phone']
  
      # Get the current date and format it
      now = datetime.datetime.now()
      formatted_date = now.strftime('%a, %d-%b, %Y')
      self.label_11.text = formatted_date
  
      # Display the username
      self.label_20.text = self.user['users_username']
  
      # Get the user's default currency
      user_default_currency = 'INR'
      users_def_currency = app_tables.wallet_users.get(users_phone=self.user['users_phone'])
      if users_def_currency['users_defaultcurrency'] is not None:
          user_default_currency = users_def_currency['users_defaultcurrency']
  
      # Get the INR balance from the server and update the label
      balance_iterator = anvil.server.call('get_inr_balance', self.user['users_phone'])
      if balance_iterator is not None:
          balance = self.inr_balance(balance_iterator, user_default_currency)
          if balance != '0':
              self.label_13.text = str(f'{balance:.2f}')
          else:
              self.label_13.text = balance
          self.label_13.icon = f'fa:{user_default_currency.lower()}'
          self.label_13.icon_align = 'left'
      else:
          self.label_13.text = str(0)
  
      # Call the server function to get transactions data
      transactions = anvil.server.call('get_transactions')
  
      # DEBUG: Print the number of transactions retrieved from the server
      print("Number of transactions retrieved:", len(transactions))
  
      # Filter transactions to include only those involving the user's phone number and default currency
      filtered_transactions = [t for t in transactions if (t['users_transaction_phone'] == phone_number or t['users_transaction_receiver_phone'] == phone_number) and t['users_transaction_currency'] == user_default_currency]
  
      # DEBUG: Print the number of transactions after filtering
      print("Number of transactions after filtering:", len(filtered_transactions))
  
      # Filter transactions to include only 'Credit' and 'Debit' types
      filtered_transactions = [t for t in filtered_transactions if (t['users_transaction_phone'] == self.user['users_phone'] and t['users_transaction_type']=='Debit') or  (t['users_transaction_receiver_phone'] == self.user['users_phone']  and t['users_transaction_receiver_type']=='Credit')]
  
      # Organize data for plotting (aggregate by date and type)
      data_for_plot = {'Credit': {}, 'Debit': {}}  # Separate dictionaries for Credit and Debit transactions
      for transaction in filtered_transactions:
          date = transaction['users_transaction_date'].strftime("%Y-%m-%d")  # Format date as string for grouping
  
          trans_type = ''
          if transaction['users_transaction_phone'] == self.user['users_phone'] and transaction['users_transaction_type']=='Debit':
            trans_type='Debit'
          elif transaction['users_transaction_receiver_phone'] == self.user['users_phone'] and transaction['users_transaction_receiver_type']=='Credit':
            trans_type='Credit'
            
          fund = transaction['users_transaction_fund']  # Retrieve the 'fund' field
  
          try:
            if date not in data_for_plot[trans_type]:
                data_for_plot[trans_type][date] = 0
          except Exception as e:
            print(e)
  
          # Ensure fund is a string or a number before conversion
          if isinstance(fund, (int, float)):
              money_amount = fund
          elif isinstance(fund, str):
              # Extract numeric value from the 'fund' field
              try:
                  money_amount = float(fund)
              except ValueError:
                  money_amount = 0  # Handle cases where conversion to float fails
          else:
              money_amount = 0  # Default to 0 if 'fund' is neither a string nor a number
  
          # Aggregate transaction amounts by date and type
          if trans_type in data_for_plot:
              data_for_plot[trans_type][date] += money_amount
  
      # DEBUG: Print the data for plotting
      print("Data for plotting:", data_for_plot)
  
      # Plot the data
      categories = list(set(data_for_plot['Credit'].keys()) | set(data_for_plot['Debit'].keys()))  # Combine dates from Credit and Debit transactions
      categories.sort()  # Sort the dates for a proper time series plot
      credit_values = [data_for_plot['Credit'].get(date, 0) for date in categories]  # Get credit values for each date or 0 if date not present
      debit_values = [data_for_plot['Debit'].get(date, 0) for date in categories]    # Get debit values for each date or 0 if date not present
  
      self.plot_1.data = [
          {'x': categories, 'y': debit_values, 'type': 'bar', 'name': 'Debit', 'marker': {'color': 'gray'}},
          {'x': categories, 'y': credit_values, 'type': 'bar', 'name': 'Credit', 'marker': {'color': 'lightblue'}}
      ]
  
      self.plot_1.visible = True

    def get_credit_debit_details(self):
      users_phone = self.user['users_phone']
      user_default_currency='INR'
      users_def_currency = app_tables.wallet_users.get(users_phone=self.user['users_phone'])
      if users_def_currency['users_defaultcurrency'] is not None:
          user_default_currency = users_def_currency['users_defaultcurrency']
      else:
        user_default_currency = 'INR'
      
      try:
        cred_debt = anvil.server.call('get_credit_debit',users_phone,user_default_currency)
        credit_details = cred_debt['credit_details']
        debit_details = cred_debt['debit_details']
        credit_sum = 0
        debit_sum = 0
        if credit_details is not None:
          for i in credit_details:
            print(i['users_transaction_fund'])
            credit_sum += i['users_transaction_fund']
          print('credit',credit_sum)
          self.label_17_copy.text = str(credit_sum)
          self.label_17_copy.icon = f'fa:{user_default_currency.lower()}'
          self.label_17_copy.icon_align ='left'
        else:
          print('none')
          self.label_17_copy.text = str(0)
        if debit_details is not None:
          for j in debit_details:
            debit_sum += j['users_transaction_fund']
            print(j['users_transaction_fund'])
          print('debit',debit_sum)
          self.label_15_copy.text = str(debit_sum)
          self.label_15_copy.icon = f'fa:{user_default_currency.lower()}'
          self.label_15_copy.icon_align ='left'
        else:
          print('none')
          self.label_15_copy.text = str(0)
      except Exception as e:
        print(e)

    def check_profile_pic(self):
        print(self.user)
        print(self.user['users_email'],type(self.user['users_email']))
        user_data = app_tables.wallet_users.get(users_email=str(self.user['users_email'])) #changed
        if user_data:
          existing_img = user_data['users_profile_pic']
          if existing_img != None:
            self.image_2_copy.source = existing_img
          else: 
            print('no pic')
        else:
          print('none')

    def filter_transactions_by_period(self, transactions, period):
        now = datetime.datetime.now()

        if period == 'week':
            start_date = now - datetime.timedelta(days=7)
        elif period == 'month':
            start_date = now - datetime.timedelta(days=30)
        elif period == 'year':
            start_date = now - datetime.timedelta(days=365)
        else:
            return transactions  # If period is invalid, return all transactions

        # Ensure start_date is naive datetime
        start_date = start_date.replace(tzinfo=None)

        # Filter transactions with naive datetime comparison
        filtered_transactions = [t for t in transactions if t['users_transaction_date'].replace(tzinfo=None) >= start_date]
        return filtered_transactions

    def plot_transactions(self, transactions, plot_component):
    # Organize data for plotting (aggregate by date and type)
      data_for_plot = {'Credit': {}, 'Debit': {}}  # Separate dictionaries for Credit and Debit transactions
      for transaction in transactions:
          date = transaction['users_transaction_date'].strftime("%Y-%m-%d")  # Format date as string for grouping
  
          trans_type = ''
          if transaction['users_transaction_phone'] == self.user['users_phone'] and transaction['users_transaction_type']=='Debit':
            trans_type='Debit'
          elif transaction['users_transaction_receiver_phone'] == self.user['users_phone'] and transaction['users_transaction_receiver_type']=='Credit':
            trans_type='Credit'
          fund = transaction['users_transaction_fund']  # Retrieve the 'fund' field
  
          try:
            if date not in data_for_plot[trans_type]:
                data_for_plot[trans_type][date] = 0
          except Exception as e:
            print(e)
  
          # Ensure fund is a string or a number before conversion
          if isinstance(fund, (int, float)):
              money_amount = fund
          elif isinstance(fund, str):
              # Extract numeric value from the 'fund' field
              try:
                  money_amount = float(fund)
              except ValueError:
                  money_amount = 0  # Handle cases where conversion to float fails
          else:
              money_amount = 0  # Default to 0 if 'fund' is neither a string nor a number
  
          # Aggregate transaction amounts by date and type
          if trans_type in data_for_plot:
              data_for_plot[trans_type][date] += money_amount
  
      # DEBUG: Print the data for plotting
      print("Data for plotting:", data_for_plot)
  
      # Plot the data
      categories = list(set(data_for_plot['Credit'].keys()) | set(data_for_plot['Debit'].keys()))  # Combine dates from Credit and Debit transactions
      categories.sort()  # Sort the dates for a proper time series plot
      credit_values = [data_for_plot['Credit'].get(date, 0) for date in categories]  # Get credit values for each date or 0 if date not present
      debit_values = [data_for_plot['Debit'].get(date, 0) for date in categories]  # Get debit values for each date or 0 if date not present
  
      plot_component.data = [
          {'x': categories, 'y': debit_values, 'type': 'bar', 'name': 'Debit', 'marker': {'color': 'gray'}},
          {'x': categories, 'y': credit_values, 'type': 'bar', 'name': 'Credit', 'marker': {'color': 'lightblue'}}
      ]
  
      plot_component.visible = True
  
    def link_12_copy_click(self, **event_args):
        """This method is called when the link is clicked"""
        transactions = anvil.server.call('get_transactions')
        phone_number = self.user['users_phone']
        user_default_currency = self.get_user_default_currency()
    
        # Filter transactions based on phone number and default currency
        user_transactions = [
            t for t in transactions 
            if ( t['users_transaction_phone'] == phone_number or t['users_transaction_receiver_phone'] == phone_number) and t['users_transaction_currency'] == user_default_currency
        ]
        weekly_transactions = self.filter_transactions_by_period(user_transactions, 'week')
        self.plot_transactions(weekly_transactions, self.plot_1)
    
    def link_13_copy_click(self, **event_args):
        """This method is called when the link is clicked"""
        transactions = anvil.server.call('get_transactions')
        phone_number = self.user['users_phone']
        user_default_currency = self.get_user_default_currency()
    
        # Filter transactions based on phone number and default currency
        user_transactions = [
            t for t in transactions 
            if (t['users_transaction_phone'] == phone_number or t['users_transaction_receiver_phone'] == phone_number) and t['users_transaction_currency'] == user_default_currency
        ]
        monthly_transactions = self.filter_transactions_by_period(user_transactions, 'month')
        self.plot_transactions(monthly_transactions, self.plot_1)
    
    def link_14_click(self, **event_args):
        """This method is called when the link is clicked"""
        transactions = anvil.server.call('get_transactions')
        phone_number = self.user['users_phone']
        user_default_currency = self.get_user_default_currency()
    
        # Filter transactions based on phone number and default currency
        user_transactions = [
            t for t in transactions 
            if (t['users_transaction_phone'] == phone_number or t['users_transaction_receiver_phone'] == phone_number) and t['users_transaction_currency'] == user_default_currency
        ]
        yearly_transactions = self.filter_transactions_by_period(user_transactions, 'year')
        self.plot_transactions(yearly_transactions, self.plot_1)
    
    def get_user_default_currency(self):
        """Helper function to get the user's default currency"""
        user_default_currency = 'INR'
        users_def_currency = app_tables.wallet_users.get(users_phone=self.user['users_phone'])
        if users_def_currency and users_def_currency['users_defaultcurrency']:
            user_default_currency = users_def_currency['users_defaultcurrency']
        return user_default_currency
  
      
    def link_2_click(self, **event_args):
        open_form('customer.walletbalance', user=self.user)

    def link_3_click(self, **event_args):
        open_form('customer.transactions', user=self.user)

    def link_4_click(self, **event_args):
        open_form('customer.transfer', user=self.user)

    def link_5_click(self, **event_args):
        open_form('customer.withdraw', user=self.user)

    def link_7_click(self, **event_args):
        open_form('customer.Viewprofile', user=self.user)

    def link_6_click(self, **event_args):
        open_form('customer.auto_topup', user=self.user)

    def link_9_click(self, **event_args):
        open_form('Home', user=self.user)

    def link_8_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.settings',user = self.user)

    def notifications(self):
      items=[]
      self.repeating_panel_1.items=items
      an=anvil.server.call('get_notifications',self.user['users_phone'])
      so=sorted(an,key=lambda x:x['users_notification_date_time'],reverse=True)
      # length=0
      if so:
        for i in so:
          # column3=ColumnPanel(border='white',background='#87cefa')
          if i['users_notification_read'] is None or i['users_notification_read'] is not True:
            a=i['users_notification_text']
            b=i['users_notification_date_time'] #.strftime("%a-%I:%M %p")
            items.append({'text':a,
                        'date':b,
                          'phone':self.user['users_phone']})
            
        if len(items)>0:
          self.label_2.text=len(items)
        else:
          self.label_2.text=''
    
    def link_15_copy_click(self, **event_args):
      """This method is called when the link is clicked"""
      items=[]
      self.repeating_panel_1.items=items
      
      if self.link_clicked:
        self.column_panel_2.visible = True
        an=anvil.server.call('get_notifications',self.user['users_phone'])
        so=sorted(an,key=lambda x:x['users_notification_date_time'],reverse=True)
        length=0
        # total_notifications=len(so)
        for i in so:
          if i['users_notification_read'] is None or i['users_notification_read'] is not True:
            a=i['users_notification_text']
            b=i['users_notification_date_time'] #.strftime("%a-%I:%M %p")
            sender=i['users_notification_sender']
            items.append({'text':a,
                        'date':b,
                          'phone':self.user['users_phone'],
                         'sender_phone':sender})
            length +=1
            if length>4:
              break
        if len(items)>0:
          self.repeating_panel_1.items=items
          self.label_2.text=len(items)
        else:
          self.label_4.visible=True
          self.label_2.text=''
          self.repeating_panel_1.visible=False
          
        self.link_clicked=False
      else:
        self.column_panel_2.visible = False
        self.notifications()
        self.link_clicked=True

    def link_11_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.notifications',user=self.user)

    def link_10_copy_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.transactions',user=self.user)

    def link_1_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.wallet',user=self.user)

    def link_add_bank_click(self, **event_args):
      open_form("customer.wallet", user = self.user)

    def link_help_click(self, **event_args):
        
        open_form("help",user = self.user)

    def clik_dashboard(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer",user=self.user)

   
  
    # def timer_1_tick(self, **event_args):
    #   self.schedule_interval(self.check_user_data)
    
    # def start_checking(self):
    #     print("first ")

       
        
        
        
        
    #     while True:
    #         schedule.run_pending()
    #         time.sleep(10)
        
  
       
  
    # def check_user_data(self, dt):
  
    #     try:
    #         phone = self.user['users_phone']
    #         user = app_tables.wallet_users.get(users_phone=phone)
    #         if not user:
    #             print("Error: User data not found. Please set up your account.")
    #             return
           
    #         status = user['users_timely_topup']
  
    #         if user['users_last_auto_topup_time'] is not None:
    #             print("user inside4")
    #             today = datetime.today()
    #             formatted_date = today.strftime('%Y-%m-%d')
    #             if status and formatted_date <= user['users_timely_topup_expiry_date']:
    #                 next_topup_str = user['users_last_auto_topup_time']
    #                 next_topup = datetime.strptime(next_topup_str, '%Y-%m-%d %H:%M:%S.%f')
    #                 now = datetime.now()
  
    #                 if next_topup > now:
    #                     delay = (next_topup - now).total_seconds()
    #                     self.timer_2.interval = delay
                        
    #                     # Clock.schedule_once( delay)
    #                 else:
    #                     self.schedule_monthly_topup()
    #             else:
    #                 print("Auto top-up is disabled.")
    #         else:

    #             phone = self.user['users_phone']
    #             user = app_tables.wallet_users.get(users_phone=phone)
            
    #             status = self.user['users_timely_topup']
    #             today = datetime.datetime.today()
    #             formatted_date = today.strftime('%Y-%m-%d')
    #             print("gg",status)
    #             if status and formatted_date <= user['users_timely_topup_expiry_date']:
    #                 self.schedule_monthly_topup()
    #             else:
    #                self.schedule_monthly_topup()
                  
    #     except Exception as e:
    #         print(e)
    # schedule.every(20).seconds.do(check_user_data())
    # def schedule_monthly_topup(self):
    #     try:
    #         print("user inside")
    #         phone = self.user['users_phone']
    #         user = app_tables.wallet_users.get(users_phone=phone)
  
    #         status = user["users_timely_autotopup"]
    #         duration_days = None
    #         if  user['users_timely_topup_duration'] is not None:
    #             print("user inside1")
    #             duration_days = int(user['users_timely_topup_duration'])
    #         today = datetime.datetime.today()
    #         formatted_date = today.strftime('%Y-%m-%d')
    #         if status and duration_days is not None and formatted_date <= str(user['users_timely_topup_expiry_date']):
    #             now = datetime.datetime.now()
    #             next_topup = now + timedelta(days=duration_days)
    #             delay = (next_topup - now).total_seconds()
                
    #             self.timer_3 = delay
               
    #             # Clock.schedule_once(, delay)
    #         else:
    #             print("Auto top-up is disabled.")
    #     except Exception as e:
    #         print(e)
  
    # def add_money_to_wallet(self, dt):
  
    #     try:
    #         print("user inside3")
    #         phone = self.user['users_phone']
    #         user = app_tables.wallet_users.get(users_phone=phone)
    #         status = user["users_timely_autotopup"]
  
    #         today = datetime.datetime.today()
    #         formatted_date = today.strftime('%Y-%m-%d')
    #         if status and formatted_date <= str(user['users_timely_topup_expiry_date']):
    #             if user:
                    
    #                 amount = user["users_timely_topup_amount"]
    #                 # phone = user_data.get("users_phone")
    #                 currency_type = user['users_defaultcurrency']
    #                 balance_table = app_tables.wallet_users_balance.get(
    #                     users_balance_phone=phone,
    #                     users_balance_currency_type=currency_type
    #                 )
  
    #                 try:
    #                     if balance_table is not None:
    #                         date = datetime.now()
    #                         old_balance = balance_table['users_balance']
    #                         new_balance = old_balance + amount
    #                         balance_table['users_balance'] = new_balance
    #                         balance_table.update()
    #                         print(f"New balance: {balance_table['users_balance']}")
    #                         users_text = f"{amount} Added Through AutoTopUp"
    #                         anvil.server.call('notify', users_text, date, phone, phone)
    #                     else:
    #                         print("Error: Balance table not found.")
    #                 except Exception as e:
    #                     print(e)
  
    #                 self.schedule_monthly_topup()
    #     except Exception as e:
    #         print(e)

    # def timer_2_tick(self, **event_args):
    #   self.add_money_to_wallet()
    #   """This method is called Every [interval] secon. Does not trigger if [interval] is 0."""
    #   pass

    # def timer_3_tick(self, **event_args):
    #   self.add_money_to_wallet()
    #   pass

  
