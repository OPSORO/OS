$(document).ready(function(){
  var Model = function(){
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
    self.toggleLocked = function(){
			if (self.fileIsLocked()) {
				self.unlockFile();
			}
			else {
				self.lockFile();
			}
		};
		self.lockFile = function(){
			self.fileIsLocked(true);
			self.fileStatus("Locked")
		};
		self.unlockFile = function(){
			self.fileIsLocked(false);
			self.fileStatus("Editing")
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

    self.init = function(){
      // Clear data, new file, ...
			self.fileName("Untitled");
			self.unlockFile();
			self.fileIsModified(false);
    };

    self.loadFileData = function(filename){
			if (filename == "") {
				//("No filename!");
				return;
			}
			$.ajax({
				dataType: "text",
				type: "POST",
				url: "files/get",
				cache: false,
				data: {path: filename, extension: self.fileExtension()},
				success: function(data){
					// Load data
					var dataobj = JSON.parse(data);

          // Do something with the data

					// Update filename and asterisk
					var filename_no_ext = filename;
					if(filename_no_ext.toLowerCase().slice(-4) == self.fileExtension()){
						filename_no_ext = filename_no_ext.slice(0, -4);
					}
					self.fileName(filename_no_ext);
					self.fileIsModified(false);
					self.lockFile();
				},
				error: function(){
					window.location.href = "?";
				}
			});
		};

		self.saveFileData = function(filename){
			if(filename == ""){
				//("No filename!");
				return;
			}else{
        // Convert data
        file_data = {};
				var data = ko.toJSON(file_data, null, 2);
        // Send data
				$.ajax({
					dataType: "json",
					data: {
						path: filename,
						filedata: data,
						overwrite: 1,
						extension: self.fileExtension()
					},
					type: "POST",
					url: "files/save",
					success: function(data){
						var filename_no_ext = filename;
						if(filename_no_ext.toLowerCase().slice(-4) == self.fileExtension()){
							filename_no_ext = filename_no_ext.slice(0, -4);
						}
						self.fileName(filename_no_ext);
						self.fileIsModified(false);
					}
				});
			}
		};
  };
  // This makes Knockout get to work
  var model = new Model();
  ko.applyBindings(model);
	model.fileIsModified(false);

  // Configurate toolbar handlers
  //config_file_operations("", model.fileExtension(), model.saveFileData, model.loadFileData, model.init);
});
