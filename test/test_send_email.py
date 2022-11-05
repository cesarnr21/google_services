"""
This is a script to test the capability of creating and sending an email with attachments
"""

import sys
import os
from datetime import datetime
from googol import GmailMessage

project_path = __file__[:-len('test/send_email_test.py')]
sys.path.append(project_path + './data/')

creds_file = '/Users/cesarnunezrodriguez/local/projects/settings/ceres_google_creds.json'
auth_file = '/Users/cesarnunezrodriguez/local/projects/settings/ceres_google_token.pickle'

now = datetime.now()

subject = 'Test on ' + now.strftime('%A %B %d, %Y at %-I:%M %p')
content = 'Files: '
attachments = (project_path + './data/' + 'file1.txt', project_path + './data/' + 'google-products.jpg')

email = GmailMessage(creds_file, auth_file)
email.build_message(subject, content, attachments)

new_attachments = (project_path + './data/' + 'file542.txt', project_path + './data/' + 'screenshot.png')
email.add_attachments(new_attachments)
email.send_email('ceres.assistant@gmail.com', 'cesarnr21@gmail.com')
