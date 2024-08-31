from ._anvil_designer import report_analysisTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go
import anvil.server
import re  # Import the regular expression module

class report_analysis(report_analysisTemplate):
    def __init__(self, user=None, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.user = user
        if user is not None:
            self.label_656.text = user['user_fullname']
        
        # Hide plot initially
        self.plot_1.visible = False
        self.refresh_data("transaction_trends")
      
    def refresh_data(self, data_type):
        if data_type == "transaction_trends":
          # Call the server function to get transactions data
          transactions = anvil.server.call('get_wallet_transactions')
      
          # Organize data for plotting (example: aggregate by date and type)
          data_for_plot = {}
          for transaction in transactions:
              date = transaction.get('transaction_timestamp', 'Unknown Date')
              trans_type = transaction.get('transaction_type', 'Unknown Type')
              fund = transaction.get('transaction_amount', 0)  # Default to 0 if not present
      
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
      
          # Extract data for plotting in the desired order
          categories = list(data_for_plot.keys())
          debit_values = [data['Debit'] for data in data_for_plot.values()]
          credit_values = [data['Credit'] for data in data_for_plot.values()]
          e_wallet_values = [data['Account to G-wallet'] for data in data_for_plot.values()]
          # Plot data in the specified order: Debit, Credit, Account to G-wallet
          self.plot_1.data = [
              {'x': categories, 'y': debit_values, 'type': 'bar', 'name': 'Debit'},
              {'x': categories, 'y': credit_values, 'type': 'bar', 'name': 'Credit'},
              {'x': categories, 'y': e_wallet_values, 'type': 'bar', 'name': 'Account to G-wallet'}
          ]
          self.plot_1.layout = go.Layout(title="Transaction Trends")

        elif data_type == "user_activity":
            # Call the server function to get user data
            users = anvil.server.call('get_user_pie', self.user['user_fullname'])
          
            # Count the number of active, inactive, and banned users
            active_users = sum(1 for user in users if self.is_user_active(user))
            banned_users = sum(1 for user in users if self.is_user_banned(user))
            inactive_users = sum(1 for user in users if self.is_user_inactive(user))
            
            # Create pie chart data in the order: Active, Banned, Inactive
            labels = ['Active Users', 'Banned Users', 'Inactive Users']
            values = [active_users, banned_users, inactive_users]
            
            # Plot the pie chart with click event handler
            self.plot_1.data = [{'labels': labels, 'values': values, 'type': 'pie'}]
            self.plot_1.layout = go.Layout(title="User Activity")

        elif data_type == "system_performance":
            # Call the server function to get transaction proof data
            transaction_proofs = anvil.server.call('get_wallet_transactions')

            # Count the number of successful and failed transactions
            successful_transactions = sum(1 for proof in transaction_proofs if isinstance(proof, dict) and proof.get('transaction_status') == 'success')
            failed_transactions = sum(1 for proof in transaction_proofs if isinstance(proof, dict) and proof.get('transaction_status') == 'failed')

            # Calculate percentages
            total_transactions = successful_transactions + failed_transactions
            if total_transactions > 0:
                success_percentage = (successful_transactions / total_transactions) * 100
                failed_percentage = (failed_transactions / total_transactions) * 100
            else:
                success_percentage = 0
                failed_percentage = 0

            # Create pie chart data with labels and percentages
            labels = ['Successful Transactions', 'Failed Transactions']
            values = [success_percentage, failed_percentage]

            self.plot_1.data = [{'labels': labels, 'values': values, 'type': 'pie'}]
            self.plot_1.layout = go.Layout(title="System Performance")

        # Show the plot
        self.plot_1.visible = True

    def is_user_active(self, user):
        """Check if the user is active (not banned and not inactive)."""
        return not user.get('user_banned') and not user.get('user_inactive')
    
    def is_user_inactive(self, user):
        """Check if the user is inactive (not banned but marked as inactive)."""
        return not user.get('user_banned') and user.get('user_inactive')
    
    def is_user_banned(self, user):
        """Check if the user is banned."""
        return user.get('user_banned')

    def plot_1_click(self, points, **event_args):
      """This method is called when a data point is clicked."""
      clicked_label = points[0]['label'] if points else None
  
      if clicked_label == 'Active Users':
          self.show_user_list(self.get_filtered_users('Active'))
      elif clicked_label == 'Banned Users':
          self.show_user_list(self.get_filtered_users('Banned'))
      elif clicked_label == 'Inactive Users':
          self.show_user_list(self.get_filtered_users('Inactive'))
  
    def get_filtered_users(self, status):
        """Filter users based on the clicked status."""
        users = anvil.server.call('get_user_data', self.user['user_fullname'])
        if status == 'Active':
            return [user for user in users if self.is_user_active(user)]
        elif status == 'Inactive':
            return [user for user in users if self.is_user_inactive(user)]
        elif status == 'Banned':
            return [user for user in users if self.is_user_banned(user)]
        return []
    
    def show_user_list(self, filtered_users):
        """Display the list of filtered users based on the selected status."""
        # Here you can implement logic to display filtered users, such as updating a table or label.
        # For demonstration, we'll print the filtered user count.
        alert(f"Number of users: {len(filtered_users)}")
      
    def link_44_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.refresh_data("transaction_trends")

    def link_66_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.refresh_data("user_activity")

    def link_99_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.refresh_data("system_performance")

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
        open_form('admin.admin_add_user', user=self.user)

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
        open_form('admin', user=self.user)

    def link_10_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.add_currency', user=self.user)

    def link_5_copy_click(self, **event_args):
        if self.user['user_usertype'] == 'super_admin':
            open_form('admin.manage_users', user=self.user)
        elif self.user['user_usertype'] == 'admin':
            open_form('admin.manage_users', user=self.user)
        else:
            open_form('user.view_profile', user=self.user)

    # def plot_1_click(self, points, **event_args):
    #   """This method is called when a data point is clicked."""
    #   if points:
    #       # Get the clicked segment's label
    #       clicked_label = points['points'][0]['label']
          
    #       if clicked_label == 'Active Users':
    #           # Perform action for active users
    #           print("Clicked on Active Users")
    #           # Open the relevant form or perform an action
    #           # For example: open_form('admin.active_users', user=self.user)
    #       elif clicked_label == 'Inactive Users':
    #           # Perform action for inactive users
    #           print("Clicked on Inactive Users")
    #           # Open the relevant form or perform an action
    #           # For example: open_form('admin.inactive_users', user=self.user)
    #       elif clicked_label == 'Banned Users':
    #           # Perform action for banned users
    #           print("Clicked on Banned Users")
    #           # Open the relevant form or perform an action
    #           # For example: open_form('admin.banned_users', user=self.user)

    
