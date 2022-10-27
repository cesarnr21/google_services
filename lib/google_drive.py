import google.auth
from google_services import GoogleService
import os

class DriveAction(GoogleService):
    """Tutorial here: https://www.thepythoncode.com/article/using-google-drive--api-in-python """
    def __init__(self, creds_file: str = None, auth_file: str = None, notify: bool = False):
        app_scope = ['https://drive.google.com/']
        GoogleService.__init__(self, app_scope, creds_file, auth_file)
        self.notify = notify

    # should this be separate from using using folder?
    def upload_folder(self, folder_name: str, destination: str):
        pass


    def upload(self, file_name: str, destination: str):
        pass


    def create_folder(self, folder_name: str, destination: str):
        pass


    # should this be diffent from a share folder method?
    def share_file(self, file_name: str, destination: str):
        pass


    def download_file(self, file_name: str, destination: str):
        pass


class GoogleSheet(DriveAction):
    def __init__(self, creds_file: str = None, auth_file: str = None, notify: bool = False):
        app_scope = 'place holder look this up'
        DriveAction.__init__(self, app_scope, creds_file, auth_file, notify)
