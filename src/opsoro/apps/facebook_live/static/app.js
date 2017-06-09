$(document).ready(function() {
    var FacebookLiveModel = function() {
        var self = this;
        this.startFacebookLiveDialog = ko.observable(function(){
          FB.ui({
            display: 'popup',
            method: 'live_broadcast',
            phase: 'create',
          }, function(response) {
            if (!response.id) {
              alert('dialog canceled');
              return;
            }
            alert('stream url:' + response.secure_stream_url);
            FB.ui({
              display: 'popup',

              method: 'live_broadcast',
              phase: 'publish',
              broadcast_data: response,
            }, function(response) {
              alert("video status: \n" + response.status);
            });
          });
        });

        this.streamKey= ko.observable("");

        this.startFunction = ko.observable(function(){
          console.log(this.streamKey());
        });
  };
    // This makes Knockout get to work
    var model = new FacebookLiveModel();
    ko.applyBindings(model);


    //START facebook api content
    window.fbAsyncInit = function() {
    FB.init({
      appId            : '1710409469251997',
      autoLogAppEvents : true,
      xfbml            : true,
      version          : 'v2.9'
    });
    FB.AppEvents.logPageView();
    };

    (function(d, s, id){
     var js, fjs = d.getElementsByTagName(s)[0];
     if (d.getElementById(id)) {return;}
     js = d.createElement(s); js.id = id;
     js.src = "//connect.facebook.net/en_US/sdk.js";
     fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));

    //STOP facebook api content
});
