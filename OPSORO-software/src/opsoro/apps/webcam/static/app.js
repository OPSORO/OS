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

        // Setup websocket connection.
        self.conn = null;
        self.connReady = false;
        self.conn = new SockJS("http://" + window.location.host + "/sockjs");

        self.conn.onopen = function(){
          $.ajax({
            url: "/sockjstoken",
            cache: false
          })
          .done(function(data) {
            self.conn.send(JSON.stringify({action: "authenticate", token: data}));
            self.connReady = true;
          });
        };

        self.conn.onmessage = function(e){
          var msg = $.parseJSON(e.data);
          switch(msg.action){
            case "soundStopped":
              if (self.selectedVoiceLine() != undefined) {
                self.selectedVoiceLine().isPlaying(false);
                self.selectedVoiceLine().hasPlayed(true);
              }
              break;
          }
        };

        self.conn.onclose = function(){
          self.conn = null;
          self.connReady = false;
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

    // Configurate toolbar handlers
    //config_file_operations("", model.fileExtension(), model.saveFileData, model.loadFileData, model.init);
});
