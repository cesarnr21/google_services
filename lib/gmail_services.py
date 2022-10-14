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
        # might remove these lines below
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
                   msg = MIMEText(file.read().decode(), _subtype=sub_type)

            elif main_type == 'image':
                with open(attachment, 'rb') as file:
                   msg = MIMEImage(file.read(), _subtype=sub_type)

            elif main_type == 'audio':
                with open(attachment, 'rb') as file:
                   msg = MIMEAudio(file.read(), _subtype=sub_type)

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



    # utility functions
    def get_size_format(b, factor = 1024, suffix="B"):
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



    def clean(text):
        # clean text for creating a folder
        return "".join(c if c.isalnum() else "_" for c in text)



    def get_messages(self, query):
        messages = query
        return messages



    def search_email(service, query):
        result = service.users().messages().list(userId='me',q=query).execute()
        messages = [ ]
        if 'messages' in result:
            messages.extend(result['messages'])
        while 'nextPageToken' in result:
            page_token = result['nextPageToken']
            result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
            if 'messages' in result:
                messages.extend(result['messages'])
        return messages



    def parse_parts(service, parts, folder_name, message):
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
                    parse_parts(service, part.get("parts"), folder_name, message)

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
                                print("Saving the file:", filename, "size:", get_size_format(file_size))
                                attachment_id = body.get("attachmentId")
                                attachment = service.users().messages() \
                                            .attachments().get(id=attachment_id, userId='me', messageId=message['id']).execute()
                                data = attachment.get("data")
                                filepath = os.path.join(folder_name, filename)
                                if data:
                                    with open(filepath, "wb") as f:
                                        f.write(urlsafe_b64decode(data))

    def read_message(service, message):
        pass