# twitter.py
this class holds the code that needs to be executed in the blockly module.
in order for this to work you need to edit scripthost.py in the folder lua_scripting
the main class ```_twitter``` holds all the code needed for authorizing requests. It also holds a second class for the streamreader
```
from opsoro.twitter import Twitter
```
and declare it in the function setup_runtime like this:
```
g["Twitter"] = Twitter
```
# Code
there are a few global variables
```
loop_T = None #loop for Stoppable Thread
autoRead = True #bool that sets if the tweet needs to be readed automaticly
hasRecievedTweet = False #bool that keeps track if the streamreader has recieved a tweet, used to exit the stoppableThread
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
def start_streamreader(self, twitterwords):
    global hasRecievedTweet
    global myStream
    myStream.filter(track=twitterwords, async=True);
    hasRecievedTweet = True #if adding ui elements to blockly this can be used to get out of a loop
    print_info(twitterwords)
```
A StoppableThread is used for checking if the listener has recieved a tweet or not
```
def wait_for_tweet(self):
    time.sleep(1) #the delay
    global loop_T
    while not loop_T.stopped():
        global hasRecievedTweet #if true stops the loop and streamreader
        if hasRecievedTweet == True:
            global myStream
            myStream.disconnect()
            loop_T.stop()
            pass
```
```stop_streamreader()``` is used to stop the streamreader.

```
def stop_streamreader(self):
    global myStream
    myStream.disconnect()
```
# Todo list:
- [x] start streamListener
- [x] stop streamListener
- [x] filter the tweet
- [x] robot read tweet in language
- [x] play emoticons
- [x] create seperate blocks for start stream and stop stream
- [x][ ] make some presets that can be loaded into blockly
- [x] play multiple tweets

# commented code *
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
# testing
 - when pressing stop script sound will continue to play it's current sentence.
  Possible solution: bind stop script to a Sound.stop_sound
als het in een cyrilisch alfabet staat wordt de tekst niet afgespeeld
