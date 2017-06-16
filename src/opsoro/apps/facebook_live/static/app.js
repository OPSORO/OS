$(document).ready(function() {

  /* Facebook SDK Init */


  window.fbAsyncInit = function() {
    FB.init({
      appId            : '288611811599525',
      autoLogAppEvents : true,
      xfbml            : true,
      version          : 'v2.9'
    });
    FB.AppEvents.logPageView();

    // Start using the FB SDK

    model.fbInitialized(true);

    // check if loggedIn ? Not working I think, unless you automatically logout every page refresh?
    model.getLoginStatus();

  }

  $(function(d, s, id){
     var js, fjs = d.getElementsByTagName(s)[0];
     if (d.getElementById(id)) {return;}
     js = d.createElement(s); js.id = id;
     js.src = "//connect.facebook.net/en_US/sdk.js";
     fjs.parentNode.insertBefore(js, fjs);
   }(document, 'script', 'facebook-jssdk'));


  /* Models */

  var CommentModel = function(commentData){
    var self = this;
    self.username = ko.observable(commentData["from"]["name"] || "");
    self.comment = ko.observable(commentData["message"] || "");
  }
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
      self.newLiveVideo = ko.observable(""); // holds the new live video's data
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
      self.isPost = ko.observable(false);
      self.isLiveVideo = ko.observable(false);

      /* General observables */
      self.autoRead = ko.observable(false);
      self.availableEmotions = ko.observableArray([new EmotionModel('None', 0)]);
      self.selectedEmotion = ko.observable();
      for (var i = 0; i < emotions_data.length; i++) {
        self.availableEmotions.push(new EmotionModel(emotions_data[i]['name'], i+1));
      }

      self.getLoginStatus = function() {
        FB.getLoginStatus(function(response){ 
          if (response.status === 'connected') {
            console.log(response)
            self.setData(response);
          } else {
            // self.fbLogin()
            self.unsetData();
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
        });      
      }

      self.fbLogout = function() {
        FB.logout(function(response) {
          console.log(response)
          this.unsetData();
        });
      }

      self.setData = function(response) {
        self.loggedIn(true)
        self.accessToken(response.authResponse.accessToken)
        self.userID(response.authResponse.userID)
      }

      self.unsetData = function() {
        self.loggedIn(false)
        self.accessToken("")
        self.userID("")
      }

      self.fbGET = function(obj) {
        FB.api('/' + obj.fb_id + '?fields=' + obj.fields + '&access_token=' + self.accessToken(), function(response) {
          if(response && !response.error) {

            console.log(response);
            self.fbDataResponse(response) // could use this instead of passing through params

            if (self.isNewVideo()) {

              self.setIFrame(); // should only happen once, does it ?
              self.handleLayout(response)

            } else if(self.isPage()) {
              // get feed posts?
            } else if(self.isPost()) {
              // get post's comments ect ... ?
            } else if(self.isLiveVideo()) {
              
              self.setIFrame();
              self.handleLayout(response);

            }
          } else {
            // error
            console.log(response)
          }
        })
      }

      /* Videos */

      self.startNewLiveStream = function() {
        if(self.isStreaming()){
          self.stopStream();
        }

        FB.ui({
            display: 'popup',
            method: 'live_broadcast',
            phase: 'create',
            fields: 'embed_html'
        }, function(response) {
            if (!response.id) {
              alert('dialog canceled');
              return;
            }
            self.isNewVideo(true);
            self.handleData(response)
          }
        );
      }

      self.newVideoRequest = function(obj) {
        FB.ui({
          display: 'popup',
          method: 'live_broadcast',
          phase: 'publish',
          broadcast_data: response,
        }, function(response) {
          console.log(response)
          //  alert("video status: \n" + response.status);
          if (response.status === "live") {
            self.postToThread(obj)
          }
        });
      }

      /* Custom page input */

      self.toggleStreaming = function(){

        console.log(self.isStreaming());

        if(self.isStreaming()){
          self.stopStream();
        } else {

          self.isNewVideo(false); // firing custom request so disable the ability to start a new live video

          console.log(self.facebookID()); // make sure facebookID is bound to HTML without () for two-way binding

          var data_obj = { id: self.facebookID() } // sending the id in an object because handleData expects an object

          self.handleData(data_obj);
        }

        self.isStreaming(!self.isStreaming()); // will this be instantly executed or only after the functions above ??
      }

      self.requestByCustomID = function(obj) {

        // Let's get the type of the requested info first ...
        // is page, is post, is video?

        // ------------- Hier gebleven ------------------

        console.log(self.selectedType());

        switch(self.selectedType().index) {
          case 0: // Page

            break;
          case 1: // Post

            break;
          case 2: // Video
            self.isLiveVideo(true);
            obj.fields = "status,live_views,comments{from,message,permalink_url},embed_html,title,reactions{name,link,type},likes{name}";
            self.postToThread(obj);
            break;
        }


        // self.postToThread(obj)


      }

      /* General */

      self.stopStream = function(){

        self.sendPost('stopThread', {});

        // reset lay-out
        self.comments.removeAll();
        self.isNewVideo(false);
        self.isLiveVideo(false);
        self.views(0);
      }

      self.handleData = function(data) { // function will be used for a new live video but also for custom id input so don't set isNewVideo(true) likewise in here
        
        self.facebookID(data.id);

        var obj = { fb_id: self.facebookID(), fields: "" }

        if(self.isNewVideo()) {
          self.newLiveVideo(data);
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

        self.views(data.live_views);

        if(data.comments && data.comments.data.length > 0) {
          var arr_comments = data.comments.data;

          if(self.comments().length != arr_comments.length){
            if(self.autoRead() && self.comments().length < arr_comments.length && self.comments().length != 0){
              //send laatste comment om voor te lezen
              robotSendTTS(arr_comments[arr_comments.length -1]["message"]);
            }
            //hervul de lijst om laatste comments te krijgen
            self.comments(arr_comments.reverse())
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

  app_socket_handler = function(data) {
    switch (data.action) {
      case "threadRunning":
        if(data.fb_id && data.fields) {
          model.fbGET(data)
        }
        break;
    }
  };
});
