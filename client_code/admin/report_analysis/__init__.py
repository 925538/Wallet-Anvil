from ._anvil_designer import report_analysisTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
import re  # Import the regular expression module

class report_analysis(report_analysisTemplate):
    def __init__(self, user=None, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.user = user
        if user is not None:
            self.label_656.text = user['users_username']
        
        # Hide plot initially
        self.plot_1.visible = False
        self.refresh_data("transaction_trends")

    def refresh_data(self, data_type):
        if data_type == "transaction_trends":
            # Call the server function to get transactions data
            transactions = anvil.server.call('get_transactions')
        
            # Organize data for plotting (example: aggregate by date and type)
            data_for_plot = {}
            for transaction in transactions:
                date = transaction['users_transaction_date']
                trans_type = transaction['users_transaction_type']
                fund = transaction['users_transaction_fund']  # Retrieve the 'fund' field
        
                if date not in data_for_plot:
                    data_for_plot[date] = {'Debit': 0, 'Credit': 0, 'Account to G-wallet': 0}
        
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
        
                if trans_type == 'Debit':
                    data_for_plot[date]['Debit'] += money_amount
                elif trans_type == 'Credit':
                    data_for_plot[date]['Credit'] += money_amount
                elif trans_type == 'Account to G-wallet':
                    data_for_plot[date]['Account to G-wallet'] += money_amount
        
            categories = list(data_for_plot.keys())
            deposit_values = [data['Debit'] for data in data_for_plot.values()]
            withdrawal_values = [data['Credit'] for data in data_for_plot.values()]
            e_wallet_values = [data['Account to G-wallet'] for data in data_for_plot.values()]
        
            self.plot_1.data = [
                {'x': categories, 'y': deposit_values, 'type': 'bar', 'name': 'Debit'},
                {'x': categories, 'y': withdrawal_values, 'type': 'bar', 'name': 'Credit'},
                {'x': categories, 'y': e_wallet_values, 'type': 'bar', 'name': 'Account to G-wallet'}
            ]
            self.plot_1.layout = go.Layout(title="Transaction Trends")
        
        elif data_type == "user_activity":
    # Call the server function to get user data
            users = anvil.server.call('get_user_data')
        
            # Count the number of active, inactive, and banned users
            active_users = sum(1 for user in users if user['inactive'] is None and user['banned'] is None)
            inactive_users = sum(1 for user in users if user['inactive'] is True and user['banned'] is None)
            banned_users = sum(1 for user in users if user['banned'] is True)
        
            # Calculate percentages
            total_users = banned_users + active_users + inactive_users
            banned_percentage = (banned_users / total_users) * 100
            active_percentage = (active_users / total_users) * 100
            inactive_percentage = (inactive_users / total_users) * 100
        
            # Create pie chart data
            labels = ['Banned Users', 'Active Users', 'Inactive Users']
            values = [banned_percentage, active_percentage, inactive_percentage]
        
            self.plot_1.data = [{'labels': labels, 'values': values, 'type': 'pie'}]
            self.plot_1.layout = go.Layout(title="User Activity")
        
        elif data_type == "system_performance":
            # Call the server function to get transaction proof data
            transaction_proofs = anvil.server.call('get_transaction_proofs')

            # Count the number of successful and failed transactions
            successful_transactions = sum(1 for proof in transaction_proofs if proof['users_transaction_status'] == 'success')
            failed_transactions = sum(1 for proof in transaction_proofs if proof['users_transaction_status'] == 'failed')

            # Calculate percentages
            total_transactions = successful_transactions + failed_transactions
            success_percentage = (successful_transactions / total_transactions) * 100
            failed_percentage = (failed_transactions / total_transactions) * 100

            # Create pie chart data
            labels = ['Successful Transactions', 'Failed Transactions']
            values = [success_percentage, failed_percentage]

            self.plot_1.data = [{'labels': labels, 'values': values, 'type': 'pie'}]
            self.plot_1.layout = go.Layout(title="System Performance")

        # Show the plot
        self.plot_1.visible = True

    def link_44_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.refresh_data("transaction_trends")

    def link_66_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.refresh_data("user_activity")

    # def link_99_click(self, **event_args):
    #     """This method is called when the button is clicked"""
    #     self.refresh_data("system_performance")

    def link_1_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.report_analysis', user=self.user)

    def link_2_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.account_management', user=self.user)

    def link_7_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.transaction_monitoring', user=self.user)

    def link_6_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.admin_add_user', user=self.user)

    def link_5_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.audit_trail', user=self.user)

    def link_4_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.admin_add_user',user=self.user)

    def link_3_click(self, **event_args):
        """This method is called when the link is clicked"""
        show_users_form = open_form('admin.transaction_monitoring', user=self.user)

    def link_8_copy_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin', user=self.user)

    def button_8_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('Login')

    def button_3_copy_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('admin', user=self.user)

    def link_8_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('admin',user=self.user)

    def link_10_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('admin.add_currency',user=self.user)

    def link_5_copy_click(self, **event_args):
      if self.user['users_usertype'] == 'super_admin':
          # Open the admin creation form
          open_form("admin.create_admin", user=self.user)
      else:
          # Show an alert if the user is not a super admin
          alert("You're not a super admin. Only super admins can perform this action.")

    def link_5_copy_2_click(self, **event_args):
      open_form("admin.user_support",user = self.user)

    def link_5_copy_3_click(self, **event_args):
      open_form("admin.add_bank_account",user = self.user)
