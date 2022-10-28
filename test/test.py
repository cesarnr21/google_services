# searching for emails

project_path = __file__[:-len('test/test.py')]

settings = project_path + 'test.json'

creds_file = '/Users/cesarnunezrodriguez/local/projects/settings/ceres_creds.json'
auth_file = '/Users/cesarnunezrodriguez/local/projects/settings/ceres_token.pickle'

import sys, os
sys.path.append(project_path + './lib/')
sys.path.append(project_path + './data/')
from gmail_services import GmailAction

email = GmailAction(creds_file, auth_file)
email.create_query("test 3")
email.search_email()

non_attach = ('tmobilespace.gif', 'dottedline600.gof', 'footer.gif')

email.read_message(email.messages[0], non_attach)
#email.read_message(email.search_email())
#email.mark_as_unread()
#email.delete_email()
