# template for creating messages and using a messanges

import json

project_path = __file__[:-len('test/send_email_test.py')]

settings = project_path + 'test.json'

with open(settings, 'r') as file:
    config = json.load(file)

import sys, os
sys.path.append(project_path)
sys.path.append(project_path + './lib/')
sys.path.append(project_path + './data/')
from gmail_services import gmail_message

from datetime import datetime
now = datetime.now()

email = gmail_message(creds_file = project_path + config['ceres_gapi_creds'])
email.build_message(subject = 'Test on ' + now.strftime('%A %B %d, %Y at %-I:%M %p'), content = 'Files: ', attachments = (project_path + './data/' + 'file1.txt', project_path + './data/' + 'google-products.jpg'))
email.add_attachments(attachments = (project_path + './data/' + 'file542.txt', project_path + './data/' + 'screenshot.png'))
email.send_email(config['ceres_mail'], config['cesar_tmobile'])
