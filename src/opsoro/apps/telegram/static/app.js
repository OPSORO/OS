(function TelegramManager(){

	var GeneralTelegram = function(){

		var self = this;
		var items = 15;

		self.loadLastMessages = function(){

			$.get('/apps/telegram/getLastMessages', function( data ) {
				if (data != "{}") {
					var json_data = data;
					//console.log(GlobalcontactsDataJSON);
					 $.each(json_data.messages, function(idx, line){
						 if (idx < items) {
						 	var date = new Date(line.time*1000);
							var datetime =  date.getDate() + '/' + (date.getMonth()+1) + '/' + date.getFullYear();
							var hours = date.getHours();
							var minutes = "0" + date.getMinutes();
							var seconds = "0" + date.getSeconds();
							var formattedTime = hours + ":" + minutes.substr(-2) + ":" + seconds.substr(-2);

							var name = line.first_name + " " + line.last_name;
								$('#messages').append('<div class="chatbox chatbox_you">'+
									'<div class="bubblebox">'+
										'<span class="chatname">'+name+'</span>'+
										 '<div class="bubble you">'+line.message+'</div>'+
										'<span class="time">'+formattedTime+'</span>'+
									'</div>'+
									'<span class="bubble_head"></span>'+
									'<!--<a href="#" class="repeat"></a>-->'+
								'</div>')
							}
					 });
				 }
			});
		};

		app_socket_handler = function(data) {
			switch (data.action) {
				case "messageIncomming":
        var message = data.message.text;
        var firstname = data.message.from.first_name;
        var lastname = data.message.from.last_name;
				var id = data.message.from.id;
        var timestamp = data.message.date;

				var contactsName, cotnactsLastname;
				var contactsNotExist = true;
				//console.log(message);

				$.get('/apps/telegram/getcontacts', function( data ) {
					if (data != "{}") {
						var json_data = data;
						 $.each(json_data.contacts, function(idx, line){
								contactsName = line.name;
								cotnactsLastname = line.lastname;

								if (contactsName != firstname && cotnactsLastname != lastname ) {
										contactsNotExist = false;
								}
						 });
					 }
				});

				//name
				if (contactsNotExist && message == "/start" ) {

						model.popup().newContact(firstname, lastname, id);
				}else if( message == "/start" ){


					// do nothing
				}else{
					//convert timestamp to readable time and date
	        var date = new Date(timestamp*1000);
	        var datetime =  date.getDate() + '/' + (date.getMonth()+1) + '/' + date.getFullYear();
	        var hours = date.getHours();
	        var minutes = "0" + date.getMinutes();
	        var seconds = "0" + date.getSeconds();
	        var formattedTime = hours + ":" + minutes.substr(-2) + ":" + seconds.substr(-2);

	        var name = firstname + " " + lastname;
	      	//$('#messages').prepend('<div id="message"><p>'+message+'</p><p id="name">'+name+'</p><p id="date">'+datetime+'</p></div>'); // unshifts -> pusht naar eerste element
					// if ("bot" == "robot") {
					// 	console.log("robot");
					// 	$('#messages').prepend('<div class="chatbox chatbox_me">'+
					// 		'<div class="bubblebox">'+
					// 			'<span class="chatname">'+name+'</span>'+
					// 			 '<div class="bubble me">'+message+'</div>'+
					// 			'<span class="time">'+datetime+'</span>'+
					// 		'</div>'+
					// 		'<span class="bubble_head"></span>'+
					// 	'</div>'
					// 	); // unshifts -> pusht naar eerste element
					// }else{
						//console.log("person");
						$('#messages').prepend('<div class="chatbox chatbox_you">'+
							'<div class="bubblebox">'+
								'<span class="chatname">'+name+'</span>'+
								 '<div class="bubble you">'+message+'</div>'+
								'<span class="time">'+formattedTime+'</span>'+
							'</div>'+
							'<span class="bubble_head"></span>'+
							'<!--<a href="#" class="repeat"></a>-->'+
						'</div>'
						); // unshifts -> pusht naar eerste element
					//}
					console.log($('.chatbox').length);
					for( var i=0; i< $('.chatbox').length - items; i++){
					     $('.chatbox').eq(-1).remove();
					}

	      	console.log(data)
				}
      	break;
    	default:
			}

			return;
	}}

	var ContactsTelegram = function(){

		var self = this;
		GlobalcontactsDataJSON = [];

		self.templateContacts = 'contactTemplate';

		self.conName = ko.observable();
		self.lastname = ko.observable();
		self.contacts = ko.observableArray();

		self.addItem = function(){
			self.contacts.push(new Contact(self.conName(), self.lastname()));
			self.reset();
		};

		self.addContactFromMessage = function(name, lastname){

			self.conName(name);
			self.lastname(lastname);

			var data_line = {
				name : self.conName(),
				lastname : self.lastname()
			};
			self.saveJson(data_line);

		}

		//remove item van lijst En in json direct
		self.removeItem = function(item){

			self.contacts.remove(item);

			var newitems = [];
			var items = GlobalcontactsDataJSON;
			var deletedItemName =  item.conName();
			var deletedItemLastname =  item.lastname();
			var result = $.grep(items, function(e){
				console.log(e);

				if ((e.name != deletedItemName) && (e.lastname != deletedItemName)) {
					newitems.push(e)
				}
			});
			GlobalcontactsDataJSON = newitems;
			newitems = JSON.stringify(newitems);
			console.log(newitems);
			 $.post('/apps/telegram/signcontacts', { contacts: newitems }, function(resp) {
			 	console.log('posted to python');
			 });
		};

		// json inladen en in de velden pushen
		self.loadContacts = function(){

			$.get('/apps/telegram/getcontacts', function( data ) {
				if (data != "{}") {
					var json_data = data;
					GlobalcontactsDataJSON = json_data.contacts;
					//console.log(GlobalcontactsDataJSON);
					 $.each(json_data.contacts, function(idx, line){
							self.conName(line.name);
							self.lastname(line.lastname);
							self.contacts.push(new Contact(self.conName(), self.lastname()));
							self.reset();
					 });
				 }
			});
		};

		$('input[type=text]').on('keydown', function(e) {
		    if (e.which == 13) {
		       self.save();
		    }
		});

		self.save = function(){

			$( "#error_contacts").empty();
			if (self.conName().length < 20 && self.lastname().length < 20 ) {

				var data_line = {
			    name : self.conName(),
			    lastname : self.lastname()
				};
				ko.toJSON(data_line);
				self.saveJson(data_line);
			}else{
				$("#error_contacts").append("<br /><small>Data not valid</small>");
			}


		};

		// de json zelf opslaan in de json  en later doorsturen na de pytrhon
		self.saveJson = function(data_line){

			// get data first
			var dataJSON = GlobalcontactsDataJSON;
			dataJSON.push(data_line);
			//console.log(dataJSON);
			dataJSON = JSON.stringify(dataJSON);
			// console.log(dataJSON);
			$.post('/apps/telegram/signcontacts', { contacts: dataJSON }, function(resp) {
				console.log("test");
				self.addItem();
			});

		};

		self.reset = function() {
			self.conName('');
			self.lastname('');
		};

		return self.templateContacts;
	};

	var BlockedTelegram = function(){

		var self = this;
		GlobalBanDataJSON = [];

		//data binden
		self.templateBan = 'banlistTemplate';
		self.banName = ko.observable();
		self.banLastname = ko.observable();
		self.banId = ko.observable();
		self.bans = ko.observableArray();

		self.addBanItem = function(){
			self.bans.push(new Ban( self.banName(), self.banLastname(), self.banId()));
			self.reset();
		};

		self.addBanFromMessage = function(name , lastname, id){

			self.banName(name);
			self.banLastname(lastname);
			self.banId(id);

			var data_line = {
				banName: self.banName(),
				banLastname: self.banLastname(),
				banId: self.banId()
			};
			self.saveJson(data_line);
		};

		self.removeBanItem = function(item){
			self.bans.remove(item);

			var newitems = [];
			var items = GlobalBanDataJSON;
			var deletedItem = item.banId();
			var result = $.grep(items, function(e){

				if ( e.banId != deletedItem) {
					newitems.push(e)
				}
			});
			GlobalBanDataJSON = newitems;
			newitems = JSON.stringify(newitems);
			 $.post('/apps/telegram/signbans', { bans: newitems }, function(resp) {
			 	//console.log('posted to python');
			 });
		};

		// zaken inladen werkt nog niet
		self.loadbans = function(){
			// haven't tested, but probably won't work. I think you'd have to convert your JSON to observables
			$.get( '/apps/telegram/getbans', function( data ) {
				if (data != "{}") {
					var json_data = data;
					GlobalBanDataJSON = json_data.bans;
					 $.each(GlobalBanDataJSON, function(idx, line){
							self.banName(line.banName);
							self.banLastname(line.banLastname);
							self.banId(line.banId);
					  	self.bans.push(new Ban( self.banName(), self.banLastname(), self.banId()));
							self.reset();
					 });
				 }
			});
		};

		// opslaan als er op de save knop gedurk is, het object otevoegen
		self.saveBan = function(){

				var data_line = {
					banName: item.banName(),
					banLastname: item.banLastname(),
					banId: item.banId()
				};
				ko.toJSON(data_line);
				self.saveJson(data_line);
		};

		self.saveJson = function(data_line){

			var dataJSON = GlobalBanDataJSON;
			dataJSON.push(data_line);
			dataJSON = JSON.stringify(dataJSON);
			$.post('/apps/telegram/signbans', { bans: dataJSON }, function(resp) {
				self.addBanItem();
			});

		};

		self.reset = function() {
			self.banName('');
			self.banLastname('');
			self.banId('');
		};

		return self.templateBan;
	};

	// model.popup
	var PopupTelegram = function(){

		var self = this;
		var newName, newLastname, newId;

		self.newContact  = function(name, lastname, id){
		//self.newContact  = function(){

			window.location.href = "/apps/telegram/#modal";

			newName = name;
			newLastname = lastname;
			newId = id;

			var pupupText = "<p>You received a message from "+newName+" "+newLastname+". </p><p>You can either add this person to your Contacts, or you can block this person.</p>";

			$('#modal1Desc').empty();
			$('#modal1Desc').append(pupupText);
		}


		self.addNewContact = function(){

			// $(document).on('opening', '.remodal', function () {
			// 	console.log('opening');
			// });
			//
			// $(document).on('opened', '.remodal', function () {
			// 	console.log('opened');
			// });
			//
			// $(document).on('closing', '.remodal', function (e) {
			// 	console.log('closing' + (e.reason ? ', reason: ' + e.reason : ''));
			// });
			//
			// $(document).on('closed', '.remodal', function (e) {
			// 	console.log('closed' + (e.reason ? ', reason: ' + e.reason : ''));
			// });
			//
			// $(document).on('confirmation', '.remodal', function () {
			// 	//console.log('confirmation');
			// 	model.contacts().addContactFromMessage(newName, newLastname);
			// 	$('#modal1Desc').empty();
			// });
			//
			// $(document).on('cancellation', '.remodal', function () {
			// 	console.log('cancellation');
			// 	model.bans().addBanFromMessage(newName, newLastname, newId)
			// 	$('#modal1Desc').empty();$('#modal1Desc').empty();
			// });

			console.log('confirmation');
			model.contacts().addContactFromMessage(newName, newLastname);
			$('#modal1Desc').empty();
			newName = "";
			newLastname = "";
			newId = "";

		}
		self.addNewBlocked = function(){

			console.log('cancellation');
			model.bans().addBanFromMessage(newName, newLastname, newId)
			$('modal1Desc').empty();$('#modal1Desc').empty();
			newName = "";
			newLastname = "";
			newId = "";
		}

		return;
	}

	var SettignsTelegram = function(){

		var self = this;
		self.api = ko.observable();
		self.APIS = ko.observableArray();

		self.addItem = function(){
			self.APIS.push(new API(self.api()));
		};

		self.loadApiKey = function(){
			// haven't tested, but probably won't work. I think you'd have to convert your JSON to observables
			$.get('/apps/telegram/getsettings', function( data ) {
				if (data != "{}") {
					var json_data = data;
					console.log(data);
					//console.log(GlobalcontactsDataJSON);
					 $.each(json_data.settings, function(idx, line){
							self.api(line);
							self.APIS.push(new API(self.api()));

					 });
				 }
			});
		};

		self.saveApi = function(){
			console.log('saving');
			var data = self.api()
			$.post('/apps/telegram/signsettings', { apiKey: data }, function(resp) {
				self.addItem();
				window.location.href = "/apps/telegram/";
			});
		};

	}

	var TelegramModel = (function(){

		var self = this;
		self.general = ko.observable(new GeneralTelegram());
		self.contacts = ko.observable(new ContactsTelegram());
		self.bans = ko.observable(new BlockedTelegram());
		self.settings = ko.observable(new SettignsTelegram());
		self.popup = ko.observable(new PopupTelegram());
	});

	model = new TelegramModel();
	ko.applyBindings(model);

	addNewContact= function(){
		model.popup().addNewContact();
	}
	addBlockPerson = function(){
		model.popup().addNewBlocked();
	}

	loadingData = function(){

		model.contacts().loadContacts();
		model.bans().loadbans();
		model.settings().loadApiKey()
		model.general().loadLastMessages();
	}

	loadingNew = function(){
		model.popup().newContact();
	}

	function Contact(name, lastname){

		var self = this;
		self.conName = ko.observable(name)
		self.lastname = ko.observable(lastname)
	}

	function Ban(banName, banLastname, banId){

		var self = this;
		self.banName = ko.observable(banName)
		self.banLastname = ko.observable(banLastname)
		self.banId = ko.observable(banId)
	};
	function API(apiKey){

		var self = this;
		self.apikey = ko.observable(apiKey)
	}

})();

// de zaken binden met de waardes
