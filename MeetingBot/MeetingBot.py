from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime
from pyshorteners import Shortener

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

shortenerAPIKey = open("URLShortenerKey", "r").read()

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
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def prepareForUseAsURL(someText):
    """
        prepares someText for use as a URL by replacing the special characters ()" and space with their
        HTML encoding equivalents
    """
    someText=someText.replace(" ","%20")
    someText=someText.replace("(","%28")
    someText=someText.replace(")","%29")
    someText=someText.replace("\"","%22")
    return someText

def generateMessage(event, delta):
    """
        Generates a message to be sent based on an event and the time
        to the event (in days)
    """
    message = "This is an automated reminder for the event \""
    message += str(event['summary'])
    message += ",\" scheduled for "
    eventDate = datetime.datetime.strptime(event['start'].get("dateTime")[0:10], "%Y-%m-%d").date() #create date object
    message += str(eventDate.strftime("%A, %B %d, %Y")) #format event date so it looks pretty
    if delta == datetime.timedelta(days=1): #relation to current day
        message += " (tomorrow) "
    elif delta == datetime.timedelta(days=0):
        message += " (today) "
    message += "from "
    eventStartTime = datetime.datetime.strptime(event['start'].get("dateTime")[11:16], "%H:%M") #create event start time object
    message += str(eventStartTime.strftime("%I:%M %p")) #format start time so it looks pretty
    message += " to "
    eventEndTime = datetime.datetime.strptime(event['end'].get("dateTime")[11:16], "%H:%M") #create event end time object
    message += str(eventEndTime.strftime("%I:%M %p")) #format end time so it looks pretty
    message += " at the location \""
    message += str(event['location']) #event location
    message += "\". For more information, click this link: "
    eventURL = str(event['htmlLink']) #Google Calendar Web View link to event
    shortener = Shortener('GoogleShortener', api_key=shortenerAPIKey) #set up event shortener
    message += shortener.short(eventURL) #add shortened URL to GCal event
    return prepareForUseAsURL(message)

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='2l1q01jmkfotg6flkcask9glv8@group.calendar.google.com', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        return
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))[0:10]
        #print(event['summary'])
        eventDate = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        todaysDate = datetime.date.today()
        delta = eventDate - todaysDate
        if ((delta == datetime.timedelta(days=1)) or (delta == datetime.timedelta(days=0))):
            messageBody = generateMessage(event, delta)
            #print(messageBody)
            terminalCommandToExcecute = "curl -X POST https://maker.ifttt.com/trigger/{sci_oly_event}/with/key/bMrFgIC-rvsYHAQUkiimCV?value1="+messageBody
            os.system(terminalCommandToExcecute)


if __name__ == '__main__':
    main()