from ._anvil_designer import adminTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import datetime


class admin(adminTemplate):
    def __init__(self, user=None, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.user = user
        if user is not None:
            self.label_2.text = user['users_username']
        self.refresh_data()

    def refresh_data(self):
        # Call the server function to get transactions data
        transactions = anvil.server.call('get_transactions')

        # Filter transactions to include only 'Credit' type
        credit_transactions = [t for t in transactions if t['users_transaction_type'] == 'Credit']

        # Identify all years present in the transactions
        years = sorted(set(transaction['users_transaction_date'].year for transaction in credit_transactions))

        # Organize data for plotting (aggregate by month and sum credit amounts)
        credit_by_month = {}
        for year in years:
            for month in range(1, 13):
                key = f"{year}-{month:02}"
                credit_by_month[key] = 0

        for transaction in credit_transactions:
            date = transaction['users_transaction_date'].strftime("%Y-%m")  # Format date as string for grouping
            credit_by_month[date] += transaction['users_transaction_fund']

        # Create data for plotting
        all_months = sorted(credit_by_month.keys())
        credit_values = [credit_by_month[month] for month in all_months]

        # Set the initial visible range to the last 12 months
        initial_visible_range = [all_months[-12], all_months[-1]] if len(all_months) >= 12 else [all_months[0], all_months[-1]]

        # Plot the data
        self.plot_1.data = [
            go.Bar(x=all_months, y=credit_values, name='Credit', marker_color='lightblue')
        ]

        # Set the layout to include month and year labels, highlighting current year
        self.plot_1.layout = go.Layout(
            title='Monthly Credit Transactions',
            xaxis=dict(
                title='Month',
                tickmode='array',
                tickvals=all_months,
                ticktext=[datetime.datetime.strptime(month, "%Y-%m").strftime("%Y-%b") for month in all_months],
                range=initial_visible_range  # Set the initial visible range
            ),
            yaxis=dict(title='Amount'),
            barmode='group'
        )

        self.plot_1.visible = True

    def link_1_click(self, **event_args):
        open_form('admin.report_analysis')

    def link_2_click(self, **event_args):
        open_form('admin.account_management')

    def link_3_click(self, **event_args):
        open_form('admin.transaction_monitoring')

    def link_4_click(self, **event_args):
        open_form('admin.admin_add_user',user=self.user)

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

    
