# Blockly

The subfolder blockly in tweader is used to declare new blocks for the blockly app.
This folder contains two files and bears the same name as the app:
1. tweader.xml: Here we declare new blocks ie. `<block type="type_name"></block>`
2. tweader.js: We initialize the blocks and assign the code that needs to be executed.
  2.1`Blockly.Blocks['type_name'] = {}` is where the code for the layout is put.
  2.2.`Blockly.Lua['type_name'] = function(block) {}` is where we will put the code that is to be generated in.

For this project we have made a custom class twitter.py that holds the code used for the blockly module.

### scripthost.py
In order to add a module in blockly that is in an app folder ie. ```tweader/blockly``` to work correctly you need to make a few changes in ```scripthost.py``` located in the folder lua_scripting.
```
from opsoro.twitter import Twitter #import the class

```
In the function ```setup_runtime``` add the line ```g["Twitter"] = Twitter```

## using blockly
You can easily create new blocks for blockly by using the site: https://blockly-demo.appspot.com/static/demos/blockfactory/index.html

This site implements a visual way where the user can create blocks by dragging simple blocks and connecting them to create more advanced blocks in the left view. On the right view the user can see the preview of the block and the code needed to implement the block ie.
1. Definitions for json or js which describe the layout of the block
2. The generator stubs: the code that will be executed. this can be: JavaScript, Python, Lua, PHP or Dart.

### block definitions
The block definition describes the layout of the block.
```
Blockly.Blocks['sociono_get_tweet'] = {
  init: function() {
    this.appendValueInput("value") #this is a value input
        .setCheck(null)
        .appendField("get a single tweet based on hashtag "); #a sipmle text that the user will see
    this.setInputsInline(true); # if set to true the input will be in the block itself instead of a puzzelslot at the end of the block
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230); # colour of the block
    this.setTooltip('connect your variable to this block to filter by'); # tooltip for the user.
    this.setHelpUrl('');
  }
};
```

### generator stubs
The preview for the generated code will give this:
```
Blockly.Lua['sociono_get_tweet'] = function(block) {
    var value_value = Blockly.Lua.valueToCode(block, 'value', Blockly.Lua.ORDER_ATOMIC);
    var code = 'Twitter:get_tweet('+value_value+')\n';
  return code;
};

```
```var value_value = Blockly.Lua.valueToCode(block, 'value', Blockly.Lua.ORDER_ATOMIC);``` Here we take the data from the input field and store it in a variable.

```var code = 'Twitter:get_tweet('+value_value+')\n';``` This is the code that the will be returned to the generator. All code snippets needs to be put between single quotes except the values declared in the program.


```
To change the programming language you can select the language you want it to be. This can also be done manually ie. ```Blockly.Lua['block_type']``` to ```Blockly.Python['block_type']```

# twitter.py
This class holds the code that needs to be executed in the blockly module.

## Code
There are a few global variables
```
access_token = 'token'
access_token_secret = 'token secret'
consumer_key = 'consumer key'
consumer_secret = 'consumer secret'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

loop_T = None # loop var for wait_for_tweet
loop_E = None # loop var for Emoticons
loop_TC = None # loop var for tweets by amount

Emoticons = []
hasRecievedTweet = False #bool that keeps track if the streamreader has recieved a tweet, used to exit the stoppableThread
stopLoop = False # failsafe for a stoppableThread if true will exit the stoppableThread

TweetCount = 0 # tweets recieved by stream.
TweetMax = 0 # maximum allowed tweets

```
### get a single tweet based on a hashtag

The function ```get_tweet(self, hashtag)``` recieves the hashtag needed to listen in on and initializes a stoppableThread. We also check wether the hastag exists so that the code doesn't run without a valid input.
```
def get_tweet(self, hashtag):
      global loop_T
      if not (hashtag is None):
          print_info(hashtag)
          self.start_streamreader(hashtag)
          loop_T = StoppableThread(target=self.wait_for_tweet)
      else:
          print_info("no input given")
```
In ```start_streamreader(self, twitterwords)``` a stream is started that listens for new tweets, ```twitterwords``` is the hashtag that is being listened on.
```
def start_streamreader(self, hashtag):
    global hasRecievedTweet
    global myStream
    social_id = []
    social_id.append(hashtag) #if you input the hashtag in the filter without doing this, then there is a chance that it will split up the word in letters and filter by those letters
    hasRecievedTweet = False #if adding ui elements to blockly this can be used to get out of a loop
    myStream.filter(track=social_id, async=True);
```
A StoppableThread is used for checking if the listener has recieved a tweet or not. If ```hasRecievedTweet``` is set to true then the StoppableThread will be stopped.
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
```stop_streamreader()``` is used to stop the streamreader and stop the sound. The value for stopLoop is set to True. This serves a way for when you want to interrupt the get_tweet_amount manually.

```
def stop_streamreader(self):
    global myStream
    global hasRecievedTweet
    global stopLoop
    stopLoop = True
    myStream.disconnect()
    hasRecievedTweet = True
    Sound.stop_sound()
    print_info("stop twitter")
```
### return a set amount of tweets based on a hashtag
Start the stream and set the amout of tweets that it needs to show. The check for a valid input is also done here.
```
def start_streamreader_amount(self, hashtag, times):
      global myStream
      global loop_TC
      global TweetCount
      global TweetMax
      global stopLoop
      if not (hashtag is None):
          TweetCount = 0
          TweetMax = times
          social_id = []
          social_id.append(hashtag)
          myStream.filter(track=social_id, async=True);
          stopLoop = False
          loop_TC = StoppableThread(target=self.count_tweets)
```
The StoppableThread is used to check if the amounts of recieved tweets is equal the the maximum of allowed tweets or if stopLoop is set to True. In these cases the loop and the stream will be stopped.
```
def count_tweets(self):
      time.sleep(1)  # delay
      global TweetMax
      global loop_TC
      global stopLoop
      while not loop_TC.stopped():
          global TweetCount
          print_info(TweetCount)
          if TweetCount == TweetMax or stopLoop == True:
              global myStream
              myStream.disconnect()
              print_info("stop twitter stream")
              loop_TC.stop()
              pass
```
