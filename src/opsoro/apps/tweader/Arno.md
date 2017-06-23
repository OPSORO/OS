# Arno Documentation

## getting twitter key

1. go to https://apps.twitter.com
2. create your app
3. go to "keys and tokens"
4. create an access tokens
5. now you have an consumer key, consumer secret, access token and a access token secret

## using tweepy

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

  don't forget to stop your stream to save server load
  ```
  global myStream
  myStream.disconnect()
  ```

## sending profile picture and url
 to make the frontend more attractive we decided to show te profile picture of the tweet and make it clickable.
 To do so we send some extra content from the json we get to our javascript: ["user"]["screen_name"] and ["user"]["profile_image_url_https"]

  The profile picture is just a simple img object with the src you get from twitter.

  Around the img we made an a object and the href = www.twitter.com/ {username}



## Multi language
  Because a tweet can be in every language the speaking must be in the correct language. From the tweet json we got a parameter "lang".

  We made a function playTweetInLanguage(text, language). this function creates a file with eSpeak and reads it out loud.

## auto reader
  The autoreader is a checkbox that is binded with an javascript variable. when we start the stream we send a post to the server and send the autoread boolean with it.
  then wen it's enabled the server will read out every new tweet he gets. When he is not done reading a tweet and there is a new one. The reading will stop and he will begin reading the latest tweet.
