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
