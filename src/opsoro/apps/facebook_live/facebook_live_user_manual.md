












----------------------------------------------------------------------

### Open Broadcasting Software

OBS (Open Broadcasting Software) is referenced to and shown in the Facebook documentation, download link: https://obsproject.com/download

Follow this link to set-up OBS: https://github.com/jp9000/obs-studio/wiki/Install-Instructions

Once it's downloaded an "Auto-Configuration Wizard" will pop-up, make good use of this. Make sure you set the streaming service to "Facebook Live". Enter your stream url and key. You can retrieve this key through a Facebook dialog but you can also just fetch it from your stream url.

Example: "stream_url": "rtmp://rtmp-api.facebook.com:80/rtmp/1548733171824663?ds=1&s_l=1&a=ATghSBT1Dp_Gp7Rh"

The part after "/rtmp/" is your stream key, so "1548733171824663?ds=1&s_l=1&a=ATghSBT1Dp_Gp7Rh".
The first part refers to your user, page, group or event id.

### Problem

OBS didn't want to connect so I'll approach it differently.

### Facebook built-in stream widget (solution?)

1. Open another window (don't close the Graph API Explorer) and navigate to the desired facebook profile, page, group or event owned by you and start a live video.

You'll get a screen like this:
<img here>

2. At the bottom right corner (marked red) there's an option to stream with external software (OBS, ...), click it. This might be useful if you want to show more than just the your face ... for example your desktop while gaming and yourself in the bottom right or left corner giving live commentary.

3. Click "make livestream" this results in a modal window where you can enter a video title and get your stream key. If not already, start OBS, go to settings, select "Facebook Live" as service and paste your stream key.

4. Back in the Facebook window, set the access level (public recommended) and go live! 


## 2. Reading

1. In the Graph API Explorer, query "<facebook-id>/live_videos" example: "me/live_videos", press submit. You should see your video listed where "status" is "LIVE", click on the id
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

### 1. Paste your access_token
### 2. Get Request me/live_videos, this will result into something like this:
  {
    "data": [
      {
        "title": "Niks te zien, test voor project! (zwart scherm)",
        "status": "LIVE",
        "stream_url": "rtmp://rtmp-api.facebook.com:80/rtmp/1550981988266448?ds=1&s_l=1&a=AThG-5FPYt7Uf8YD",
        "secure_stream_url": "rtmps://rtmp-api.facebook.com:443/rtmp/1550981988266448?ds=1&s_l=1&a=AThG-5FPYt7Uf8YD",
        "embed_html": "<iframe src=\"https://www.facebook.com/plugins/video.php?href=https%3A%2F%2Fwww.facebook.com%2Fauguste.vannieuwenhuyzen%2Fvideos%2F1550981984933115%2F&width=1280\" width=\"1280\" height=\"720\" style=\"border:none;overflow:hidden\" scrolling=\"no\" frameborder=\"0\" allowTransparency=\"true\" allowFullScreen=\"true\"></iframe>",
        "id": "1550981988266448"
      }
    ],
    "paging": {
      "cursors": {
        "before": "MTU1MDk4MTk4ODI2NjQ0OAZDZD",
        "after": "MTU1MDk4MTk4ODI2NjQ0OAZDZD"
      }
    }
  } 


#### 2.1. Send response from python to JS & validate it there. 


### 3. Filter out live video (status="LIVE"), get it's ID
    Send back video IDs of the live videos only with a post to python, (in python) get their data with a graph request

#### 3.1 Set lay-out with live_video data -> embed iFrame error: this video can't be embed (not embeddable while streaming?)
      Works when going through OBS, sometimes ?!

### 4. Use ID for Facebook call for comments & views
    get request for live_views & comments

### 5. Get the data every 2 seconds and bind to lay-out to show up to date data (through sockets to JS). 
    Why fetching all the comments over and over? Because comments might be deleted, edited and added. This way you don't have to make complex checks nor will you see comments that were deleted on Facebook but not on our app.




## Facebook Login, pages, videos, feed with SDK

Add your test domain url to FB app




Extra: Multiple videos ? Display all, check the one you want

