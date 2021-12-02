from __future__ import print_function

import datetime
import os.path
import re
from datetime import *
from dateutil import tz

from dateutil.parser import *
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('America/New_York')


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def google_auth():
    """ Taken almost directly from Google's quick-start guide:
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    credentials = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Got rid of the lines below because they forced re-authenticating via browser.

    # # If there are no (valid) credentials available, let the user log in.
    # if not credentials or not credentials.valid:
    #     if credentials and credentials.expired and credentials.refresh_token:
    #         credentials.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'credentials.json', SCOPES)
    #         credentials = flow.run_local_server(port=0)
    #     # Save the credentials for the next run
    #     with open('token.json', 'w') as token:
    #         token.write(credentials.to_json())

    service = build('calendar', 'v3', credentials=credentials)
    return service


def check_schedule(service, calendarId):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    event_list = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start = parse(start).strftime("%m/%d/%Y %H:%M")

        end = event['end'].get('dateTime', event['end'].get('date'))
        event_name = event['summary']
        start_id = event['summary'] + ' starts: ' + start + '\n'
        end_id = end + event['summary']
        event_list.append(start_id + '\n')

    return event_list


def add_to_schedule(service, text):
    name = re.search("-n(.*?)-s", text).group(1)

    unparsed_start = re.search("-s(.*?)-e", text).group(1)
    parsed_start = datetime.strftime(parse(unparsed_start), "%Y-%m-%dT%H:%M:%S")
    start = {'dateTime': parsed_start,
             'timeZone': 'America/New_York'}

    unparsed_end = ''.join(text[text.index('-e') + 3:])
    parsed_end = datetime.strftime(parse(unparsed_end), "%Y-%m-%dT%H:%M:%S")
    end = {'dateTime': parsed_end,
           'timeZone': 'America/New_York'}

    event = {
        'summary': name,
        'start': start,
        'end': end
    }

    service.events().insert(calendarId='primary', body=event).execute()
    return 'Added!'
