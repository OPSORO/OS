$(document).ready(function() {

    conn = null;
    connReady = false;
    conn = new SockJS('http://' + window.location.host + '/appsockjs');

    conn.onopen = function() {
            console.log("SockJS connected.");
            $.ajax({
                url: "/appsockjstoken",
                cache: false
            }).done(function(data) {
                conn.send(JSON.stringify({
                    action: "authenticate",
                    token: data
                }));
                
                connReady = true;
                console.log("SockJS authenticated.");
            });
    };
    conn.onmessage = function(e) {
        console.log(e.data);
    };   

    conn.onclose = function() {
            console.log("SockJS disconnected.");
            conn = null;
            connReady = false;
    };

    $('#cmdqueue').sortable({
        revert: true,
        placeholder: "highlight command",
        cancel: ".disabled"
    });
    $('#sortable').disableSelection();
    $('.draggable').draggable({
            connectToSortable: "#cmdqueue",
            helper: "clone",
            revert: "invalid"
    });
    $('#cmdqueue').droppable({
      drop: function( event, ui ) {
        $('#cmdqueue-placeholder').find('p').addClass("hidden");
      }
    });

    $('#filters').accordion({
      collapsible: true
    });
    $('#cmdqueue').on('click', '.command', function() {      
        this.parentNode.removeChild(this);
    });

    

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
        /*
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
        */
    };
    // This makes Knockout get to work
    var model = new Model();
    ko.applyBindings(model);
    model.fileIsModified(false);
    
    // Configurate toolbar handlers
    //config_file_operations("", model.fileExtension(), model.saveFileData, model.loadFileData, model.init);
});
