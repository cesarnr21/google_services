import google.auth
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle


class GoogleService():
    def __init__(self, app_scope: list[str], creds_file: str = None, auth_file: str = None,) -> None:
        """
        eliminate the verification proccess
        docs here: https://www.thepythoncode.com/article/use-gmail-api-in-python 
        """

        self.creds = None
        if os.path.exists(auth_file):
            with open(auth_file, 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())

            else:  
                flow = InstalledAppFlow.from_client_secrets_file(creds_file, app_scope)
                self.creds = flow.run_local_server(port = 0)


            with open(auth_file, 'wb') as token:
                pickle.dump(self.creds, token)

