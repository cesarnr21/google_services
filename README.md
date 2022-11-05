# Google Services
Just some modules that allow to use some Google Services. Install using:
`python3 -m pip install --editable .`

To use Google Services and APIs, they need to be setup
- instructions here: <https://www.thepythoncode.com/article/use-gmail-api-in-python>

Then download the API credentials to a `json` file and add it to the working directory.
A lot of code used in these modules came from this [Gmail API Tutorial](https://www.thepythoncode.com/article/use-gmail-api-in-python#Reading_Emails), it presents more of a functional programming approach, but these modules should be easier to use.

### Requirements
The Python Module need to access Google's API and require Google's Authentication packges. Install them using:
```sh
python3 -m pip install -r requirements.txt
```

## Gmail Module
### Sending Emails
The `gmail.py` module includes the class `GmailMessage` which allows to send emails and attachments. To send an email:
1. Used the `build_message(subject: str, content: str, attachments: Union[str, tuple])` function. This is used to put together the message being sent.
    - Another way to add attachements to the email message is to use the `add_attachments()` function. Argument can either be a `string` for a single attachment or a `tuple` for multiple. It is important to add the full path of the attachment. The `os.path.anspath()` can be used to help with this.
2. `send_email()` can be used after building a message to send the email. The arguments are the source email and a destination email address.
```py
import sys
from gmail import GmailMessage

sys.path.append('path/' + 'google_services/lib/')
creds_file = 'path/file'
auth_file = 'path/file'

subject = 'email subject'
content = 'content of email'
attachments = ('file1', 'file2')

email = GmailMessage(creds_file, auth_file)
email.build_message(subject, content, attachments)

new_attachments = ('file3', 'file4')
email.add_attachments(new_attachments)
email.send_email('source email', 'destination email')
```

### Reading Emails
To read emails, use the `GmailAction` class. 

More specify query options here: [Google APIs Notes](docs/google_APIs.md#Gmail-Query)
### Other Actions

## Google Drive and Google Sheets
The `google_drive.py` module includes the class `DriveAction` which will have the capability to upload 

--------------------------------------------------------

# TO DO
### Overall
- [ ] Add `setup.py` to install the module. Move the `requirements.txt` file here
- [ ] add API notes to docs
- [ ] add exceptions if there are no `auth_file` or `creds_file` given
- [ ] add better embedded `__docs__` into all modules/files
- [ ] place `create_query()` and other tools into a `tools.py` module?

### Gmail Module
- [ ] add option to use `mark_as_read` and other gmail actions by specifying an expecific email, instead of relying on `search_email`
- [ ] worth looking into:
    - <https://github.com/jeremyephron/simplegmail#downloading-attachments>
        - receiving emails
        - downloading attachments
    - <https://github.com/dermasmid/google-workspace>
        - similar to what you are doing. some drive components
    - node.js client: <https://github.com/levz0r/gmail-tester>
- [ ] add instructions to creating google credentials
- [ ] change how text files are sent, maybe remove all the options for storing different files.
    - check this out: <https://developers.google.com/gmail/api/guides/uploads>
- [ ] try sending videos, and other files
- [ ] Add functionality to receive emails and proccess them
- [ ] work with `notify` to print statements if the user wants
- [ ] add a `create_query()` to simplify the querying proccess. maybe create `guery` class? this will denpend on the querying proccess for google drive and sheets
    - test `after:` and `before:` queries with time instead of dates
- [ ] way to send a copy of a google drive file throught gmail (is this a function??, a script)

### Google Drive Modules
- [ ] upload file/folder
- [ ] download file/folder
- [ ] create folder
- [ ] share file/folder

### Sheets Module
- [ ] do these work for excel files uploaded to google sheets??
- [ ] download spreadsheet as an excel, maybe another more open source option
    - how to convert between the two filetypes offline as well
- [ ] create spreadsheet
- [ ] add to current spreadsheet
- [ ] how different is uploading and downloading these in relation to the `DriveAction` class?

## Bugs/Issues
- [ ] Error with subject highlighting without any attachments

