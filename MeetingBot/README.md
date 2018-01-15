# MeetingBot
Python script to monitor Google Calendar for upcoming events and post details in a GroupMe chat (or any other supported chat service) via IFTTT.

## Overview
The script uses the [Google Calendar API](https://developers.google.com/google-apps/calendar/quickstart/python) to monitor a specified calendar. 
If there are any events (up to 10) scheduled to begin within 24 hours, it generates a message with event details suitable for posting to a group chat. 
The message is then sent to IFTTT via their [maker channel](https://ifttt.com/maker).
I set up a recipe to post the message to a GroupMe group (and later a Slack channel), but it could easily be sent to other services supported by IFTTT.

## Setup
1. Set up the Google Calendar API and install the Python library per [this guide](https://developers.google.com/google-apps/calendar/quickstart/python).
2. Find the ID of the calendar you want to use at [this page](https://developers.google.com/google-apps/calendar/v3/reference/calendarList/list) and substitute that ID in the appropriate place in the script.
3. Install the [pyshorteners](https://github.com/ellisonleao/pyshorteners) library.
4. Get a Google URL Shortener API key and save it as "URLShortenerKey" (a plaintext file, with no file extension) in the same directory as the script.
5. Configure an IFTTT recipe using the maker channel that recieves the message and posts it to the chat service fo your choice. See a sample recipe [here](https://ifttt.com/recipes/463791-meetingbot-sample-recipe).
6. Configure the script to run once every 24 hours (i.e., via [cron](https://en.wikipedia.org/wiki/Cron))

## Why?
Since Google Calendar integrates directly with IFTTT, you're probably wondering why I bothered to write a python script to do this.
Google Calendar offers thre IFTTT triggers: "Any event starts," "Event from search starts," and "Any new event added." So I can
post a message when an event is about to start, or when I create an event, but what I really want to do is post a reminder in 
GroupMe the day before an event starts. A previous workaround was to have Google Calendar send me an email notification the day
before an event, to which Gmail applied a special label via a filter I set up. IFTTT watched for new emails with this label (via its gmail
integration) and this triggered the message to be sent. However, the only data about the event I could really include in those messages
was the subject lines of those emails, which were of the following format:

>Upcoming Event Notification: Testing @ Tue Dec 22, 2015 4:47pm - 5:47pm (Testing Calendar)

While this worked, the resulting messages weren't very pretty, and I found the workaround rather inelegant. So I decided to write my own
Python script (based on Google's sample code) to monitor Google calendar, and trigger an event using IFTTT's Maker Channel, which
results in a GroupMe message being sent. The script generates the message itself, and passes it to IFTTT, so I can format the
messages better and customize what data to include, like this:

>This is an automated reminder for the event "Testing," scheduled for Tuesday, December 29, 2015 (tomorrow) from 11:00 PM to 11:30 PM at the location "Dummy Location". For more information, click this link: https://goo.gl/rlVI2b

Much Better.


