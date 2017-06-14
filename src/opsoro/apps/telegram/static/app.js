(function TelegramManager(){

	var GeneralTelegram = function(){

		var self = this;
		app_socket_handler = function(data) {
			switch (data.action) {
				case "messageIncomming":
        var message = data.message.text;
        var firstname = data.message.from.first_name;
        var lastname = data.message.from.last_name;
        var timestamp = data.message.date;

        //convert timestamp to readable time and date
        var date = new Date(timestamp*1000);
        var datetime =  date.getDate() + '/' + (date.getMonth()+1) + '/' + date.getFullYear();
        console.log(dateh);
        var hours = date.getHours();
        var minutes = "0" + date.getMinutes();
        var seconds = "0" + date.getSeconds();
        var formattedTime = hours + ":" + minutes.substr(-2) + ":" + seconds.substr(-2);

        var name = firstname + " " + lastname;
      	//$('#messages').prepend('<div id="message"><p>'+message+'</p><p id="name">'+name+'</p><p id="date">'+datetime+'</p></div>'); // unshifts -> pusht naar eerste element
				if ("bot" = "bot") {
					$('#messages').prepend('<div class="chatbox chatbox_me">'+
						'<div class="bubblebox">'+
							'<span class="name">'+name+'</span>'+
							 '<div class="bubble me">'+message+'</div>'+
							'<span class="time">'+datetime+'</span>'+
						'</div>'+
						'<span class="bubble_head"></span>'+
					'</div>'
					); // unshifts -> pusht naar eerste element
				}else{
					$('#messages').prepend($('#messages').prepend('<div class="chatbox chatbox_me">'+
						'<div class="bubblebox">'+
							'<span class="name">'+name+'</span>'+
							 '<div class="bubble me">'+message+'</div>'+
							'<span class="time">'+datetime+'</span>'+
						'</div>'+
						'<span class="bubble_head"></span>'+
					'</div>'
					); // unshifts -> pusht naar eerste element
				}

      	console.log(data)
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
			var deletedItem = {name: item.conName(), lastname: item.lastname()}
			var result = $.grep(items, function(e){
				if (JSON.stringify(e) != JSON.stringify(deletedItem)) {
					newitems.push(e)
				}
			});
			GlobalcontactsDataJSON = newitems;
			newitems = JSON.stringify(newitems);
			 $.post('/apps/telegram/signcontacts', { contacts: newitems }, function(resp) {
			 	console.log('posted to python');
			 });
		};

		// json inladen en in de velden pushen
		self.loadContacts = function(){

			$.get('/apps/telegram/getcontacts', function( data ) {
				if (data != "{}") {
					var json_data = data;
					GlobalcontactsDataJSON = JSON.parse(json_data.contacts);
					//console.log(GlobalcontactsDataJSON);
					 $.each(JSON.parse(json_data.contacts), function(idx, line){
							self.conName(line.name);
							self.lastname(line.lastname);
							self.contacts.push(new Contact(self.conName(), self.lastname()));
							self.reset();
					 });
				 }
			});
		};

		//als er op de save button geklikt word en item laten toeveoegen
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
			console.log(dataJSON);
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
			var deletedItem = {
				banName: item.banName(),
				banLastname: item.banLastname(),
				banId: item.banId()
			}
			var result = $.grep(items, function(e){
				if (JSON.stringify(e) != JSON.stringify(deletedItem)) {
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
					GlobalBanDataJSON = JSON.parse(json_data.bans);
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

	var PopupTelegram = function(){

		self.addNewContact = function(name, lastname, id){

			var pupupText = "<p>tekt voor de naam "+name+" "+lastname+". </p><p>Als je het bericht wilt lezen voeg haar toe bij je contacten of blokeer deze person.</p>";

			$( function() {
			$("#dialog-confirm").append(pupupText);
		    $( "#dialog-confirm" ).dialog({
		      resizable: false,
		      height: "auto",
		      width: 400,
		      modal: true,
		      buttons: {
		        "Add person to contacts": function() {
		          $( this ).dialog( "close" );
							model.contacts().addContactFromMessage(name , lastname);
							$( "#dialog-confirm").empty();
		        },
		        "Block person": function() {
		          $( this ).dialog( "close" );
							model.bans().addBanFromMessage(name , lastname, id);
							$( "#dialog-confirm").empty();
		        }
		      }
		    });
	  	});
		}

		self.newContact  = function(person){
			var name, lastname, id;
			person = '{"messages": [{"maxid": 670008003, "first_name": "Joffrey", "update_id": 670008003, "message": "Hallo"}]}'

			var json_Data = JSON.parse(person).messages;
			name = json_Data[0].first_name;
			lastname = json_Data[0].first_name;
			id = json_Data[0].first_name;
			self.addNewContact(name, lastname, id);
		}

		return self.templatePopup;
	}

	var TelegramModel = (function(){

		var self = this;
		self.general = ko.observable(new GeneralTelegram());
		self.contacts = ko.observable(new ContactsTelegram());
		self.bans = ko.observable(new BlockedTelegram());
		self.popup = ko.observable(new PopupTelegram());

	});

	model = new TelegramModel();
	ko.applyBindings(model);

	loadingData = function(){

		model.contacts().loadContacts();
		model.bans().loadbans();
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

})();

// de zaken binden met de waardes
