# Facebook API & SDK

This is a quick guide to get you started on the Facebook JavaScript SDK.

## Table of contents

 - Create a Facebook Application
 - Facebook Graph Explorer
 - Access Tokens & Permissions
 - CRUD Operations in the Facebook Graph API Explorer
 - Code samples using the JavaScript SDK

## Creating A Facebook Application

It's possible to alter Facebook data solely through HTTP requests but the possibilities will remain limited. Becoming a Facebook developer gives you access to extra features such as an SDK which includes Facebook GUI  elements like: sharing, live streaming, ... dialogs.

 - Register yourself as a Facebook developer: https://developers.facebook.com/
 - Click "My Apps" in the top right corner and add a new app.
 - Give it a display name and your e-mail address, press "Create App".

A Facebook app keeps track of stats such as active users during a period and much more.

You now have an app which you can use for a Facebook SDK and even the Graph API Explorer: https://developers.facebook.com/tools/explorer/

## Graph API Explorer

The Graph API Explorer is a tool commonly used for testing and playing with Facebook data.

### Use your app

By default the Graph API Explorer will be selected in the top right corner. This is the same as using the URL in HTTP request, limited. Therefor you should use your (recently made) Facebook application. Another benefit of this is that for example a status update created by this app will mention it's made by your app, free credits?

Here is an example URL for if you would like to test the Graph API Explorer through HTTP requests or just in your browser.
https://graph.facebook.com/DjVDC

Navigate to the URL above and you'll encounter an "OAuthException" telling you that you need an **access token** to request this resource.

## Access Tokens & Permissions

Access tokens are required to get, post, update or delete Facebook data through the Graph API or an SDK. It's the way to authenticate requests.

There are a few different types of access tokens: user tokens, app tokens & page tokens. The difference lies within the access possibilties for example, a user token will allow access to everything you can normally access. Page and app tokens have other perks.

Read more about Facebook's access tokens here: https://developers.facebook.com/docs/facebook-login/access-tokens

### Ways to retrieve an access token

There are several options to retrieve access tokens.

 - Navigate to the Graph API if you haven't already, click the dropdown button **Get Token** and select **Get User Access Token**. If there is something already filled in, in the access token field than this is your **short lived** access token.

You cannot do this with a HTTP request since you'll need an access token to execute the request, if I'm not mistaken. You could get a page token through a HTTP request using your user access token. Or an app token by making a GET request like this (fill it in with your app information):
https://graph.facebook.com/oauth/access_token?client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&grant_type=client_credentials

 - Another option is by logging into Facebook using an SDK. The SDK provides a dialog window prompting for you to log in. In the response you'll find your access token. Later more on that.

Example response:

    {
      status: 'connected',
      authResponse: {
          accessToken: '...',
          expiresIn:'...',
          signedRequest:'...',
          userID:'...'
      }
    }

There might be more ways to retrieve one, feel free to investigate. Either way you'll generate a **short lived** (user or page) access token. This means that it'll expire when you log out of Facebook in any way or if you're logged in for more than about 45 minutes, this means your session has expired. In the Graph API Explorer you'll be prompted to press **ALT + T** to renew your session. In your web application you'll want to ask your user to re-login. Annoying isn't it?

There's a solution for every problem? Well in this case there is. You can exchange your short lived token into a long lived one, this will obviously last longer before it expires. Does this cut the deal for you? It doesn't for me so I'd exchange that long lived token for a permanent token this will never expire (unless you delete your account or targeted Facebook page). 

Follow this link to generate a long lived or permanent access token:
https://stackoverflow.com/questions/17197970/facebook-permanent-page-access-token

Here's a tool for validation your access token, check if it is indeed the token you want:
https://developers.facebook.com/tools/debug/accesstoken

### Permissions

If you deploy an application for multiple users where you use their data or perform actions to their Facebook account, you'll need their permission. This can be done using **scopes**.

When clicking **Get User Access Token** in the Graph API Explorer you might be prompted to select permissions, it will require different permissions / scopes depending on where you want to perform an action:

 - To your own feed (user) it needs: `publish_actions`.
 - To a page: `publish_actions, manage_pages`.
 - To a group: `publish_actions, user_managed_groups`.
 - To an event: `publish_actions, user_events`.

Some data can be accessed without permission, for example the name of a publicly accessible Facebook page.

Some need do permission, for example getting a user's e-mail address.

And some need extra permission by getting your application reviewed by Facebook moderators (this may take days or weeks). There's a similar process for making your Facebook application public, **online** requires an accepted review. An example would be like things in the name of the user, this could be heavily abused so Facebook has to be strict at granting these permissions to app developers.

Here is how to submit a review to get those extra Facebook features for your app: https://developers.facebook.com/docs/apps/review/feature 

## CRUD Operations in the Facebook Graph API Explorer

CRUD litteraly stands for Create (post), Read (get), Update (put) and Delete (delete). These are methods / actions you use to alter or retrieve data.

Let's play around with the Graph API Explorer. Start simple by submitting `me`.

By default you'll retrieve the **fields** name and id.

    {
      "name": "...",
      "id": "1234567891011"
    }

To get data from more fields, you can enter it in the left column in the search field. You'll be assisted by a nice autocomplete box. If you click a field in the autcompletion box, it will be added to your **querystring** to be submitted. This is one of the great features of the Graph API Explorer. But in your own application you shouldn't expect this kind of support. So I'll explain further how it works.

For extra fields you just type them after the `?fields=` parameter, for example: `me?fields=id,name,birthday,picture`. You can also get data from **sub-fields** and even deeper nested data. 
Example: `me?fields=id,name,events{category,place{name,location{street,city}}}`.

When requesting an **array** of data / objects pagination is active with a default limit of 25. You can change this limit, I tested with a limit over 500. Getting a lot data at once would take too long.
Depending on the limit you often retrieve a `paging` object in your response, this holds a **token** for the next and previous page.

Applying a limit: `me?fields=events.limit(10){name,place{location{street,city}}}`

Offsets make it possible to, for example get the data from the second 'page': the 26th element to the 50th.

Applying an offset: `me?fields=events.offset(25){name,place{location{street,city}}}`

And so on, these are usable querystring examples for requesting data through HTTP or code using an SDK but you can execute more CRUD operations ofcourse.

Creating, reading, updating and deleting data on a node (page, post, ...) require different permissions and each node has different fields, for example you can't request the field `PLACE_TYPE` querying on a user. This will return an error in the response.

    {
      error: {
        code: 100,
        type: GraphMethodException,
        message: "The field PLACE_TYPE does not exist on node User"
      } 
    }

## Code samples using the JavaScript SDK

I'll guide you through the flow of setting up the JavaScript SDK to **log a user in** and to make a simple **GET** request.

### Initialize Facebook

This is the trickiest part as you might encounter complex errors.

- First in your HTML make this `<div id="fb-root"></div>` the first element in your body. Facebook needs this to append it's dialogs and modal boxes.

- In your JavaScript, in your `window.load` function or `$(document).ready` or whatever `onLoad` function you prefer. You should execute the Facebook initialize function. This function is called **asynchronously** and might take some time to load so don't think that you can use it instantly.

        window.fbAsyncInit = function() {
          FB.init({
            appId            : 'YOUR_APP_ID_HERE',
            autoLogAppEvents : true,
            xfbml            : true,
            status           : true,
            version          : 'v2.9' // your app version
          });
          FB.AppEvents.logPageView();
          // From here you can use the FB 
        }

- Fill in your app id so the requests go through you app and you can analyze the stats, how or how many times your app is used ect.

Over time certain data becomes irrelevant or dissapears because of security / permission updates, you know how it goes. This is why the **app version** is important so you can can keep track of which fields, permissions, ... become **deprecated** and can no longer be used in your app.

There are a few lesser important options:

        xfbml: true, 

Determines whether **XFBML** tags used by social plugins are parsed, and therefore whether the plugins are rendered or not. Defaults to false.

        cookie: false,

Determines whether a **cookie** is created for the **session** or not. If enabled, it can be accessed by **server-side** code. Defaults to false.

        status: true,

Determines whether the current **login status** of the user is freshly retrieved on every page load. If this is disabled, that status will have to be manually retrieved using .getLoginStatus(). Defaults to false.

Source: https://developers.facebook.com/docs/javascript/reference/FB.init/v2.9

- The next thing to do is to make the **script tag** importing the Facebook SDK JavaScript file. This code comes right after the initialization in your JavaScript file. The script tag is made prepend in your HTML `<head>` section.

        $(function(d, s, id){
           var js, fjs = d.getElementsByTagName(s)[0];
           if (d.getElementById(id)) {return;}
           js = d.createElement(s); js.id = id;
           js.src = "//connect.facebook.net/en_US/sdk.js";
           fjs.parentNode.insertBefore(js, fjs);
         }(document, 'script', 'facebook-jssdk'));

This function will be triggered on load. It will find your first `<script>` element and prepend an new `<script>` element to it with an id of `facebook-jssdk` and a source of `//connect.facebook.net/en_US/sdk.js`. You are free to change the language setting `en_US` to whatever you like, make sure it's in the right format. Another example is: `nl_NL`.

### Log into Facebook

We are now ready to make the log in functionality. We'll prompt the user to login when clicking a button. All prompts and dialogs are pop-up windows and might get blocked by your browser if the user hasn't interacted with your application. So it isn't wise to prompt a user to log in on page load.

- Make a button in your HTML file and make it call `fbLogin()`. This will refer to the function below:

        function fbLogin() {
          FB.login(function(response) {
            if (response.status === 'connected') {
              // you are logged in
              console.log(response)
            } else {
              console.log(response)
            }
          }, { scope: 'user_videos, user_photos' });
        }

If the response status equals `connected`, you'll be logged in successfully. Else you should handle your error. If you get an error like `FB init is not defined ...` in you **browser console**, you might have tried to use the SDK functionality (FB) before the **asynchronous** function has completed. This is another reason for why you shouldn't execute SDK functionality directly on page load.

You can see **scopes** requested at the login. This will prompt the user to grant or deny permissions for your app.

Find more functionality here: 

More about the scopes and other options: https://developers.facebook.com/docs/reference/javascript/FB.login/v2.9

The response will look like this if it was successful:

        {
          status: 'connected',
          authResponse {
            userID: 123546879,
            accessToken: EEEgopjergog4r56e465rg46e56...,
            expiresIn: ...,
            signedRequest: ...
          },
          ...
        } 

This **access token** is important for further requests.

### A simple GET request

Let's make a simple GET request to get your id, name and **1** of your events with it's location and name, make sure you fill in your **access token**:

        function fbGET() {
          FB.api('/me?fields=id,name,events.limit(1){name,place{location{street,city}}}&access_token=YOUR_ACCESS_TOKEN', function(response) {
            if(response && !response.error){
              // successfully retrieved 

            } else {
              // an error occured!
              console.log(response.error)
            }
          })
        }

If succesful, the response will result in a JSON object with the requested data. Else it will give you a JSON response aswell but with an error object. Example:

    {
      error: {
        code: 100,
        type: GraphMethodException,
        message: "The field PLACE_TYPE does not exist on node User"
      } 
    }

More about errors can be found here: https://developers.facebook.com/docs/graph-api/using-graph-api/#errors

## Extra information - more limitations

You can request a **max. of 50 ids at once**.
Example:

        FB.get('/ids=<50NumericIdsSplitByCommaHere>,...&fields=...&access_token=...', function(response) {

        });

There also is a limitation on requests **per second** so if you tend to execute request in a loop you should definitly use a time out of some sort.

## Foot Note

The rest is up to you, goodluck!
  *Experience makes perfect*

Written by Auguste Van Nieuwenhuyzen for educational purpose. Feel free to copy my work!