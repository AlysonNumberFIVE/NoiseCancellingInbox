from __future__ import print_function
import base64

from bs4 import BeautifulSoup
import os.path
import os
import re
import sys
import time

import ignore
import utils


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Max amount of messages to pull from your inbox.
MAX_MESSAGES = 30 

# Max amount of tokens to group messages by. GPT-4 has an upper limit of 8000-ish tokens at a time.
# For optimal performance, GPT-4-32K is recommended where this number can be pushed up to 30,000
MAX_TOKEN_COUNT = 3000 

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def clean_email_body(body):
    """
    Refines the email body to save on the number of GPT tokens used.
        It removes things like the footer and the greeting.
    :param: body: The email body.
    :return: The refined email body with all the needless details
        stripped away.
    """
    
    # Remove footer
    footer_phrases = ["Unsubscribe", "To stop receiving these emails"]
    for phrase in footer_phrases:
        body = body.split(phrase)[0]
    
    # Remove salutations
    salutations = ["Dear", "Hi", "Hello"]
    for salutation in salutations:
        body = re.sub(r'{} [A-Za-z,]*'.format(salutation), '', body)
    
    # Remove email signatures
    body = re.sub(r'--.*', '', body, flags=re.DOTALL)  # remove everything after "--"
    body = re.sub(r'(Best|Sincerely|Regards|Cheers),?.*', '', body, flags=re.DOTALL)  # remove everything after common sign-offs
    
    # Replace newline and carriage return with space
    body = re.sub(r'\n+', '\n', body)
    body = re.sub(r'\r+', '\r', body)
    body = re.sub(r'\(\s*\)', '', body)
    return body
    

def gmail():
    """
    Extract up to 100 emails from the user's logged in Gmail account.
    """

    token_count = 0
    email_objects = []
    data_body = ''
    creds = None
    # This first part is rudimentary Gmail API setup and is copied verbatim from the
    # quickstart

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # The Maybe starts from here onwards
        service = build('gmail', 'v1', credentials=creds)

        # Call the Gmail API to fetch inbox
        last_monday_date = utils.last_monday()
        results = service.users().messages().list(
            userId='me',
            q=f'after:{last_monday_date}',
            labelIds = ['INBOX']
        ).execute()

        messages = results.get('messages',[])

        if not messages:
            print("No new messages.")
        else:
            message_count = 0
            for message in messages:
            
                sender = 'Unknown'
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                headers = msg['payload']['headers']
                for values in headers:
                    name = values['name']
                    if name == 'From':
                        sender = values['value']
                    if name == 'Subject':
                        subject = values['value']

                        # Ignore emails with certain keywords in the subject
                        if any(keyword in subject.lower() for keyword in ignore.keywords):
                            continue

                from_field = next(header for header in headers if header["name"] == "From")
                sender_email = from_field["value"]
                subject = next(header for header in headers if header["name"] == "Subject")["value"]
                date = next(header for header in headers if header["name"] == "Date")["value"]

                # Ignore emails from specific senders
                from_field = next(header for header in headers if header["name"] == "From")
                sender_email = from_field["value"]
     
                if any(sender in sender_email for sender in ignore.addresses):
                    continue
                   
                if 'parts' in msg['payload']:
                    # Aggressive defense
                    payload = msg.get('payload', {})
                    parts = payload.get('parts', [{}])
                    body = parts[0].get('body', {})
                    data = body.get('data', '')
                else:
                    data = msg['payload']['body']['data']

                data = data.replace("-","+").replace("_","/")
                decoded_data = base64.b64decode(data)
                soup = BeautifulSoup(decoded_data, "html.parser")
                body = utils.remove_urls(clean_email_body(soup.get_text()))
                token_count += utils.num_tokens_from_string(f'Sender: {sender}\nSubject: {subject}\nDate: {date}\nBody: {body}\n\n')

                data_body += f'Sender: {sender}\nSubject: {subject}\nDate: {date}\nBody: {body}\n\n'

                if token_count >= MAX_TOKEN_COUNT:
                    email_objects.append(data_body)
                    data_body = ''
                    token_count = 0

                message_count += 1
                if message_count == MAX_MESSAGES: 
                    break

    except HttpError as error:
        print(f'zsh: Segmentation fault ./{sys.argv[0]}')
        time.sleep(3)
        print(f'Jk, real error: {error}')
        sys.exit(1)

    if len(data_body) > 0:
        email_objects.append(data_body)
 
    return email_objects
