from ._anvil_designer import audit_trailTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class audit_trail(audit_trailTemplate):
    def __init__(self, user=None, **properties):
        # Set Form properties and Data Bindings.
        self.user = user
        self.init_components(**properties)
        self.repeating_panel_items = []
        self.load_all_actions()
        # Any code you write here will run before the form opens.
        self.check_profile_pic()
        # self.label_7.text = self.user['users_username']

    def check_profile_pic(self):
        if self.user and 'users_email' in self.user:
            print(self.user)
            print(self.user['users_email'], type(self.user['users_email']))
            user_data = app_tables.wallet_users.get(users_email=str(self.user['users_email']))  # changed
            if user_data:
                existing_img = user_data.get('users_profile_pic')
                if existing_img:
                    self.image_3_copy.source = existing_img
                else:
                    print('No profile picture found')
            else:
                print('No user data found')
        else:
            print('User data is incomplete or missing')

    def load_all_actions(self):
        """Load all actions into the repeating panel."""
        self.repeating_panel_items = []
        actions_data = app_tables.wallet_admins_actions.search()
        self.grouped_details = {}
        if actions_data:
            for item in actions_data:
                print('yes1')
                # Extract date in YYYY-MM-DD format without time
                date_str = item['admins_actions_date'] #.strftime("%Y-%m-%d")
                if date_str not in self.grouped_details:
                    self.grouped_details[date_str] = {'date': item['admins_actions_date'], 'details': []}
                self.grouped_details[date_str]['details'].append(item)
        else:
            return

        # Sort dates in descending order
        sorted_dates = sorted(self.grouped_details.keys(), reverse=True)

        # Create a list of dictionaries for repeating_panel_1
        # repeating_panel_items = []
        for date_str in sorted_dates:
            date_info = self.grouped_details[date_str]
            for action in reversed(date_info['details']):
                admin_action = action['admins_actions']
                admin_action_username = action['admins_actions_username']
                profile_pic = '_/theme/account.png'
                userr = app_tables.wallet_users.get(users_username=action['admins_actions_username'])
                if userr:
                    if userr['users_profile_pic']:
                        profile_pic = userr['users_profile_pic']
                    else:
                        profile_pic = '_/theme/account.png'

                # Append transaction details with username instead of receiver_phone
                self.repeating_panel_items.append({'date': date_info['date'].strftime("%Y-%m-%d"),
                                                   'time': date_info['date'].strftime("%I:%M %p"),
                                                   'admin_name': action['admins_actions_name'],
                                                   'admin_action': admin_action,
                                                   'admin_action_username': admin_action_username,
                                                   'profile_pic': profile_pic,
                                                   })
        self.repeating_panel_2.items = self.repeating_panel_items
        self.data_grid_1.rows_per_page = int(self.text_box_2.text) + 1

    def date_picker_1_change(self, **event_args):
        start = []
        end = []
        if self.date_picker_1.date and self.date_picker_2.date:
            for i in range(len(self.repeating_panel_items)):
                if str(self.date_picker_1.date.strftime("%Y-%m-%d")) <= str(self.repeating_panel_items[i]['date']) <= str(self.date_picker_2.date.strftime("%Y-%m-%d")):
                    end.append({'date': self.repeating_panel_items[i]['date'],
                                'time': self.repeating_panel_items[i]['time'],
                                'admin_name': self.repeating_panel_items[i]['admin_name'],
                                'admin_action': self.repeating_panel_items[i]['admin_action'],
                                'admin_action_username': self.repeating_panel_items[i]['admin_action_username'],
                                'profile_pic': self.repeating_panel_items[i]['profile_pic'],
                                })
            self.repeating_panel_2.items = end
        elif self.date_picker_1.date:
            for i in range(len(self.repeating_panel_items)):
                if str(self.repeating_panel_items[i]['date']) == str(self.date_picker_1.date.strftime("%Y-%m-%d")):
                    start.append({'date': self.repeating_panel_items[i]['date'],
                                  'time': self.repeating_panel_items[i]['time'],
                                  'admin_name': self.repeating_panel_items[i]['admin_name'],
                                  'admin_action': self.repeating_panel_items[i]['admin_action'],
                                  'admin_action_username': self.repeating_panel_items[i]['admin_action_username'],
                                  'profile_pic': self.repeating_panel_items[i]['profile_pic'],
                                  })
            self.repeating_panel_2.items = start
        else:
            print('no')
            self.load_all_actions()

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        username = self.text_box_1.text.strip()
        users = []
        search_results = app_tables.wallet_admins_actions.search(admins_actions_username=username)
        if search_results:
            # Perform the search for users based on the entered username
            for i in range(len(self.repeating_panel_items)):
                if username == self.repeating_panel_items[i]['admin_action_username'].strip():
                    users.append({'date': self.repeating_panel_items[i]['date'],
                                  'time': self.repeating_panel_items[i]['time'],
                                  'admin_name': self.repeating_panel_items[i]['admin_name'],
                                  'admin_action': self.repeating_panel_items[i]['admin_action'],
                                  'admin_action_username': self.repeating_panel_items[i]['admin_action_username'],
                                  'profile_pic': self.repeating_panel_items[i]['profile_pic'],
                                  })
            self.repeating_panel_2.items = users
        print('seeing', users)
        if not users:
            # If the search box is empty, load all actions
            print('reaching')
            anvil.alert('User not found.')
            self.load_all_actions()

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
        open_form('admin.admin_add_user',user=self.user)

    def link_3_click(self, **event_args):
        open_form('admin.transaction_monitoring',user=self.user)

    def link_8_copy_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin', user=self.user)

    def button_8_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('Login')

    def button_3_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('Home')

    def link_8_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin', user=self.user)

    # def button_1_click(self, **event_args):
    #   """This method is called when the button is clicked"""
    #   username = self.text_box_1.text.strip()
    #   if username:
    #     # Perform the search for users based on the entered username
    #     search_results = app_tables.wallet_admins_actions.search(admins_actions_username=username)
    #     self.repeating_panel_2.items = search_results

    #   else:
    #     # If the search box is empty, load all actions
    #     self.load_all_actions()








# from ._anvil_designer import audit_trailTemplate




# from anvil import *
# import anvil.server
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables

# class audit_trail(audit_trailTemplate):
#   def __init__(self, user=None, **properties):
#     # Set Form properties and Data Bindings.
#     self.user = user
#     self.init_components(**properties)
#     self.repeating_panel_items=[]
#     self.load_all_actions()
#     # Any code you write here will run before the form opens.
#     self.check_profile_pic()
#     #self.label_7.text = self.user['users_username']
  
#   def check_profile_pic(self):
#         print(self.user)
#         print(self.user['users_email'],type(self.user['users_email']))
#         user_data = app_tables.wallet_users.get(users_email=str(self.user['users_email'])) #changed
#         if user_data:
#           existing_img = user_data['users_profile_pic']
#           if existing_img != None:
#             self.image_3_copy.source = existing_img
#           else: 
#             print('no pic')
#         else:
#           print('none')
  
#   def load_all_actions(self):
#     """Load all actions into the repeating panel."""
#     self.repeating_panel_items=[]
#     actions_data = app_tables.wallet_admins_actions.search()
#     self.grouped_details = {}
#     if actions_data:
#       for item in actions_data:
#           print('yes1')
#           # Extract date in YYYY-MM-DD format without time
#           date_str = item['admins_actions_date'].strftime("%Y-%m-%d")
#           if date_str not in self.grouped_details:
#               self.grouped_details[date_str] = {'date': item['admins_actions_date'], 'details': []}
#           self.grouped_details[date_str]['details'].append(item)
#     else:
#       return

#     # Sort dates in descending order
#     sorted_dates = sorted(self.grouped_details.keys(), reverse=True)

#     # Create a list of dictionaries for repeating_panel_1
#     # repeating_panel_items = []
#     for date_str in sorted_dates:
#         date_info = self.grouped_details[date_str]
#         for action in reversed(date_info['details']):
#             admin_action = action['admins_actions']
#             admin_action_username = action['admins_actions_username']
#             profile_pic = '_/theme/account.png'
#             userr = app_tables.wallet_users.get(users_username= action['admins_actions_username'])
#             if userr:
#               if userr['users_profile_pic']:
#                 profile_pic = userr['users_profile_pic'] 
#               else:
#                 profile_pic = '_/theme/account.png'
            
#             # Append transaction details with username instead of receiver_phone
#             self.repeating_panel_items.append({'date': date_info['date'].strftime("%Y-%m-%d"),
#                                             'admin_name':action['admins_actions_name'],
#                                             'admin_action':admin_action,
#                                             'admin_action_username':admin_action_username,
#                                             'profile_pic':profile_pic,
#                                             })
#     self.repeating_panel_2.items = self.repeating_panel_items
#     self.data_grid_1.rows_per_page = int(self.text_box_2.text)+1

#   def date_picker_1_change(self, **event_args):
#     start = []
#     end=[]
#     if self.date_picker_1.date and self.date_picker_2.date:
#       for i in range(len(self.repeating_panel_items)):
#         if str(self.date_picker_1.date.strftime("%Y-%m-%d")) <= str(self.repeating_panel_items[i]['date']) <= str(self.date_picker_2.date.strftime("%Y-%m-%d")):
#           end.append({'date': self.repeating_panel_items[i]['date'],
#                         'admin_name':self.repeating_panel_items[i]['admin_name'],
#                         'admin_action':self.repeating_panel_items[i]['admin_action'],
#                         'admin_action_username':self.repeating_panel_items[i]['admin_action_username'],
#                         'profile_pic':self.repeating_panel_items[i]['profile_pic'],
#                         })
#       self.repeating_panel_2.items = end
#     elif self.date_picker_1.date:
#       for i in range(len(self.repeating_panel_items)):
#         if str(self.repeating_panel_items[i]['date']) == str(self.date_picker_1.date.strftime("%Y-%m-%d")):
#           start.append({'date': self.repeating_panel_items[i]['date'],
#                         'admin_name':self.repeating_panel_items[i]['admin_name'],
#                         'admin_action':self.repeating_panel_items[i]['admin_action'],
#                         'admin_action_username':self.repeating_panel_items[i]['admin_action_username'],
#                         'profile_pic':self.repeating_panel_items[i]['profile_pic'],
#                         })
#       self.repeating_panel_2.items = start

#     else:
#       print('no')
#       self.load_all_actions()

#   def button_1_click(self, **event_args):
#     """This method is called when the button is clicked"""
#     username = self.text_box_1.text.strip()
#     users=[]
#     search_results = app_tables.wallet_admins_actions.search(admins_actions_username=username)
#     if search_results:
#       # Perform the search for users based on the entered username 
#       for i in range(len(self.repeating_panel_items)):
#         if username == self.repeating_panel_items[i]['admin_action_username'].strip():
#           users.append({'date': self.repeating_panel_items[i]['date'],
#                         'admin_name':self.repeating_panel_items[i]['admin_name'],
#                         'admin_action':self.repeating_panel_items[i]['admin_action'],
#                         'admin_action_username':self.repeating_panel_items[i]['admin_action_username'],
#                         'profile_pic':self.repeating_panel_items[i]['profile_pic'],
#                         })
#       self.repeating_panel_2.items = users  
#     print('seeing',users)
#     if not users:
#       # If the search box is empty, load all actions
#       print('reaching')
#       anvil.alert('User not found.')
#       self.load_all_actions()

  
#   def link_1_click(self, **event_args):
#     """This method is called when the link is clicked"""
#     open_form('admin.report_analysis', user=self.user)

#   def link_2_click(self, **event_args):
#     """This method is called when the link is clicked"""
#     open_form('admin.account_management', user=self.user)

#   def link_7_click(self, **event_args):
#     """This method is called when the link is clicked"""
#     open_form('admin.transaction_monitoring', user=self.user)

#   def link_6_click(self, **event_args):
#     """This method is called when the link is clicked"""
#     open_form('admin.admin_add_user', user=self.user)

#   def link_5_click(self, **event_args):
#     """This method is called when the link is clicked"""
#     open_form('admin.audit_trail', user=self.user)

#   def link_4_click(self, **event_args):
#     """This method is called when the link is clicked"""
#     serves_data = app_tables.wallet_admins_actions.search()

#     # Open the admin.user_support form and pass the serves_data
#     user_support_form = open_form('admin.user_support', serves_data=serves_data, user=self.user)

#   def link_3_click(self, **event_args):
#     """This method is called when the link is clicked"""
#     show_users_form = open_form('admin.show_users', user=self.user)

#   def link_8_copy_click(self, **event_args):
#     """This method is called when the link is clicked"""
#     open_form('admin', user=self.user)

#   def button_8_click(self, **event_args):
#     """This method is called when the button is clicked"""
#     open_form('Login')

#   def button_3_click(self, **event_args):
#     """This method is called when the button is clicked"""
#     open_form('Home')

#   def link_8_click(self, **event_args):
#     """This method is called when the link is clicked"""
#     open_form('admin',user=self.user)

#   # def button_1_click(self, **event_args):
#   #   """This method is called when the button is clicked"""
#   #   username = self.text_box_1.text.strip()
#   #   if username:
#   #     # Perform the search for users based on the entered username
#   #     search_results = app_tables.wallet_admins_actions.search(admins_actions_username=username)
#   #     self.repeating_panel_2.items = search_results
    
      
#   #   else:
#   #     # If the search box is empty, load all actions
#   #     self.load_all_actions()

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
    

