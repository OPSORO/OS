# twitter Blockly integration
this class holds the code that needs to be executed in the blockly module.
# setup
### twitter.py
the main class ```_twitter``` holds all the code needed for authorizing requests. It also holds a second class for the streamreader

at the bottom of the code declare ```Twitter = _twitter()``` so that this class can be accessed by apps and scripts

### scripthost.py
in order to add a module in blockly that is in an app folder ie. ```sociono/blockly``` to work correctly you need to make a few changes in ```scripthost.py``` located in the folder lua_scripting.
```
from opsoro.twitter import Twitter #import the class

```
in the function ```setup_runtime``` add the line ```g["Twitter"] = Twitter```
# Code
there are a few global variables
```
loop_T = None #loop for Stoppable Thread
autoRead = True #bool that sets if the tweet needs to be readed automaticly
hasRecievedTweet = False #bool that keeps track if the streamreader has recieved a tweet, used to exit the stoppableThread
loop_TC = None # loop var for tweets by amount

Emoticons = []
hasRecievedTweet = False
TweetCount = 0 # tweets recieved by stream.
TweetMax = 0 # maximum allowed tweets
### get a single tweet based on a hashtag
```
the function ```get_tweet(self, hashtag)``` recieves the hashtag needed to listen in on and initializes a stoppableThread
```
def get_tweet(self, hashtag):
    global loop_T
    self.start_streamreader(hashtag)
    loop_T = StoppableThread(target=self.wait_for_tweet)
```
in ```start_streamreader(self, twitterwords)``` a stream is started that listens for new tweets ```twitterwords``` is the hashtag that is being listened on.
```
def start_streamreader(self, hashtag):
    global hasRecievedTweet
    global myStream
    social_id = []
    social_id.append(hashtag) #if you input the hashtag in the filter without doing this, then there is a chance that it will split up the word in letters and filter by those letters
    hasRecievedTweet = False #if adding ui elements to blockly this can be used to get out of a loop
    myStream.filter(track=social_id, async=True);
```
A StoppableThread is used for checking if the listener has recieved a tweet or not. if ```hasRecievedTweet``` is set to true then the StoppableThread will be stopped.
```
def wait_for_tweet(self):
    time.sleep(1)
    global loop_T
    while not loop_T.stopped():
        global hasRecievedTweet
        if hasRecievedTweet == True:
            global myStream
            myStream.disconnect()
            print_info("stop twitter stream")
            loop_T.stop()
            pass
```
```stop_streamreader()``` is used to stop the streamreader. In this function we will also stop the sound from playing

```
def stop_streamreader(self):
    global myStream
    global hasRecievedTweet
    myStream.disconnect()
    hasRecievedTweet = True
    Sound.stop_sound()
    print_info("stop twitter")
```
### return a set amount of tweets based on a hashtag
```
start the stream and set the amout of tweets that it needs to show
def start_streamreader_amount(self, hashtag, times):
    global myStream
    global loop_TC
    global TweetCount
    global TweetMax
    TweetCount = 0
    TweetMax = times
    social_id = []
    social_id.append(hashtag)
    myStream.filter(track=social_id, async=True);
    loop_TC = StoppableThread(target=self.count_tweets)
```
the StoppableThread is used the check if the amounts of recieved tweets is equal the the maximum of allowed tweets. If this is true the loop will stop and the stream will be stopped.
```
def count_tweets(self):
    time.sleep(1)  # delay
    global TweetMax
    global loop_TC
    while not loop_TC.stopped():
        global TweetCount
        if TweetCount == TweetMax:
            global myStream
            myStream.disconnect()
            print_info("stop twitter stream")
            loop_TC.stop()
            pass

```
# deleted code *
these codes need to be uncommented. If this is done the program will wait untill it's finished before playing a new tweet
```
loop_S = None # loop var for wait_for_sound
SoundPosition = 0 #global var for the sound position
Tweets = [] # this array keeps track of all incoming tweets
```
in stop_streamreader. this checks if the array with tweets is not empty. In this case it will play the sound
```
if Tweets:
    self.playSound()
```
in wait_for_tweet before loop_T.stop():
```
self.playSound()
```
in processJson
```
global Tweets
Tweets.insert(len(Tweets),data) #inserts a tweet at the last position
```
if the array has 1 item it will play the sound and emotion once. else it will use a stoppable thread to play all the tweets.
```
def playSound(self):
   global loop_S
   if len(Tweets) == 1:
       self.playTweetInLanguage(Tweets[0])
       self.playEmotion(Tweets[0])
   elif len(Tweets) > 1:
       loop_S = StoppableThread(target=self.wait_for_sound)
```
plays the sound of the arrays current position
```
def playMultipleTweets(self, position):
   self.playTweetInLanguage(Tweets[position])
```
The StoppableThread iterates through the array and increases by 1 after the sound has played. If the position is equal to the lenght of the array it will stop.
```
def wait_for_sound(self):
   time.sleep(0.05)

   global loop_S
   global SoundPosition
   while not loop_S.stopped():
       Sound.wait_for_sound()
       global autoRead
       if autoRead == 1:
           self.playMultipleTweets(SoundPosition)
           SoundPosition = SoundPosition + 1
       if SoundPosition == len(Tweets):
           loop_S.stop()
           pass
```
function to stop the streamreader without giving the order to play a sound.
```
 def stop_streamreader_on_exit(self):
     global myStream
     global hasRecievedTweet
     myStream.disconnect()
     hasRecievedTweet = False
```
comment these 3 lines in the streamlistener
```
if autoRead == True:
      Twitter.playEmotion(dataToSend)
      Twitter.playTweetInLanguage(dataToSend)
```
