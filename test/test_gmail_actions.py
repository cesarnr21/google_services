# searching for emails

import sys, os
from googol import GmailAction
from googol import create_query

project_path = __file__[:-len('test/gmail_action_tests.py')]
sys.path.append(project_path + './lib/')
sys.path.append(project_path + './data/')

creds_file = '/Users/cesarnunezrodriguez/local/projects/settings/ceres_google_creds.json'
auth_file = '/Users/cesarnunezrodriguez/local/projects/settings/ceres_google_token.pickle'

email = GmailAction(creds_file, auth_file)
query = create_query('test 3', 'to:ceres.assistant@gmail.com')
email.search_email(query)

non_attach = ('tmobilespace.gif', 'dottedline600.gof', 'footer.gif')

#email.read_message(email.messages[0], non_attach)
email.read_message(email.messages)
email.print_messages()
email.mark_as_unread()      # amrks emails as unread
email.mark_as_read()        # marks emails as read
email.delete_email()        # deletes emails
