from base64 import urlsafe_b64decode
from email import message
from google_services import google_service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type
import os




class gmail_message(google_service):
    """docs here: https://www.thepythoncode.com/article/use-gmail-api-in-python """
    def __init__(self, creds_file: str):
        app_scope = ['https://mail.google.com/']
        google_service.__init__(self, creds_file, app_scope)
        from googleapiclient.discovery import build
        self.service = build('gmail', 'v1', credentials = self.creds)


    def build_message(self, content: str, subject = '', attachments = ()):
        """check this out about optional parameters: https://pybit.es/articles/code-better-with-type-hints-part-3/ """
        if subject == '':
            subject = 'no_subject'

        if len(attachments) != 0:
            attach_buf = {}

            if len(attachments) == 1:
                attach_buf[0] = attachments
            else:
                for i in range(len(attachments)):
                    attach_buf[i] = attachments[i]

            self.message = {'subject' : subject, 'content' : content, 'attachments' : attach_buf}

        else:
            self.message = {'subject' : subject, 'content' : content, 'attachments' : attachments}

        return self.message


    def build_attach(self, mail, attachment):
        content_type, encoding = guess_mime_type(attachment)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)

        try:
            if main_type == 'text':
                with open(attachment, 'rb') as file:
                   msg = MIMEText(file.read().decode(), _subtype = sub_type)

            elif main_type == 'image':
                with open(attachment, 'rb') as file:
                   msg = MIMEImage(file.read(), _subtype = sub_type)

            elif main_type == 'audio':
                with open(attachment, 'rb') as file:
                   msg = MIMEAudio(file.read(), _subtype = sub_type)

            else:
                with open(attachment, 'rb') as file:
                   msg = MIMEBase(main_type, sub_type)
                msg.set_payload(file.read())

            attachment = os.path.basename(attachment)
            msg.add_header('Content-Disposition', 'attachment', file = attachment)
            mail.attach(msg)

        except FileNotFoundError:
            print(attachment)
            print("ERROR: Attachments not found. Make sure you specify full path of file you want to attach")



    def create_draft(self):
        """docs here: https://developers.google.com/gmail/api/guides/drafts """
        print("create draft test:\n------------------------")
        print(self.message)
        # import base64
        # from email.message import EmailMessage

        # try:
        #     service = build('gmail', 'v1', credentials = self.creds)

        # except HttpError as error:
        #     print(F'An error occurred: {error}')
        #     draft = None

        # return draft
        return self.message


    def send_email(self, source_mail: str, target_mail: str):
        """docs here: https://developers.google.com/gmail/api/guides/sending """
        if not self.message['attachments']:
            mail = MIMEText(self.message['content'])
            mail['To'] = target_mail
            mail['From'] = source_mail
            mail['Subject'] = self.message['subject']

        else:
            mail = MIMEMultipart()
            mail['To'] = target_mail
            mail['From'] = source_mail
            mail['Subject'] = self.message['subject']
            mail.attach(MIMEText(self.message['content']))

            for i in range(len(self.message['attachments'])):
                self.build_attach(mail, self.message['attachments'][i])

        self.service.users().messages().send(userId = 'me', body = {'raw': base64.urlsafe_b64encode(mail.as_bytes()).decode()}).execute()


    def add_attachments(self, attachments = ()):
        index = len(self.message['attachments'])
        for i in range(len(attachments)):
            self.message['attachments'][index + i] = attachments[i]

        return self.message





class gmail_action(google_service):
    """docs here: 
    https://developers.google.com/gmail/api/guides/push 
    https://www.thepythoncode.com/article/use-gmail-api-in-python#Reading_Emails
    """

    def __init__(self, creds_file):
        app_scope = ['https://mail.google.com/']
        google_service.__init__(self, creds_file, app_scope)
        from googleapiclient.discovery import build
        self.service = build('gmail', 'v1', credentials = self.creds)


    def get_size_format(self, b, factor = 1024, suffix="B"):
        """
        Scale bytes to its proper byte format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
            if b < factor:
                return f"{b:.2f}{unit}{suffix}"
            b /= factor
        return f"{b:.2f}Y{suffix}"


    def clean(self, text):
        # clean text for creating a folder
        return "".join(c if c.isalnum() else "_" for c in text)


    def create_query(self, query):
        self.query = query
        return self.query


    def search_email(self):
        result = self.service.users().messages().list(userId = 'me', q = self.query).execute()
        self.messages = [ ]
        if 'messages' in result:
            self.messages.extend(result['messages'])

        while 'nextPageToken' in result:
            page_token = result['nextPageToken']
            result = self.service.users().messages().list(userId = 'me', q = self.query, pageToken = page_token).execute()

            if 'messages' in result:
                self.messages.extend(result['messages'])

        return self.messages


    def print_messages(self):
        print("Found", len(self.messages), "that matched the search query")
        for msg in self.messages:
            self.read_message(msg)


    def parse_parts(self, parts, folder_name, message):
        """Utility function that parses the content of an email partition"""
        if parts:
            for part in parts:
                filename = part.get("filename")
                mimeType = part.get("mimeType")
                body = part.get("body")
                data = body.get("data")
                file_size = body.get("size")
                part_headers = part.get("headers")

                if part.get("parts"):
                    self.parse_parts(self.service, part.get("parts"), folder_name, message)

                if mimeType == "text/plain":
                    if data:
                        text = urlsafe_b64decode(data).decode()
                        print(text)

                elif mimeType == "text/html":
                    if not filename:
                        filename = "index.html"

                    filepath = os.path.join(folder_name, filename)
                    print("Saving HTML to", filepath)
                    with open(filepath, "wb") as f:
                        f.write(urlsafe_b64decode(data))

                else:
                    # attachment other than a plain text or HTML
                    for part_header in part_headers:
                        part_header_name = part_header.get("name")
                        part_header_value = part_header.get("value")
                        if part_header_name == "Content-Disposition":
                            if "attachment" in part_header_value:
                                # we get the attachment ID 
                                # and make another request to get the attachment itself
                                print("Saving the file:", filename, "size:", self.get_size_format(file_size))
                                attachment_id = body.get("attachmentId")
                                attachment = self.service.users().messages() \
                                            .attachments().get(id=attachment_id, userId = 'me', messageId=message['id']).execute()
                                data = attachment.get("data")
                                filepath = os.path.join(folder_name, filename)
                                if data:
                                    with open(filepath, "wb") as f:
                                        f.write(urlsafe_b64decode(data))


    def read_message(self, message):
        msg = self.service.users().messages().get(userId = 'me', id = message['id'], format = 'full').execute()
        payload = msg['payload']
        headers = payload.get('headers')
        parts = payload.get('parts')
        self.attachments = payload.get('parts')
        folder_name = '../data/email'
        has_subject = False

        if headers:
            for header in headers:
                name = header.get('name')
                value = header.get('value')
                if name.lower() == 'from':
                    # we print the From address
                    print("From:", value)
                if name.lower() == 'to':
                    # we print the To address
                    print("To:", value)
                if name.lower() == 'from':
                    # make our boolean True, the email has "subject"
                    has_subject = True
                    # make a directory with the name of the subject
                    folder_name = self.clean(value)
                    # we will also handle emails with the same subject name
                    folder_counter = 0
                    while os.path.isdir(folder_name):
                        folder_counter += 1
                        # we have the same folder name, add a number next to it
                        if folder_name[-1].isdigit() and folder_name[-2] == "_":
                            folder_name = f"{folder_name[:-2]}_{folder_counter}"
                        elif folder_name[-2:].isdigit() and folder_name[-3] == "_":
                            folder_name = f"{folder_name[:-3]}_{folder_counter}"
                        else:
                            folder_name = f"{folder_name}_{folder_counter}"
                    os.mkdir(folder_name)
                    print("Subject:", value)
                if name.lower() == "date":
                    print("Date:", value)
        if not has_subject:
            # if the email does not have a subject, then make a folder with "email" name
            # since folders are created based on subjects
            if not os.path.isdir(folder_name):
                os.mkdir(folder_name)
        self.parse_parts(parts, folder_name, message)
        print("=" * 50)


    def print_email(self):
        print("=" * 50)

        pass


    def save_email(self, folder, file_name):
        if not file_name:
            file_name = "index.html"

        filepath = os.path.join(folder, file_name)
        print("Saving HTML to", filepath)
        with open(filepath, "wb") as f:
            f.write(urlsafe_b64decode(data))
        pass


    def save_attachments(self, folder):
        if not os.path.isdir(folder):
            os.mkdir(folder)

        pass


    def mark_as_read(self):
        messages_to_mark = self.search_email()
        
        # remove after done
        print("Matched emails:", len(messages_to_mark))

        return self.service.users().messages().batchModify( 
            userId = 'me',
            body = {'ids': [ msg['id'] for msg in messages_to_mark ], 'removeLabelIds': ['UNREAD']}
            ).execute()


    def mark_as_unread(self):
        messages_to_mark = self.search_email()

        # remove after done
        print("Matched emails:", len(messages_to_mark))

        return self.service.users().messages().batchModify( 
            userId = 'me',
            body = {'ids': [ msg['id'] for msg in messages_to_mark ], 'addLabelIds': ['UNREAD']}
            ).execute()


    def delete_email(self):
        messages_to_delete = self.search_messages()
        return self.service.users().messages().batchDelete(
            userId='me',
            body={'ids': [ msg['id'] for msg in messages_to_delete]}
            ).execute()
