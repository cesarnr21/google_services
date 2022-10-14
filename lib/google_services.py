
from copyreg import pickle


class google_service():
    def __init__(self, creds_file, app_scope):
        import google.auth
        from googleapiclient.discovery import build
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request

        """eliminate the verification proccess"""
        """docs here: https://www.thepythoncode.com/article/use-gmail-api-in-python """
        import os, sys
        sys.path.append(__file__[:-len('lib/google_services.py')])
        import pickle

        self.creds = None
        if os.path.exists('ceres_token.pickle'):
            with open('ceres_token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())

            else:  
                flow = InstalledAppFlow.from_client_secrets_file(creds_file, app_scope)
                self.creds = flow.run_local_server(port = 0)


            with open('ceres_token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

