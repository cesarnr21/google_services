# searching for emails

import json

project_path = __file__[:-len('test/test.py')]

settings = project_path + 'test.json'

with open(settings, 'r') as file:
    config = json.load(file)

import sys, os
sys.path.append(project_path + './lib/')
sys.path.append(project_path + './data/')
from gmail_services import gmail_action

email = gmail_action(creds_file = config['ceres_gapi_creds'])
email.create_query("test_4")
email.search_email()
email.read_message(email.messages[0])
#email.read_message(email.search_email())
email.mark_as_unread()

