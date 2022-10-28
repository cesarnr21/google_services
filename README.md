# Google Services
Just some modules that allow to use some Google Services. To use Google Services and APIs, they need to be setup
- instructions here: <https://www.thepythoncode.com/article/use-gmail-api-in-python>

Then download the API credentials to a `json` file and add it to the working directory.
A lot of code used in these modules came from this [Gmail API Tutorial](https://www.thepythoncode.com/article/use-gmail-api-in-python#Reading_Emails), it presents more of a functional programming approach, but these modules should be easier to use.

## Gmail Module
### Sending Emails
The `gmail_services.py` module includes the class `GmailMessage` which allows to send emails and attachments. To send an email:
1. Used the `build_message(subject: str, content: str, attachments: Union[str, tuple)` function. This is used to put together the message being sent.
    - Another way to add attachements to the email message is to use the `add_attachments()` function. Argument can either be a `string` for a single attachment or a `tuple` for multiple. It is important to add the full path of the attachment. The `os.path.anspath()` can be used to help with this.
2. `send_email()` can be used after building a message to send the email. The arguments are the source email and a destination email address.
```py
from gmail_services import GmailMessage

creds_file = 'path'
auth_file = 'path'

email = GmailMessage(creds_file, auth_file)

email.build_message(subject = ' ', content = ' ', attachments = ('path/file1', 'path/file2'))
email.add_attachments(attachments = ('path/file3', 'path/file4')) # optional: if you want to add attachments after building the message
email.send_email('source_email', 'target_email')
```

### Reading Emails
To read emails, use the `GmailAction` class. 

### Other Actions

## Google Drive and Google Sheets

# TO DO
- should `attachemtns` in the message dictionary be stored as `dict` or a `list`. can't do `tuple` because then you wouldn't be able to add more attachments.
- add exceptions if there are no `auth_file` or `creds_file` given
- add option to use `mark_as_read` and other gmail actions by specifying an expecific email, instead of relying on `search_email`
- check that sending attachments work from directories outside the `google services` directory
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
- add a `create_query()` to simplify the querying proccess. maybe create `guery` class? this will denpend on the querying proccess for google drive and sheets
    - search emails by:
        - unread
        - starred
    - examplee: <https://github.com/jeremyephron/simplegmail/blob/master/simplegmail/query.py>
- work with `notify` to print statements if the user wants
- way to send a copy of a google drive file throught gmail (is this a function??, a script)

## Bugs/Issues
- Error with subject highlighting without any attachments
