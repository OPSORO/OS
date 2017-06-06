$(document).ready(function() {
    var Model = function() {
        var self = this;

        // File operations toolbar item
        self.fileIsLocked = ko.observable(false);
        self.fileIsModified = ko.observable(false);
        self.fileName = ko.observable("");
        self.fileStatus = ko.observable("");
        self.fileExtension = ko.observable(".ext");

        // Script operations toolbar item
        self.isRunning = ko.observable(false);
        self.isUI = ko.observable(false);

        // Lock/Unlock toolbar item
        self.toggleLocked = function() {
            if (self.fileIsLocked()) {
                self.unlockFile();
            } else {
                self.lockFile();
            }
        };
        self.lockFile = function() {
            self.fileIsLocked(true);
            self.fileStatus("Locked")
        };
        self.unlockFile = function() {
            self.fileIsLocked(false);
            self.fileStatus("Editing")
        };

        // Popup window
        self.popupTextInput = ko.observable("Hi! This text can be changed. Click on the button to change me!");
        self.showPopup = function() {
          $("#popup_window").foundation('open');

        };
        self.closePopup = function() {
            $("#popup_window").foundation('close');
        };
        self.popupButtonHandler = function() {
            self.closePopup();
        };

        self.init = function() {
            // Clear data, new file, ...
            self.fileName("Untitled");
            self.unlockFile();
            self.fileIsModified(false);
        };

        self.loadFileData = function(data) {
            if (data == undefined) {
                return;
            }

            // Load data, parse if needed
            var dataobj = JSON.parse(data);


            self.fileIsModified(false);
            self.lockFile();
        };

        self.saveFileData = function() {
            // Convert data
            file_data = {};

            var data = ko.toJSON(file_data, null, 2);
            self.fileIsModified(false);
            return data;
        };
    };
    // This makes Knockout get to work
    var model = new Model();
    ko.applyBindings(model);
    model.fileIsModified(false);



  (function(d, s, id){
     var js, fjs = d.getElementsByTagName(s)[0];
     if (d.getElementById(id)) {return;}
     js = d.createElement(s); js.id = id;
     js.src = "//connect.facebook.net/en_US/sdk.js";
     fjs.parentNode.insertBefore(js, fjs);
   }(document, 'script', 'facebook-jssdk'));

   window.fbAsyncInit = function() {
   FB.init({
     appId            : '1388042014582795',
     autoLogAppEvents : true,
     xfbml            : true,
     version          : 'v2.9'
   });
   FB.AppEvents.logPageView();

   FB.api(
        "/1477323589008693?fields=live_views&access_token=EAAaBZCzjU8H8BAFV7KudJn0K1V12CDBHqTIxYu6pVh7cpZAbt1WbZCyZBeSZC472fpPd0ZAkWC1tMrfAY26XnQJUR2rNrMQncQ9OGJlie3dUeQVvabZCwNmGaLL4FGHjZBVTajid16FL5niGWytlwZCiFDgj6yjIsZAAAZD",
       function (response) {
         console.log(response)
         if (response && !response.error) {
           /* handle the result */
           console.log(response);
         }
       }
   );
  };




    // Configurate toolbar handlers
    //config_file_operations("", model.fileExtension(), model.saveFileData, model.loadFileData, model.init);
});
