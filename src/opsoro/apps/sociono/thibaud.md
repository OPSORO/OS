# Thibauds's Documentation

# init.py
The server side code for an app goes inside `__init__.py`
# removing data from text
make sure to import re (regular expressions) since we are using this for removing the link

1. `strTweet.replace("RT","Re Tweet", 1)` to replace rt by re tweet so the robot lets the audience know it's a retweet. the 1 stands for the amount of times we will replace this
2. we convert the string to a ascii format to git rid of possible artefact
3. a regular expression is used to remove the link in the tweet

# Blockly

in the folder of the app sociono there is a subfolder called blockly, this is used to declare new blocks to integrate with the blockly app
1. in sociono.xml new blocks are declared ie. `<block type="type_name"></block>`
2. in sociono.js the blocks are initialized and gets code binded to it.
  2.1`Blockly.Blocks['type_name'] = {}` is where the layout is declared
  2.2.`Blockly.Lua['type_name'] = function(block) {}` is where we will put the code that is to be generated in
for this project we have made a custom class twitter.py that holds the code used for the blockly module

# unicode
unicode is a way to encode signs as a stream of bytes.
```
strTweet = strTweet.decode('unicode_escape').encode('ascii','ignore')
```
unicode escape Produce[s] a string that is suitable as Unicode literal in Python source code
decode makes emoji from code while encode makes code from emoji

# filtering emoticons
We wil use regular expressions to check if a post has an emoticon and we wil keep count of the amount of times given emoticon is present.
```winking = len(re.findall(u"[\U0001F609]", emoticonStr))``` example of the code used to check if an emoticon is present or not. If no emoticons are present a simple none is returned

After this is done we check if the amount of ie. ```winking``` is higher then 0. If this is true we add it to the array
```
if winking > 0:
    emotions.append("tong")
if angry > 0:
    emotions.append("angry")
```

# Playing emoticons
By using the stoppableThread we execute a loop where we will iterate through an array with the emoticons that shall be played.
```
if request.form['action'] == 'playTweet':
        if request.form['data']:
            tweepyObj = json.loads(request.form['data'])

            global loop_T
            global Emoticons
            post_emoticons = json.loads(request.form['data'])
            Emoticons = post_emoticons['text']['emoticon']
            loop_T = StoppableThread(target=asyncEmotion)

            playTweetInLanguage(tweepyObj)
```

asyncEmotion iterates all items in the array and plays it. we use ```time.sleep()``` to halt the program for a few second so the animation can complete without getting interrupted by the next one. This is done on a different thread since ```time.sleep()``` halts all code from being executed for a set duration. without this call the animations will play but they will be unnoticed. They will start playing directly when the call is made causing the previous animation unable to finish because a new one should directly be executed.
```
def asyncEmotion():
    time.sleep(0.05)

    global loop_T
    global Emoticons
    currentAnimationArrayLength = len(Emoticons)
    playedAnimations = 0
    while not loop_T.stopped():
        # if running:
        print_info(Emoticons)
        if currentAnimationArrayLength > playedAnimations:
            Expression.set_emotion_name(Emoticons[playedAnimations], -1)
            playedAnimations = playedAnimations+1
            time.sleep(2)
        if currentAnimationArrayLength == playedAnimations:
            loop_T.stop()
            pass
```
the stoppable_thread function shown above.

  - ```playedAnimations``` are the animations that have been played. if this is equal to the length of emoticons the loop will stop itself
  - we increase the amount of played animations by 1 after we have played an emotion.
  - ```time.sleep(2) ``` halts the code for 2 seconds so that the animation can complete

# Issues
Emoticons
  for some reason when you play an emoticon robot will be unable to exit. and the user will see a keyboard interupt but will be unable to shutdown the robot
  
# references
link used as reference: ftp://ftp.unicode.org/Public/UNIDATA/UnicodeData.txt
```
1F620: angry face
1F628: fearful face
1F602: laughing with tears
1F603: laughing with open mouth
1F62A: sleepy face
1F62B: tired face
1F629: weary face
2639: frowning face
263A: smiling face (white)
263b: smiling face (black)
1F609: winking face
1F914: thinking face
1F922: nauseated face
1F632: astonished face
1F610: neutral face'
```
