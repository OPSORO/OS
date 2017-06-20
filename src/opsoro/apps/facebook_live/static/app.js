$(document).ready(function() {

  /* Facebook SDK Init */


  window.fbAsyncInit = function() {
    FB.init({
      appId            : '1710409469251997',
      autoLogAppEvents : true,
      xfbml            : true,
      version          : 'v2.9'
    });
    FB.AppEvents.logPageView();
    // Start using the FB SDK
    model.fbInitialized(true);
    model.checkFBLogin();
  }

  $(function(d, s, id){
     var js, fjs = d.getElementsByTagName(s)[0];
     if (d.getElementById(id)) {return;}
     js = d.createElement(s); js.id = id;
     js.src = "//connect.facebook.net/en_US/sdk.js";
     fjs.parentNode.insertBefore(js, fjs);
   }(document, 'script', 'facebook-jssdk'));

  /* Models */

  var EmotionModel = function(name, index){
    var self = this;
    self.name = name;
    self.index = index;
  }

  var TypesModel = function(text, index) {
    var self = this;
    self.text = text;
    self.index = index;
  }

  /* Facebook Login */

  var FacebookLiveModel = function() {
      var self = this;

      /* Observables for facebook init */
      self.fbInitialized = ko.observable(false);

      /* Observables for facebook Auth */
      self.loggedIn = ko.observable(false);
      self.accessToken = ko.observable(""); // retrieved from log in, needed for every Facebook call
      self.userID = ko.observable(""); // when logged into facebook, could be used if you'd like to get your own wall posts ect.
      
      /* Observables for handling the new live video stream */
      self.newLiveVideoData = ko.observable(""); // holds the new live video's data
      self.isNewVideo = ko.observable(); // check for starting a new live video -> toggle lay-out & functionality
      self.fbDataResponse = ko.observable(); // catches the facebook response every interval ... needed to set embed_html once
      self.embedIframe = ko.observable("");
      self.views = ko.observable(0)
      self.comments = ko.observableArray();

      /* Observables for handling the custom facebook requests */
      self.customRequest = ko.observable(false); // for an extra request to get the custom id's info (type, ...)
      self.isStreaming = ko.observable(false);
      self.facebookID = ko.observable(""); // when user enters his own input id
      self.ofTypes = ko.observableArray([new TypesModel('Page', 0), new TypesModel('Post', 1), new TypesModel('Live Video', 2)]);
      self.selectedType = ko.observable(); // catch the selected type for the given facebook ID
      self.isPage = ko.observable(false);
      self.pagePosts = ko.observableArray();
      self.isPost = ko.observable(false);
      self.isLiveVideo = ko.observable(false);

      /* General observables */
      self.autoRead = ko.observable(false);
      self.reactToLikes = ko.observable(false);
      self.likes = ko.observable(0);
      self.availableEmotions = ko.observableArray([new EmotionModel('None', 0)]);
      self.selectedEmotion = ko.observable();
      for (var i = 0; i < emotions_data.length; i++) {
        self.availableEmotions.push(new EmotionModel(emotions_data[i]['name'], i+1));
      }

      self.checkFBLogin = function(){
        if(self.getLoginStatus()){
          self.loggedIn(true);
        }
        else{
          self.fbLogin();
          if(self.getLoginStatus()){
            //self.loggedIn(true);
          }
        }
      }

      self.getLoginStatus = function() {
        FB.getLoginStatus(function(response){
          if (response.status === 'connected') {
            return true;
          } else {
            // self.fbLogin()
            return false;
          }
        });
      }

      self.fbLogin = function() {
        FB.login(function(response) {
          console.log(response)
          if (response.status === 'connected') {
            console.log(response)
            self.setData(response);
          } else {
            // error ?
            console.log(response)
          }
        },{scope: 'user_videos, user_posts, user_photos, user_actions.video'});
      }

      self.fbLogout = function() {
        FB.logout(function(response) {
          console.log(response);
          self.unsetData();
        });
      }

      self.setData = function(response) {
        self.loggedIn(true);
        self.accessToken(response.authResponse.accessToken);
        self.userID(response.authResponse.userID);
      }

      self.unsetData = function() {
        self.loggedIn(false);
        self.accessToken("");
        self.userID("");

        // Stop stream & reset layout !!
        self.stopStream();
      }

      self.fbGET = function(obj) {
        FB.api('/' + obj.fb_id + '?fields=' + obj.fields + '&access_token=' + self.accessToken(), function(response) {
          if(response && !response.error){
            //console.log(response);
            self.fbDataResponse(response) // could use this instead of passing through params

            if (self.isNewVideo()) {

              self.setIFrame(); // should only happen once, does it ?
              self.handleLayout(response)

            } else if(self.isPage()) {
              // get feed posts?
              self.handleLayout(response.feed); // contains data & paging object
              
            } else if(self.isPost()) {
              // get post's comments ect ... ?
              self.handleLayout(response);
            } else if(self.isLiveVideo()) {

              self.setIFrame();
              self.handleLayout(response);

            }
          } else {
            // error, check if key expired -> re-login ?
            console.log(response)
          }
        })
      }

      /* Videos */

      self.startNewLiveStream = function() {
        FB.ui({
            display: 'popup',
            method: 'live_broadcast',
            phase: 'create'
        }, function(response) {
            if (!response.id) {
              alert('dialog canceled');
              return;
            }
            self.newLiveVideoData(response);
            self.facebookID(response.id);
            self.isNewVideo(true);
            self.selectedType(self.ofTypes()[2]); // setting the selected option to "Live Video"
          }
        );
      }

      self.newVideoRequest = function(obj) {
        FB.ui({
          display: 'popup',
          method: 'live_broadcast',
          phase: 'publish',
          broadcast_data: obj,
        }, function(response) {
          //console.log(response)
          //  alert("video status: \n" + response.status);

          if (response && response.status === "live") {
            self.isNewVideo(false); // the video has already streamed so it's not new anymore ...
            self.postToThread(obj);
          } else {
            // error dialog is canceld before video went on air !!!
          }
        });
      }

      /* Custom page input */

      self.toggleStreaming = function(){
        if(self.isStreaming()){
          self.stopStream();
        } else {

          var obj;

          if (self.newLiveVideoData() != "") {
            obj = self.newLiveVideoData();
            obj.fb_id = self.facebookID();
            obj.fields = "";
          } else {
            self.isNewVideo(false); // firing custom request so disable the ability to start a new live video
            obj = { fb_id: self.facebookID() } // sending the id in an object because handleData expects an object
            console.log(self.facebookID()); // make sure facebookID is bound to HTML without () for two-way binding
          }

          self.handleData(obj);
        }

        self.isStreaming(!self.isStreaming()); // will this be instantly executed or only after the functions above ??
      }

      self.requestByCustomID = function(obj) {

        // Let's get the type of the requested info first ...
        // is page, is post, is video?

        switch(self.selectedType().index) {
          case 0: // Page
            self.isLiveVideo(false);
            self.isPage(true);
            obj.fields = "feed{id,message,reactions{ame,link,type},story,likes{name}}";
            self.postToThread(obj);
            break;
          case 1: // Post
            self.isLiveVideo(false);
            self.isPost(true);
            obj.fields = "comments{from,message,permalink_url},reactions{name,link,type},likes{name}";
            self.postToThread(obj);
            break;
          case 2: // Video
            self.isLiveVideo(true); // should be just isVideo ...
            obj.fields = "status,live_views,comments{from,message,permalink_url},embed_html,title,reactions{name,link,type},likes{name}";
            self.postToThread(obj);
            break;
        }

      }

      /* General */

      self.stopStream = function(){

        self.sendPost('stopThread', {});

        // reset lay-out
        self.resetLayout();
      }

      self.resetLayout = function() {
        self.isNewVideo(false);
        self.newLiveVideoData("");
        self.embedIframe("");
        self.fbDataResponse("");
        self.comments.removeAll();
        self.pagePosts.removeAll();
        self.isNewVideo(false);
        self.isLiveVideo(false);
        self.views(0);
      }

      self.hardResetLayout = function() { // reset everything on log out or something, not used anywhere atm!
        self.facebookID("");
        self.selectedType(self.ofTypes()[0]); // reset to element 0
        self.autoRead(false);
        self.reactToLikes(false);
        self.selectedEmotion(self.availableEmotions()[0]);
      }


      self.handleData = function(obj) { // function will be used for a new live video but also for custom id input so don't set isNewVideo(true) likewise in here
        self.facebookID(obj.fb_id);

        if(self.isNewVideo()) {
          obj.fields = "status,live_views,comments{from,message,permalink_url},embed_html,title,reactions{name,link,type},likes{name}";
          self.newVideoRequest(obj);
        } else {
          self.requestByCustomID(obj);
        }
      }

      self.postToThread = function(obj) {
        $.post('/apps/facebook_live/', { action: 'postToThread', data: JSON.stringify(obj) }, function() {
          console.log("Posted to thread to wait few seconds")
        });
      }


      self.setIFrame = function() {
        if ((self.isNewVideo() || self.isLiveVideo()) && self.fbDataResponse().embed_html) {
          self.embedIframe(self.fbDataResponse().embed_html);
        }
      }

      self.handleLayout = function(data) { // the stuff that changes every 5 seconds

        if (self.isPage()) { // handle data differently if page
          var paging = data.paging;

          if (data.data && data.data.length > 0) {

            // to avoid errors of undefined objects while binding
            var arr = [];
            $.each(data.data, function(key, val) {
              if (!val.story) {
                val.story = "";
              }
              if (!val.message) {
                val.message = "";
              }
              arr.push(val);
            });

            // can't check the count diffrence because it's limit is 25 so it will always be 25
            if(self.pagePosts().length > 0 && self.pagePosts()[0]['id'] != arr[0]['id']) { // 0 instead of last because order is diffrent (newest first)
              if(self.autoRead()){
                //send last comment to read out loud
                var textToRead;
                if (arr[0]["message"]) {
                  textToRead = arr[0]["message"];
                }
                if (arr[0]["story"]) {
                  textToRead = arr[0]["story"];
                }
                console.log(textToRead);
                robotSendTTS(textToRead);
              }

              var emotion = self.selectedEmotion();
              if(! emotion['index'] == 0){
                robotSendEmotionRPhi(1.0, emotions_data[emotion['index'] -1].poly * 18, -1);
              }
            }
            self.pagePosts(arr);
          }
        } else { // is Post or Video

          if (self.isNewVideo() || self.isLiveVideo()) {
            self.views(data.live_views);
          }

          if(data.comments && data.comments.data.length > 0) {
            var arr_comments = data.comments.data;

            if(self.comments().length != arr_comments.length){
              if(self.comments().length < arr_comments.length && self.comments().length != 0){
                if(self.autoRead()){
                  //send last comment to read out loud
                  robotSendTTS(arr_comments[arr_comments.length -1]["message"]);
                }

                var emotion = self.selectedEmotion();
                if(! emotion['index'] == 0){
                  robotSendEmotionRPhi(1.0, emotions_data[emotion['index'] -1].poly * 18, -1);
                }
              }
            }
            // refill list to get last comments
            self.comments(arr_comments.reverse());
          }

          if(data.reactions && data.reactions.data.length != 0) {
            self.likes(data.reactions.data.length);
          }
          
          if(self.reactToLikes() && data.reactions != null && data.reactions.data.length != self.likes()){

            //nieuwe reactie
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
        }
      }


      self.sendPost = function(action, data){
        console.log("Posted to stop stream! Please stahp!");
        $.ajax({
          dataType: 'json',
          type: 'POST',
          url: '/apps/facebook_live/',
          data: {action: action, data: data },
          success: function(data){
            if (!data.success) {
              showMainError(data.message);
            } else {
              console.log("Stream stopped?");
              return data.config;
            }
          }
        });
      }
  };

  // This makes Knockout get to work
  var model = new FacebookLiveModel();
  ko.applyBindings(model);

  // receiving data from python
  app_socket_handler = function(data) {
    switch (data.action) {
      case "threadRunning":
        if(data.fb_id && data.fields) {
          model.fbGET(data);
        }
        break;
    }
  };

  // listener for when input is changed / facebookID, change the selectbox accordingly
  model.facebookID.subscribe(function() {
    if (model.facebookID().indexOf("_") > 0) { // post ids have an underscore in them
      model.selectedType(model.ofTypes()[1]); // change the selectbox accordingly
    }
  })

});


// avoiding keyboard interrupts
$( window ).unload(function() {
  $.ajax({
    dataType: 'json',
    type: 'POST',
    url: '/apps/facebook_live/',
    data: {action: 'stopThread', data: {} },
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
