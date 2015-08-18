import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime
import json

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print 'Storing credentials to ' + credential_path
    return credentials

def getEvents(date):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    calendars = service.calendarList().list().execute()
    #print json.dumps(calendars)
    #calendars = calendars.get('items', []).execute()
    #for calendar in calendars['items']:
        #print 'summary: ' + calendar['summary']
        #print 'ID: ' + calendar['id']
        #events = calendar.get('events', []).execute()
        #print events
    #calendar = service.calendars().get(calendarId='pint.com_8rrqqnt01l8pq36npf3db3crjs@group.calendar.google.com').execute()
    if date:
        now = date
        print 'using date argument: ' + str(date)
    else:
        print 'generating now() date'
        now = datetime.datetime.now()
    nowMin = now.isoformat() + '-09:00'
    print 'now min: ' + now.isoformat() + '-09:00'
    now = now.replace(hour=(now.hour + 1))
    nowMax = now.isoformat() + '-09:00'
    print 'now max: ' + now.isoformat() + '-09:00'

    events = service.events().list(calendarId='pint.com_8rrqqnt01l8pq36npf3db3crjs@group.calendar.google.com', timeMin=nowMin, timeMax=nowMax, showDeleted=False, singleEvents=True).execute()
    returnList = []
    for event in events['items']:
        #print event['id']
        event = service.events().get(calendarId='pint.com_8rrqqnt01l8pq36npf3db3crjs@group.calendar.google.com', eventId=event['id']).execute()
        print event['start']['date']
        print event['summary']
        returnList.append(event['summary'])
    return returnList


def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print 'Getting the upcoming 10 events'
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print 'No upcoming events found.'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print start, event['summary']


if __name__ == '__main__':
    getEvents()
