# searching for emails

import sys, os
from googol import GmailAction
from googol import create_query

project_path = __file__[:-len('test/test.py')]
sys.path.append(project_path + './data/')

creds_file = 'path/file_name'
auth_file = 'path/file_name'

email = GmailAction(creds_file, auth_file)
query = create_query('test 3', 'to:ceres.assistant@gmail.com')
email.search_email(query)

non_attach = ('tmobilespace.gif', 'dottedline600.gof', 'footer.gif')

#email.read_message(email.messages[0], non_attach)
email.read_message(email.messages)
email.print_messages()
#email.mark_as_unread()
#email.mark_as_read()
#email.delete_email()
