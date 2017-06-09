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

# 1. Creating

If you haven't already, navigate to the Graph API Explorer: https://developers.facebook.com/tools/explorer/

1.1 Click the dropdown button with "Graph API Explorer" and select your (created) app.

1.2 Click "Get Token" to retrieve a user or page access token.

You'll be prompted to select permissions, we'll continue without so click "Get Access Token".

A "short lived" access token appears, short lived means that it'll  


2. Reading
3. Updating
4. Deleting
5. Viewer Experience



src: https://developers.facebook.com/docs/videos/live-video/getting-started

