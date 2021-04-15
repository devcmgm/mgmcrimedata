#
#  Simple Email Reader
#

# [START gmail_quickstart]
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys
import base64

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
types = [ "Arson", "Assault", "Burglary", "Disturbing the Peace", "Drugs / Alcohol Violations", "DUI", "Fraud", "Homicide", "Motor Vehicle Theft", "Robbery", "Sex Crimes", "Theft / Larceny", "Vandalism", "Vehicle Break-In / Theft", "Weapons"]


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    user_id =  'me'


    final_list = [ ]

    sys.stdout.flush()
    rows = 0
    print("Report_Id,Crime_Type,"",Crime_Detail,Year_Key,Street_Address,Datetime")

    response = service.users().messages().list(userId=user_id,
                                                           labelIds=['Label_984599473385438091'],
                                                           maxResults=15500).execute()
    messages = []
    if 'messages' in response:
        messages.extend(response['messages'])
        for email in messages:
            msg_id = email['id']
            message = service.users().messages().get(userId=user_id, id=msg_id,format='raw' ).execute()
            msg_str = str(base64.urlsafe_b64decode(message['raw'].encode('ASCII')))

            waitForNext = False;

            crimeline = "";

            linepre = msg_str.replace('\\n', '\n').replace('\\r','');
            i = 0;
            for linestr in linepre.splitlines():

                if ( linestr in types or waitForNext):

                   #print(linestr)
                   i = i + 1;
                   if ( i > 5 ):
                      waitForNext = False;
                      crimeline = '"' + msg_id + '",' + crimeline + '"' + linestr + '"';
                      print(crimeline);
                      crimeline = ""
                      i = 0;
                   else:
                      waitForNext = True;
                      crimeline = crimeline + "\"" + linestr + "\","


    sys.stdout.flush()


if __name__ == '__main__':
    main()
