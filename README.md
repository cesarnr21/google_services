# Google Services
Just some modules that allow to use some Google Services. To Google Services and APIs, they needs to be setup
- instructions here: <https://www.thepythoncode.com/article/use-gmail-api-in-python>

Then download the API credentials to a `json` file and add it to the working directory.

## Gmail Module
The `gmail_services.py` includes the class `gmail_action` which allows to send emails and attachments. Functions in the class:
- `build_message(subject = 'str', content = 'str', attachments = 'str or tuple')`. This is used to put together the message being sent.
- Another way to add attachements to the email message is to use the `add_attachments()` function. Argument can either be a `string` for a single attachment or a `tuple` for multiple. It is important to add the full path of the attachment. The `os.path.anspath()` can be used to help with this.
- `send_email()` can be used after building a message to send the email. The arguments are the source email and a destination email address.
```py
from gmail_services import gmail_action

email = gmail_action(creds_file = 'credentials.json')

email.build_message(subject = ' ', content = ' ', attachments = ('file1', 'file2'))
email.add_attachments(attachments = ('files', 'files'))
email.send_email('source_email', 'target_email')
```

## Google Drive and Google Sheets

# TO DO
- worth looking into:
    - <https://github.com/jeremyephron/simplegmail#downloading-attachments>
        - receiving emails
        - downloading attachments
    - <https://github.com/dermasmid/google-workspace>
        - similar to what you are doing. some drive components
    - node.js client: <https://github.com/levz0r/gmail-tester>
- add instructions to creating google credentials
- send email to multiple people
- change how text files are sent, maybe remove all the options for storing different files.
    - check this out: <https://developers.google.com/gmail/api/guides/uploads>
- try sending videos, and other files
- Is `create_draft()` neccessary
- Add functionality to receive emails and proccess them


