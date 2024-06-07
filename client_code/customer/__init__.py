from ._anvil_designer import customerTemplate
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime
from anvil import *

class customer(customerTemplate):
    def __init__(self, user=None, password=None, **properties):
        # Initialize the form
        self.init_components(**properties)
        self.user = user
        self.password = password

        user_dict = dict(self.user)
        self.refresh_data()
        self.get_credit_debit_details()

        # Assuming user has a 'phone' attribute
        phone_number = user_dict.get('phone', None)
        default_currency = 'INR'
        users_def_currency = app_tables.wallet_users.get(users_phone=self.user['users_phone'])
        if users_def_currency['users_defaultcurrency'] is not None:
            default_currency = users_def_currency['users_defaultcurrency']
        if phone_number:
            # Search transactions based on the user's phone number
            items = app_tables.wallet_users_transaction.search(phone=phone_number, currency=default_currency)

            # Sort transactions by date in descending order
            sorted_transactions = sorted(items, key=lambda x: x['date'], reverse=True)

            # Check if there are any transactions
            if not sorted_transactions:
                self.repeating_panel_2.items = [{
                    'fund': "",
                    'receiver_username': "You're a new user, make some activity!",
                    'transaction_text': "",
                    'transaction_time': "",
                    'fund_color': "black"
                }]
            else:
                # Process transactions as before
                self.repeating_panel_2_items = []
                max_history_entries = 5  # Maximum number of history entries to display
                for transaction in sorted_transactions:
                    fund = transaction['fund']
                    transaction_type = transaction['transaction_type']
                    receiver_phone = transaction['receiver_phone']
                    transaction_time = transaction['date'].strftime("%a-%I:%M %p")  # Concatenate day with time (e.g., Mon-06:20 PM)

                    # Fetch username from wallet_user table using receiver_phone
                    receiver_user = app_tables.wallet_users.get(phone=receiver_phone)
                    if receiver_user:
                        receiver_username = receiver_user['username']
                    else:
                        receiver_username = "Unknown"

                    # Set the transaction text and color based on transaction type
                    if transaction_type == 'Credit':
                        transaction_text = "Received"
                        fund_display = "+" + str(fund)
                        fund_color = "green"
                    elif transaction_type == 'Debit':
                        transaction_text = "Sent"
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
                    })

                    # Limit the maximum number of history entries to display
                    if len(self.repeating_panel_2_items) >= max_history_entries:
                        break

                self.repeating_panel_2.items = self.repeating_panel_2_items

    def inr_balance(self, balance, currency_type):
        # Iterate through the iterator to find the balance for the specified currency_type
        for row in balance:
            if row['users_balance_currency_type'] == currency_type:
                return row['users_balance']  # Return the balance for INR
        return '0'  # Fallback in case the currency_type is not found

    def link_10_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form("customer.deposit", user=self.user)

    def init_graph(self):
        # Create an empty figure
        fig = go.Figure()

        # Update plot with the empty figure
        self.plot_1.data = fig.data
        self.plot_1.layout = fig.layout

    def refresh_data(self):
        # Get the user's phone number
        phone_number = self.user['users_phone']

        # Getting the data for total wallet amount
        now = datetime.datetime.now()
        formatted_date = now.strftime('%a, %d-%b, %Y')
        self.label_11.text = formatted_date
        # Display the username
        self.label_20.text = self.user['users_username']
        # Get the INR balance from the server
        # currency
        user_default_currency = 'INR'

        users_def_currency = app_tables.wallet_users.get(users_phone=self.user['users_phone'])
        if users_def_currency['users_defaultcurrency'] is not None:
            user_default_currency = users_def_currency['users_defaultcurrency']
        else:
            user_default_currency = 'INR'

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

        # Filter transactions to include only those involving the user's phone number
        filtered_transactions = [t for t in transactions if t['users_transaction_phone'] == phone_number]

        # DEBUG: Print the number of transactions after filtering
        print("Number of transactions after filtering:", len(filtered_transactions))

        # Filter transactions to include only 'Credit' and 'Debit' types
        filtered_transactions = [t for t in filtered_transactions if t['users_transaction_type'] in ['Credit', 'Debit']]

        # Organize data for plotting (aggregate by date and type)
        data_for_plot = {'Credit': {}, 'Debit': {}}  # Separate dictionaries for Credit and Debit transactions
        for transaction in filtered_transactions:
            date = transaction['users_transaction_date'].strftime("%Y-%m-%d")  # Format date as string for grouping

            trans_type = transaction['users_transaction_type']
            fund = transaction['users_transaction_fund']  # Retrieve the 'fund' field

            if date not in data_for_plot[trans_type]:
                data_for_plot[trans_type][date] = 0

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

        self.plot_1.data = [
            {'x': categories, 'y': debit_values, 'type': 'bar', 'name': 'Debit', 'marker': {'color': 'gray'}},
            {'x': categories, 'y': credit_values, 'type': 'bar', 'name': 'Credit', 'marker': {'color': 'lightblue'}}
        ]

        self.plot_1.visible = True

    def get_credit_debit_details(self):
        users_phone = self.user['users_phone']
        user_default_currency = 'INR'
        users_def_currency = app_tables.wallet_users.get(users_phone=self.user['users_phone'])
        if users_def_currency['users_defaultcurrency'] is not None:
            user_default_currency = users_def_currency['users_defaultcurrency']
        else:
            user_default_currency = 'INR'

        try:
            cred_debt = anvil.server.call('get_credit_debit', users_phone, user_default_currency)
            credit_details = cred_debt['credit_details']
            debit_details = cred_debt['debit_details']
            credit_sum = 0
            debit_sum = 0
            if credit_details is not None:
                for i in credit_details:
                    print(i['fund'])
                    credit_sum += i['fund']
                print('credit', credit_sum)
                self.label_17_copy.text = str(credit_sum)
                self.label_17_copy.icon = f'fa:{user_default_currency.lower()}'
                self.label_17_copy.icon_align = 'left'
            else:
                self.label_17_copy.text = str(0)
            if debit_details is not None:
                for i in debit_details:
                    print(i['fund'])
                    debit_sum += i['fund']
                print('debit', debit_sum)
                self.label_19.text = str(debit_sum)
                self.label_19.icon = f'fa:{user_default_currency.lower()}'
                self.label_19.icon_align = 'left'
            else:
                self.label_19.text = str(0)
        except Exception as e:
            print('exception: ', e)

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

            trans_type = transaction['users_transaction_type']
            fund = transaction['users_transaction_fund']  # Retrieve the 'fund' field

            if date not in data_for_plot[trans_type]:
                data_for_plot[trans_type][date] = 0

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
        user_transactions = [t for t in transactions if t['users_transaction_phone'] == phone_number]
        weekly_transactions = self.filter_transactions_by_period(user_transactions, 'week')
        self.plot_transactions(weekly_transactions, self.plot_1)

    def link_13_copy_click(self, **event_args):
        """This method is called when the link is clicked"""
        transactions = anvil.server.call('get_transactions')
        phone_number = self.user['users_phone']
        user_transactions = [t for t in transactions if t['users_transaction_phone'] == phone_number]
        monthly_transactions = self.filter_transactions_by_period(user_transactions, 'month')
        self.plot_transactions(monthly_transactions, self.plot_1)

    def link_14_click(self, **event_args):
        """This method is called when the link is clicked"""
        transactions = anvil.server.call('get_transactions')
        phone_number = self.user['users_phone']
        user_transactions = [t for t in transactions if t['users_transaction_phone'] == phone_number]
        yearly_transactions = self.filter_transactions_by_period(user_transactions, 'year')
        self.plot_transactions(yearly_transactions, self.plot_1)

      
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

    def link_12_copy_click(self, **event_args):
      """This method is called when the link is clicked"""
      pass

    def link_13_copy_click(self, **event_args):
      """This method is called when the link is clicked"""
      pass

    def link_14_click(self, **event_args):
      """This method is called when the link is clicked"""
      pass

    def plot_1_click(self, points, **event_args):
      """This method is called when a data point is clicked."""
      pass

   




