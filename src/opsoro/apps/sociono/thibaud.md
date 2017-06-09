# Thibauds's Documentation

# init.py

The server side code for an app goes inside __init__.py

# removing data from text
make sure to import re (regular expressions) since we are using this for removing the link

1. strTweet.replace("RT","Re Tweet", 1) to replace rt by re tweet so the robot lets the audience know it's a retweet. the 1 stands for the amount of times we will replace this
2. we convert the string to a ascii format to git rid of possible artefact
3. a regular expression is used to remove the link in the tweet

#Blockly

in the folder of the app sociono there is a subfolder called blockly, this is used to declare new blocks to integrate with the blockly app
1. in sociono.xml new blocks are declared ie. <block type="type_name"></block>
2. in sociono.js the blocks are initialized and gets code binded to it.
2.1. Blockly.Blocks['type_name'] = {} is where the layout is declared
2.2. Blockly.Lua['type_name'] = function(block) {} is where we will put the code that is to be generated in

#unicode
unicode is a way to encode signs as a stream of bytes
#```
strTweet = strTweet.decode('unicode_escape').encode('ascii','ignore')
```
" unicode escape
    Produce[s] a string that is suitable as Unicode literal in Python source code
"

#filtering emoticons
#stappen
    #haal string binnen
    #overkijk ofdat er overeenkomsten zijn met 1ste kolom bovenstaande lijst
    #tekst halen uit 2de kolom
    #kijken ofdat er een bepaalde keywoorden in de text zitten
    #geen keywords => neutraal gezicht/ wel gezicht tonen met passende emotie

link used as reference: ftp://ftp.unicode.org/Public/UNIDATA/UnicodeData.txt
1F620 : angry face
1F628: fearful face
1F602: laughing with tears
1F603: laughing with open mouth
1F62A: sleepy face
1F62B:  tired face
1F629: weary face
2639: frowning face
263A: smiling face (white)
263b: smiling face (black)
1F609: winking face
1F914: thinking face
1F922: nauseated face
1F632: astonished face
1F610: neutral face
# Issues
