# template for creating messages and using a messanges

project_path = __file__[:-len('test/send_email_test.py')]

settings = project_path + 'test.json'

creds_file = '/Users/cesarnunezrodriguez/local/projects/google_services/ceres_creds.json'
auth_file = '/Users/cesarnunezrodriguez/local/projects/google_services/ceres_token.pickle'

import sys, os
sys.path.append(project_path)
sys.path.append(project_path + './lib/')
sys.path.append(project_path + './data/')
from gmail_services import gmail_message

from datetime import datetime
now = datetime.now()

subject = 'Test on ' + now.strftime('%A %B %d, %Y at %-I:%M %p')
content = 'Files: '
attachments = (project_path + './data/' + 'file1.txt', project_path + './data/' + 'google-products.jpg')

email = gmail_message(creds_file)
email.build_message(subject, content, attachments)

new_attachments = (project_path + './data/' + 'file542.txt', project_path + './data/' + 'screenshot.png')
email.add_attachments(new_attachments)
email.send_email('ceres.assistant@gmail.com', '2674695888@tmomail.net')
