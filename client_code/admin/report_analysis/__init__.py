from ._anvil_designer import report_analysisTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
import re  # Import the regular expression module
from anvil.tables import app_tables

class report_analysis(report_analysisTemplate):
    def _init_(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.refresh_data()
        self.button_3.text = "System Performance"

        # Hide all plots initially
        self.plot_1.visible = False
        self.plot_2.visible = False
        self.plot_3.visible = False

    def refresh_data(self):
    # Call the server function to get transactions data
      transactions = anvil.server.call('get_transactions')
  
      # Organize data for plotting (example: aggregate by date and type)
      data_for_plot = {}
      for transaction in transactions:
          date = transaction['date']
          trans_type = transaction['transaction_type']
          fund = transaction['fund']  # Retrieve the 'fund' field
  
          if date not in data_for_plot:
              data_for_plot[date] = {'Deposit': 0, 'Withdrawal': 0, 'Account to E-wallet': 0}
  
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
          elif trans_type == 'Account to E-wallet':
              data_for_plot[date]['Account to E-wallet'] += money_amount
  
      # Plot the data only when the button is clicked
      if self.button_1.text == "Transaction trends":
          self.plot_1.visible = False
      else:
          categories = list(data_for_plot.keys())
          deposit_values = [data['Debit'] for data in data_for_plot.values()]
          withdrawal_values = [data['Credit'] for data in data_for_plot.values()]
          e_wallet_values = [data['Account to E-wallet'] for data in data_for_plot.values()]
  
          self.plot_1.data = [
              {'x': categories, 'y': deposit_values, 'type': 'bar', 'name': 'Debit'},
              {'x': categories, 'y': withdrawal_values, 'type': 'bar', 'name': 'Credit'},
              {'x': categories, 'y': e_wallet_values, 'type': 'bar', 'name': 'Account to E-wallet'}
          ]
  
          self.plot_1.visible = True


    def button_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.plot_1.visible = not self.plot_1.visible

        # Update the button text based on visibility
      if self.plot_1.visible:
          self.button_1.text = "Hide Transaction trends"
      else:
          self.button_1.text = "Transaction trends"

        # Refresh the data to update the graph visibility
      self.refresh_data()

    def button_2_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.plot_2.visible = not self.plot_2.visible

        # Update the button text based on visibility
      if self.plot_2.visible:
          self.button_2.text = "Hide User Activity"
      else:
          self.button_2.text = "User Activity"

        # Call the server function to get user data
      users = anvil.server.call('get_user_data')

        # Count the number of active and non-active users
      active_users = sum(1 for user in users if user['banned'] is None)
      non_active_users = sum(1 for user in users if user['banned'] is True)

        # Calculate percentages
      total_users = active_users + non_active_users
      active_percentage = (active_users / total_users) * 100
      non_active_percentage = (non_active_users / total_users) * 100

        # Create pie chart data
      labels = ['Active Users', 'Non-Active Users']
      values = [active_percentage, non_active_percentage]

        # Update plot_2 with pie chart data
      self.plot_2.data = [{'labels': labels, 'values': values, 'type': 'pie'}]

        # Optionally, you can set a title for the pie chart
      self.plot_2.title = 'User Status Distribution'

    def button_3_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.plot_3.visible = not self.plot_3.visible

        # Update the button text based on visibility
      if self.plot_3.visible:
          self.button_3.text = "Hide System Performance"
      else:
          self.button_3.text = "System Performance"

        # Call the server function to get transaction proof data
      transaction_proofs = anvil.server.call('get_transaction_proofs')

        # Count the number of successful and failed transactions
      successful_transactions = sum(1 for proof in transaction_proofs if proof['transaction_status'] == 'success')
      failed_transactions = sum(1 for proof in transaction_proofs if proof['transaction_status'] == 'failed')

        # Calculate percentages
      total_transactions = successful_transactions + failed_transactions
      success_percentage = (successful_transactions / total_transactions) * 100
      failed_percentage = (failed_transactions / total_transactions) * 100

        # Create pie chart data
      labels = ['Successful Transactions', 'Failed Transactions']
      values = [success_percentage, failed_percentage]

        # Update plot_3 with pie chart data
      self.plot_3.data = [{'labels': labels, 'values': values, 'type': 'pie'}]

        # Optionally, you can set a title for the pie chart
      self.plot_3.title = 'Transaction Proof Distribution'

    def link_1_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('admin.report_analysis')

    def link_2_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('admin.account_management', user= self.user)

    def link_7_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('admin.transaction_monitoring')

    def link_6_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('admin.admin_add_user')

    def link_5_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('admin.audit_trail', user = self.user)

    def link_4_click(self, **event_args):
      """This method is called when the link is clicked"""
      serves_data = app_tables.wallet_users_service.search()

    # Open the admin.user_support form and pass the serves_data
      user_support_form = open_form('admin.user_support', serves_data=serves_data)

    def link_3_click(self, **event_args):
      """This method is called when the link is clicked"""
      show_users_form = open_form('admin.show_users')

    def link_8_copy_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('admin')

    def button_8_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('Login')

    def button_3_copy_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('admin')
