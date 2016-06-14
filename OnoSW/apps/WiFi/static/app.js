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


		self.pressConnect = function(){
			var ssid = $('#ssid-select').val();
    		var password = $('#passwordfield').val();

    		var ssidstyle = document.getElementById("ssid-select").style;
    		var passwordstyle = document.getElementById("passwordfield").style;
			var infostyle = document.getElementById("info").style;

    		if(ssid.length > 0 && password.length > 0){
    			if(password.length > 7){
				    $.ajax({
						dataType: "json",
						data: {"essid":  ssid, "psk": password },
						type: "POST",
						url: "connect",
						success: function(data){
							if(data.status == "error"){
								console.log(data);
							}else{
  								document.cookie = "ssid=" + ssid;
						
							}
						}
					});

			    	//controle

			    	$("#popup_window").foundation("reveal", "open");
			    	
			    	location.reload();

			    		



				}else{
					passwordstyle.border = "solid 1px red";
					infostyle.color = "red";
				}
			}else{
				if(!ssid.length > 0){
					ssidstyle.border = "solid 1px red";
				}
				if(!password.length > 0){
					passwordstyle.border = "solid 1px red";
					
				}
			}

		};

		self.pressRefresh = function(){

		    console.log('refresh');
		    $.ajax({
				dataType: "json",
				/*data: {"phi": self.emotion().emotion.phi, "r": self.emotion().emotion.r},*/
				type: "POST",
				url: "refresh",
				success: function(data){
					if(data.status == "error"){
						console.log(data);
					}else{
						console.log(data);
					}
				}
			});
		    location.reload();

		};


  };

  window.onload = function(){

  	var online = navigator.onLine;
  	if(online){
  		function getCookie(cname) {
    		var name = cname + "=";
    		var ca = document.cookie.split(';');
    		for(var i = 0; i <ca.length; i++) {
       			var c = ca[i];
        		while (c.charAt(0)==' ') {
            		c = c.substring(1);
        	}
        	if (c.indexOf(name) == 0) {
            	return c.substring(name.length,c.length);
        	}
    	}
    		return "";
		}

		$.ajax({
			dataType: "json",
			/*data: {"phi": self.emotion().emotion.phi, "r": self.emotion().emotion.r},*/
			type: "POST",
			url: "ip",
			success: function(data){
				if(data.status == "error"){
					console.log(data);
				}else{
					$.ajax({
						type: "GET",
						url: "/app/WiFi/static/ip"
					}).done(function(ip){
							document.getElementsByClassName('actionbar')[0].innerHTML = "Connected to " + getCookie("ssid") + " with IP: " + ip; 
							console.log(ip);
					});
					
				}
			}
		});
		
		

    		//document.getElementsByClassName('actionbar')[0].innerHTML = "Connected to " + getCookie("ssid") + "with IP: " + ip ;  
  	
  	}else{
  		document.cookie = "ssid=";
  	}

  }

// window.onload = function(){
// 	$.ajax({
// 				dataType: "json",
// 				/*data: {"phi": self.emotion().emotion.phi, "r": self.emotion().emotion.r},*/
// 				type: "GET",
// 				url: "checkwifi",
// 				success: function(data){
// 					if(data.status == "error"){
// 						console.log(data);

// 					}else{
// 						console.log(data);
// 						console.log('tes')

// 	console.log('test');
// 					}
// 				}
// 			});
// }

  						
  
  // This makes Knockout get to work
  var model = new Model();
  ko.applyBindings(model);
	model.fileIsModified(false);

  // Configurate toolbar handlers
  //config_file_operations("", model.fileExtension(), model.saveFileData, model.loadFileData, model.init);



});
