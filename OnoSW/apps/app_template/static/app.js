$(document).ready(function(){
  var Model = function(){
    var self = this;

    // File operations toolbar item
    self.fileIsModified = ko.observable(false);
    self.fileName = ko.observable("Untitled");
    self.fileStatus = ko.observable("Stopped");

    self.saveFile = function(){
    };
    self.openFile = function(){
    };
    self.newFile = function(){
    };

    // Script operations toolbar item
    self.isRunning = ko.observable(false);
    self.isUI = ko.observable(false);

    // Lock/Unlock toolbar item
    self.fileIsLocked = ko.observable(false);
    self.toggleLocked = function(){
      self.fileIsLocked( !self.fileIsLocked() );
    };

    // Popup window
    self.popupTextInput = ko.observable("Hi! This text can be changed. Click on the button to change me!");
    self.showPopup = function(){
      $("#popup_window").foundation("reveal", "open");
    };
    self.closePopup = function(){
      $("#popup_window").foundation("reveal", "close");
    };
    self.popupButtonHandler = function(){
      self.closePopup();
    };
  };
  // This makes Knockout get to work
  var model = new Model();
  ko.applyBindings(model);
});
