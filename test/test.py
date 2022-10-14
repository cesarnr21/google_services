# template for creating messages and using a messanges

import json

project_path = __file__[:-len('test/test.py')]

settings = project_path + 'test.json'

with open(settings, 'r') as file:
    config = json.load(file)

import sys, os
sys.path.append(project_path + './lib/')
sys.path.append(project_path + './data/')
from gmail_services import gmail_message

from datetime import datetime
now = datetime.now()

email = gmail_message(creds_file = config['ceres_gapi_creds'])
email.build_message(subject = 'Test at ' + now.strftime('%H:%M:%S'), \
    content = 'doing testing on sending attachments', \
        attachments = os.path.abspath('data/file1.txt'))

email.add_attachments(attachments = (os.path.abspath('data/file542.txt'), os.path.abspath('data/screenshot.png')))
email.send_email(config['ceres_mail'], config['cesar_tmobile'])
