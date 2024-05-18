from ._anvil_designer import adminTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server


class admin(adminTemplate):
  def __init__(self, user=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = user
    if user is not None:
            self.label_2.text = user['username']
    self.refresh_data()
  def refresh_data(self):
        # Call the server function to get transactions data
        transactions = anvil.server.call('get_transactions')
      
        # Organize data for plotting (aggregate by date and type)
        data_for_plot = {'Credit': {}, 'Debit': {}}  # Separate dictionaries for Credit and Debit transactions
        for transaction in transactions:
            date = transaction['date'].strftime("%Y-%m-%d")  # Format date as string for grouping
        
            trans_type = transaction['transaction_type']
            fund = transaction['fund']  # Retrieve the 'fund' field
        
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
      
        # Plot the data
        categories = list(set(data_for_plot['Credit'].keys()) | set(data_for_plot['Debit'].keys()))  # Combine dates from Credit and Debit transactions
        credit_values = [data_for_plot['Credit'].get(date, 0) for date in categories]  # Get credit values for each date or 0 if date not present
        debit_values = [data_for_plot['Debit'].get(date, 0) for date in categories]    # Get debit values for each date or 0 if date not present
        
        self.plot_1.data = [
            {'x': categories, 'y': debit_values, 'type': 'bar', 'name': 'Debit', 'marker': {'color': 'gray'}},
            {'x': categories, 'y': credit_values, 'type': 'bar', 'name': 'Credit', 'marker': {'color': 'lightblue'}}
        ]
      
        self.plot_1.visible = True
  def link_1_click(self, **event_args):
    open_form('admin.report_analysis')

  def link_2_click(self, **event_args):
    open_form('admin.account_management')

  def link_3_click(self, **event_args):
    open_form('admin.transaction_monitoring')

  def link_4_click(self, **event_args):
    open_form('admin.admin_add_user')

  def link_5_click(self, **event_args):
    open_form('admin.audit_trail')

  def link_6_click(self, **event_args):
    open_form('admin.user_support')

  def link_7_click(self, **event_args):
    open_form('admin.show_users')

  def link_9_click(self, **event_args):
    open_form('Home')

  def link_10_click(self, **event_args):
    open_form('admin.add_currency')
