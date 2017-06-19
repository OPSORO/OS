# -*- coding: utf-8 -*-
from __future__ import with_statement

import glob
import math
import os
import shutil
import time
from exceptions import RuntimeError
from functools import partial

from werkzeug import secure_filename

import cmath
from opsoro.console_msg import *
from opsoro.expression import Expression
from opsoro.hardware import Hardware
from opsoro.robot import Robot
from opsoro.sound import Sound
from opsoro.sound.tts import TTS

from opsoro.stoppable_thread import StoppableThread

from opsoro.users import Users

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

import tweepy
import re
import json
import time

def constrain(n, minn, maxn): return max(min(maxn, n), minn)

Emoticons = []
loop_T = None # loop var for Stoppable Thread
#     if winking > 0:
#         emotions.append("tong")
#     if angry > 0:
#         emotions.append("angry")
#     if happy_a > 0 or happy_b > 0 or happy_c > 0:
#         emotions.append("happy")
#     if frowning > 0:
#         emotions.append("tired")
#     if nauseated > 0:
#         emotions.append("disgusted")
#     if astonished > 0:
#         emotions.append("surprised")
#     if neutral > 0:
#         emotions.append("neutral")
#     if fearful > 0:
#         emotions.append("afraid")
#     if laughing > 0:
#         emotions.append("laughing")
#     if tired > 0:
#         emotions.append("sleep")
#     if sad > 0:
#         emotions.append("sad")
#     #if no emotions are selected returns none
#     if not emotions:
#         emotions.append("none")
#     return emotions
# def wait_for_sound():
    # time.sleep(0.05)  # delay
    #
    # global loop_T
    # while not loop_T.stopped():
    #     Sound.wait_for_sound()
    #     global autolooping
    #     if autolooping == 1:
    #         send_action("autoLoopTweepyNext")
    #     loop_T.stop()
    # pass
#the idea: recieve a tweet where all that has been filtred and processed for all but the text and emoticons.
#divide the text into segments
# vb array
# textemojiarray.append[texttospeak]
# textemojiarray.append[emoji]
#
# for value in textemojiarray:
#     if isemijo == true:
#         convertEmoji(emojiVal)
#     else:
#         playTextInLanguage(text)
#         #wait_for_sound
#     pass
class _textSplitter(object):
    """docstring for textSplitter."""
    def __init__(self):
        super(_textSplitter, self).__init__()
    def split(self,text, emoji):
        re.split(emoji, text)

    def convertEmoji(self):
        emotions = []
        # emoticonStr = status.text
        # print_info(strTweet)
        delimiters = {"\U0001F609","\U0001F620","\U0000263A", "\U0000263b","\U0001f642", "\U0001F914", "\U00002639", "\U0001F922","\U0001F632","\U0001F610","\U0001F628","\U0001F603","\U0001F62B","\U0001f641" }
        #regexPattern = '|'.join(map(re.escape, delimiters))

        text = 'thvander U0001f642, test U0001F609 emoji U0001F609 U0001f642 2'
        split = text.split(delimiters)
        print_info(split)
        for splitpart in split:
            print_info(splitpart)
        # splittedText = []
        # for delimiter in delimiters:
        #     print_info(delimiter)
        #     if re.search(delimiter, text):
        #         splittedText = re.split("("+delimiter+")", text)
        #
        # splittedTextcopy = splittedText
        # print_info(splittedTextcopy)
        # for text in splittedTextcopy:
        #     delimiters.pop()
        #     subtext = re.split("("+delimiter+")", text)
        #     print_info(subtext)
        #
        # delimiters.pop()
        # print_info(delimiters)
        # for delimiter in delimiters:
        #     for text in splittedText:
        #         print_info(text)
        #         pass
# if re.search(delimiter, text):
#      print_info("emoji found" + text)

# for text in splittedText:
#     print_info(text)
#     subsplit = re.split("("+delimiter+")", text)
#     print_info(subsplit)

        # winking = len(re.findall(u"[\U0001F609]", emoticonStr))
        # angry = len(re.findall(u"[\U0001F620]", emoticonStr))
        # happy_a = len(re.findall(u"[\U0000263A]", emoticonStr))
        # happy_b = len(re.findall(u"[\U0000263b]", emoticonStr))
        # happy_c = len(re.findall(u"[\U0001f642]", emoticonStr))
        # thinking = len(re.findall(u"[\U0001F914]", emoticonStr))
        # frowning = len(re.findall(u"[\U00002639]", emoticonStr))
        # nauseated = len(re.findall(u"[\U0001F922]", emoticonStr))
        # astonished = len(re.findall(u"[\U0001F632]", emoticonStr))
        # neutral = len(re.findall(u"[\U0001F610]", emoticonStr))
        # fearful = len(re.findall(u"[\U0001F628]", emoticonStr))
        # laughing = len(re.findall(u"[\U0001F603]", emoticonStr))
        # tired = len(re.findall(u"[\U0001F62B]", emoticonStr))
        # sad = len(re.findall(u"[\U0001f641]", emoticonStr))

        # if winking > 0:
            # winking
        # if angry > 0:
            # angry
        # if happy_a > 0 or happy_b > 0 or happy_c > 0:
            # happy
        # if frowning > 0:
            # frowning
        # if nauseated > 0:
            # nauseated
        # if astonished > 0:
            # astonished
        # if neutral > 0:
            # neutral
        # if fearful > 0:
            # fear
        # if laughing > 0:
            # laughing
        # if tired > 0:
            # tired
        # if sad > 0:
            # sad

textSplitter = _textSplitter()
