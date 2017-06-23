# Treader

## documentation tweepy
For tweepy all the documentation is on this page: http://docs.tweepy.org/en/v3.5.0/
</br>
We also looked in the source-code with you can find: https://github.com/tweepy/tweepy


## getting twitter key

1. go to https://apps.twitter.com
2. create your app
3. go to "keys and tokens"
4. create an access tokens
5. now you have an consumer key, consumer secret, access token and a access token secret

## tweepy stream

1. don't forget to import the tweepy library in the __init__.py file
  ```
  import tweepy
  ```
2. authenticate with your api keys

  ```
  access_token = {your_access_token}
  access_token_secret = {your_access_token_secret}
  consumer_key = {your_consumer_key}
  consumer_secret = {your_consumer_secret}

  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  api = tweepy.API(auth)
  ```
3. Create a stream object and a listener
  ```
  myStreamListener = MyStreamListener()
  myStream = tweepy.Stream(auth=api.auth,listener=myStreamListener)

  class MyStreamListener(tweepy.StreamListener):
      def on_status(self, status):
        dataFromTweepy = status
  ```
4. start the twitter stream

  tracking twitter words
  ```
  global myStream
  myStream.filter(track={twitterWords}, async=True)
  ```
  target a users
  ```
  global myStream
  myStream.filter(follow={userId}, async=True)
  ```

5. stop the twitter stream

  don't forget to stop your stream to save server load. The stream will close once a new tweet has come in. There is no workaround for this.
  ```
  global myStream
  myStream.disconnect()
  ```

## sending profile picture and url
 To make the front-end more attractive we decided to show the profile picture of the tweet and make it click-able.
 To do so we send some extra content from the json we get to our javascript: ["user"]["screen_name"] and ["user"]["profile_image_url_https"]

  The profile picture is just a simple img object with the src you get from twitter.

  Around the img we made an a object and the href = www.twitter.com/ {username}



## Multi language
  PlayTweetInLanguage takes 2 arguments and plays the text in that language.

  ```
  def playTweetInLanguage(text, lang):
    print_info("play tweet in language")
    if not os.path.exists("/tmp/OpsoroTTS/"):
        os.makedirs("/tmp/OpsoroTTS/")

    full_path = os.path.join(get_path("/tmp/OpsoroTTS/"), "Tweet.wav")
    print_info(full_path)

    TTS.create_espeak(text, full_path, lang, "f", "5", "150")
    Sound._play(full_path)
  ```
## auto reader comments
Autoreader is a boolean that knows when the user selected the "auto read tweet" function. <br/>
You get the value when starting the stream and when the user changes the value in javascript.<br/>
When you get a tweet from the stream it will check the value and play the tweet if necessary.

## playtweet
To play a tweet we use different functions:
### playtweet(tweepyDataModel)
Here we prepare everything to start an async function. We make sure there is no tweet playing and set the correct language. We also call a function getPlayArray(tweepyDataModel). To make a readable array with emoticons and text.
```
def playTweet(tweepyDataModel):
    global loop_PlayTweet
    if not loop_PlayTweet == None:
        loop_PlayTweet.stop()
        print_info('zou ook moeten stoppen')
    global lang
    global tweetArrayToPlay
    lang = tweepyDataModel['text']['lang']
    tweetArrayToPlay = getPlayArray(tweepyDataModel)
    loop_PlayTweet = StoppableThread(target=asyncReadTweet) #start playing Tweet

```
### getPlayArray(tweepyDataModel)
This function takes tweepyDataModel and makes an array that split text and emotions. </br>
It checks every char in the text. If there is an emoticon it will append the output with ['emj',{emotion}]
</br>
When there is no emotion it will check if it needs to add a char or if it is the first char of a new part of text. </br>
The return value is an 2 dimensional array: [[{emj or text}, {the emotion or a piece of text}], ...]
This output can be played by the asyncPlayTweet() function.
```
def getPlayArray(status):
    output = []
    teller = -1
    previousWasText = False
    emoticonStr = status["text"]["original"]
    for text in emoticonStr:
        emotions = []
        winking = len(re.findall(u"[\U0001F609]", text))
        angry = len(re.findall(u"[\U0001F620]", text))
        happy_a = len(re.findall(u"[\U0000263A]", text))
        happy_b = len(re.findall(u"[\U0000263b]", text))
        happy_c = len(re.findall(u"[\U0001f642]", text))
        thinking = len(re.findall(u"[\U0001F914]", text))
        frowning = len(re.findall(u"[\U00002639]", text))
        nauseated = len(re.findall(u"[\U0001F922]", text))
        astonished = len(re.findall(u"[\U0001F632]", text))
        neutral = len(re.findall(u"[\U0001F610]", text))
        fearful = len(re.findall(u"[\U0001F628]", text))
        laughing = len(re.findall(u"[\U0001F603]", text))
        tired = len(re.findall(u"[\U0001F62B]", text))
        sad = len(re.findall(u"[\U0001f641]", text))

        if winking > 0:
            emotions.append("tong")
        if angry > 0:
            emotions.append("angry")
        if happy_a > 0 or happy_b > 0 or happy_c > 0:
            emotions.append("happy")
        if frowning > 0:
            emotions.append("tired")
        if nauseated > 0:
            emotions.append("disgusted")
        if astonished > 0:
            emotions.append("surprised")
        if neutral > 0:
            emotions.append("neutral")
        if fearful > 0:
            emotions.append("afraid")
        if laughing > 0:
            emotions.append("laughing")
        if tired > 0:
            emotions.append("sleep")
        if sad > 0:
            emotions.append("sad")

        if not emotions:
            #this is a text obj
            if not previousWasText:
                teller = teller + 1
                output.append([])
                output[teller].append("txt")
                output[teller].append(text)
            else:
                output[teller][1] += text

            previousWasText = True
        else:
            #this is an emoticon
            teller += 1
            output.append([])
            output[teller].append("emj")
            output[teller].append(emotions[0])
            previousWasText = False


    return output

```

### asyncReadTweet()
The function takes the tweetArrayToPlay and plays it correctly.
</br>
It takes every peace of the array and checks if it's an emoticon or a peace of text.
When it's text it has to wait until the text is played. After that it takes the next piece and so on.
</br>
It also checks the if the autoloop is enabled so it can play the next tweet.
</br>
This function has to be a new tread because of the "wait_for_sound" function
 ```
 def asyncReadTweet():
    time.sleep(0.05)
    global loop_PlayTweet
    global tweetArrayToPlay
    global lang
    global autolooping
    while not loop_PlayTweet.stopped():
        for item in tweetArrayToPlay:
            if item[0] == 'txt':
                playTweetInLanguage(filterTweet(item[1]), lang)
                Sound.wait_for_sound()
            else:
                Expression.set_emotion_name(item[1], -1)
        loop_PlayTweet.stop()
        print_info(autolooping)
        if autolooping == 1:
            send_action("autoLoopTweepyNext")
 ```

 ## Autoloop
 ### Backend
 To make the autoloop work we use a boolean that knows when it's running. After a tweet is played it checks the value and sends a socket to the client side who then sends a new playtweet command to the server.

## Close connections from client
Because we work with streams it's possible there is an open connection with twitter when closing the browser. To avoid tweepy is still running we use an ajax function ".unload()". Here we send the action "stopTweepy" to disconnect the stream.


```
$( window ).unload(function() {
  $.ajax({
    dataType: 'json',
    type: 'POST',
    url: '/apps/facebook_live/',
    data: {action: 'stopTweepy', data: {} },
    success: function(data){
      if (!data.success) {
        showMainError(data.message);
      } else {
        return "";
      }
    }
  });
  return "";
});
```

# Facebook live
## Reacting to comments and reading comments
In the handleLayout() function it checks if there was a new comment and then simply sends an request to the server to play the sound. It also needs to check if the option is enabled. After that it goes to the playEmotion() function which handles the emotions().

```
if(self.comments().length > 0 && self.comments()[0]['id'] != arr_comments[arr_comments.length - 1]['id']){
    if(self.autoRead()){
      console.log("autoread")
      //send last comment to read out loud
      robotSendTTS(arr_comments[arr_comments.length -1]["message"]);
    }
    self.playEmotion();
    self.comments(arr_comments.reverse());
}
```
The playEmotion() function gets the selected item in the combo box. If it's -1 the option 'None' is selected and nothing needs to happen. If the option "Random" is selected it will select a random index from the emotions array to the server. Else there is an index selected of an available emotion, the index needs to be -1 because there is an value 'random' added.

```
self.playEmotion = function(){
  var emotion = self.selectedEmotion();
  if(emotion['index'] != -1){
    if(emotion['index'] == 0){
      var random = Math.floor(Math.random() * emotions_data.length);
      robotSendEmotionRPhi(1.0, emotions_data[random].poly * 18,-1);
    }
    else {
      robotSendEmotionRPhi(1.0, emotions_data[emotion['index'] -1].poly * 18, -1);
    }
  }
}
```

## Reacting to likes
Here there is a check in the handleLayout() function where it checks if there is a new like - Facebook calls them 'reactions'. It takes the first one and simply checks the type and sends the correct emotion to the robot.

```
if(self.reactToLikes() && data.reactions != null && data.reactions.data.length != self.likes()){
  var index = 0;
  switch (data.reactions.data[0]['type']) {
    case 'HAHA':
      index = 2;
      break;
    case 'LOVE':
      index = 1;
      break;
    case 'LIKE':
      index = 10;
      break;
    case 'WOW':
      index = 3;
      break;
    case 'SAD':
      index = 7;
      break;
    case 'ANGRY':
      index = 5;
      break;
  }
  robotSendEmotionRPhi(1.0, emotions_data[index].poly * 18, -1);
}
```
These are all the currently (June 2017) available types of reactions you can chose from Facebook.

## Facebook errors

On the login function it just checks if it has no error or there was no valid response from Facebook. It displays a clear message for the user and logs the full response in the console
```
FB.login(function(response) {
  if (response.status === 'connected') {
    self.setData(response);
  }
  if(response.status == "error"){
    showMainError("Failed to login, please try again");
    console.log(response);
  }
  if(response.status == "unknown" && response.authResponse == null){
    showMainError('Failed to login, please try again');
    console.log(response);
  } else {
    console.log(response)
}
},{scope: 'user_videos, user_photos'});
```

On the fb.get request we found an error code 100 useful to use. The code means it probably is a wrong id, or no public page. We let the user know the id was not valid so he can try again.
```
if(response.error.code){
  if(response.error.code == 100){
    showMainError('We could not find anything with this id, please enter a valid one')
  }
  var str = 'Error code: ' + response.error.code + ', ' + response.error.message;
  console.log(str);
}
```
