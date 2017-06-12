# Auguste's Documentation

# Make a new app

Make a new app in the dashboard.

1. Copy the app_template and rename the folder.
2. Rename the HTML file in /templates to <the folder's name>.html
3. Modify the config params in __init__.py, set a display name and color for your app.

# Posting a form (data-bind Knockout.JS)

1. 

# Posting data through AJAX

1.

# Post array to tweepy
[u'#opsoro']
bij elke post eerst Twitter stream stoppen


# Investigate Tweepy Response
response object

# Send Tweepy object to JS -> python Users socket
Alter js funtions to pass in tweet text
Custom addLine() function

# Autoloop voicelines
import opsoro/sound lib
recursieve functie met index_voiceline++ wachten op soundStopped
Start - Post to Python - Response from Python - Running, Next - Stop?

$root.prop != $root.prop() -> runs at start

# Locked = true for lay-out

# JS loop to Python loop with Stoppable Thread

# Convert social username to ID

# Issues

Zie pics

# Facebook Live ft. ONORobot

We'll create a Facebook live video using their API and make the ONORobot react to the view count, comments maybe, ...

# Prequisites, create a Facebook app

Follow these steps if you have no Facebook app yet:

1. Go to: https://developers.facebook.com/
2. Click "My Apps" in the top right corner and add a new app.
3. Give it a display name and your e-mail address, press "Create App".

You now have an app which you can use for the Graph API Explorer: https://developers.facebook.com/tools/explorer/

# Graph API Explorer

The Graph API Explorer is a tool commonly used for testing and playing with Facebook data. We'll use it for creating a live video.

## 1. Creating

### Use your app

If you haven't already, navigate to the Graph API Explorer: https://developers.facebook.com/tools/explorer/

1.1 Click the dropdown button with "Graph API Explorer" and select your (created) app.

### Get a token

1.2 Click "Get Token" to retrieve a user or page access token.
You could live stream a video on your own feed, on a page, on a group or on an event.

1.3 You'll be prompted to select permissions, it will require different permissions depending on where you want to post the video:

To your own feed (User) it needs: publish_actions.
To a page: publish_actions, manage_pages.
To a group: publish_actions, user_managed_groups.
To an event: publish_actions, user_events.

1.4 Check the permissions you need and click "Get Access Token" to continue.

A "short lived" access token appears, short lived means that it will vanish when you log-out or when your session expires (ca. 45 minutes)
If you need a token that lasts longer or doesn't expire, you can follow this link:
https://stackoverflow.com/questions/17197970/facebook-permanent-page-access-token

### POST request

Perform a POST request to create a Facebook live stream.

1.5 Underneath your access token to the left, you'll see a book icon (examine it if you feel like). To the right of the book icon, you see the word "GET", change it to "POST" by clicking it.

1.6 In the query field you'll see something like this "me?fields=id,name", change it to "me/live_videos" or "<your-page-id>/live_videos" and click "Submit"

This should return an object with an id, and stream urls in RTMP format.
You have now created a Facebook live stream but external software is needed to record your stream.

Something like this:
{
  "id": "1548733171824663",
  "stream_url": "rtmp://rtmp-api.facebook.com:80/rtmp/1548733171824663?ds=1&s_l=1&a=ATghSBT1Dp_Gp7Rh",
  "secure_stream_url": "rtmps://rtmp-api.facebook.com:443/rtmp/1548733171824663?ds=1&s_l=1&a=ATghSBT1Dp_Gp7Rh",
  "stream_secondary_urls": [
  ],
  "secure_stream_secondary_urls": [
  ]
}

### Open Broadcasting Software

OBS (Open Broadcasting Software) is referenced to and shown in the Facebook documentation, download link: https://obsproject.com/download

Follow this link to set-up OBS: https://github.com/jp9000/obs-studio/wiki/Install-Instructions

Once it's downloaded an "Auto-Configuration Wizard" will pop-up, make good use of this. Make sure you set the streaming service to "Facebook Live". Enter your stream url and key. You can retrieve this key through a Facebook dialog but you can also just fetch it from your stream url.

Example: "stream_url": "rtmp://rtmp-api.facebook.com:80/rtmp/1548733171824663?ds=1&s_l=1&a=ATghSBT1Dp_Gp7Rh"

The part after "/rtmp/" is your stream key, so "1548733171824663?ds=1&s_l=1&a=ATghSBT1Dp_Gp7Rh".
The first part refers to your user, page, group or event id.

### Problem
OBS didn't want to connect so I'll approach it differently.

### Facebook built-in stream widget (solution)

1. Open another window (don't close the Graph API Explorer) and navigate to the desired facebook profile, page, group or event owned by you and start a live video.

## 2. Reading
2. In the Graph API Explorer, query "<facebook-id>/live_videos" example: "me/live_videos", press submit. You should see your video listed where "status" is "LIVE", click on the id
and press submit again to get the specific data for that video.

We'll work with the views & comments of the live video.
Add fields to get specific data, example: "<live_video-id>?fields=live_views,comments".

this will result in something like this:

{
  "comments": {
    "data": [
      {
        "from": {
          "name": "Auguste Van Nieuwenhuyzen",
          "id": "1548926531805327"
        },
        "message": "Mooi",
        "id": "10209691024654989_10209691105297005"
      },
      {
        "from": {
          "name": "Auguste Van Nieuwenhuyzen",
          "id": "1548926531805327"
        },
        "message": "Ok",
        "id": "10209691024654989_10209691105857019"
      }
    ],
    "paging": {
      "cursors": {
        "before": "WTI5dGJXVnVkRjlqZAFhKemIzSTZANVEF5TURrMk9URXhNRFV5T1Rjd01EVTZANVFE1TnpJM016a3lOdz09",
        "after": "WTI5dGJXVnVkRjlqZAFhKemIzSTZANVEF5TURrMk9URXhNRFU0TlRjd01UazZANVFE1TnpJM016a3pOZAz09"
      }
    }
  },
  "live_views": 1,
  "id": "10209691024734991"
}

This is usable data for the ONORobot, let's make the app!

Side Notes:
RTMP (Real-time Messaging Protocol): https://en.wikipedia.org/wiki/Real-Time_Messaging_Protocol

src: https://developers.facebook.com/docs/videos/live-video/getting-started

# ONORobot




