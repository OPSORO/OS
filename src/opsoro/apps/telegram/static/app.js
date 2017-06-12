(function TelegramManager(){

	var GeneralTelegram = function(){
		var self = this;

	}
	var ContactsTelegram = function(){

		var self = this;
		GlobalcontactsDataJSON = [];

		self.templateContacts = 'contactTemplate';

		self.conName = ko.observable('');
		self.phone = ko.observable('');
		self.contacts = ko.observableArray();

		self.addItem = function(){
			self.contacts.push(new Contact(self.conName(), self.phone()));
		};

		//remove item van lijst En in json direct
		self.removeItem = function(item){

			self.contacts.remove(item);

			var newitems = [];
			var items = GlobalcontactsDataJSON;
			var deletedItem = {name: item.conName(), phone: item.phone()}
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
				var json_data = JSON.parse(data);
				GlobalcontactsDataJSON = JSON.parse(json_data.contacts);
				//console.log(GlobalcontactsDataJSON);
				 $.each(JSON.parse(json_data.contacts), function(idx, line){
						self.conName(line.name);
						self.phone(line.phone);
						self.contacts.push(new Contact(self.conName(), self.phone()));

				 });
			});
		};

		//als er op de save button geklikt word en item laten toeveoegen
		self.save = function(){

			var data_line = {
		    name : self.conName(),
		    phone : self.phone()
			};
			ko.toJSON(data_line);
			self.saveJson(data_line);
		};

		// de json zelf opslaan in de json  en later doorsturen na de pytrhon
		self.saveJson = function(data_line){

			// get data first
			var dataJSON = GlobalcontactsDataJSON;
			dataJSON.push(data_line);
			dataJSON = JSON.stringify(dataJSON);
			$.post('/apps/telegram/signcontacts', { contacts: dataJSON }, function(resp) {
				self.addItem();
			});

		};
		return self.templateContacts
	};

	var BlockedTelegram = function(){

		var self = this;
		GlobalBanDataJSON = [];

		//data binden
		self.templateBan = 'banlistTemplate';

		self.phoneBan = ko.observable('');
		self.bans = ko.observableArray();

		self.addBanItem = function(){
			console.log(self.phoneBan());
			self.bans.push(new Ban( self.phoneBan().value));
		};

		self.removeBanItem = function(item){
			self.bans.remove(item);

			var newitems = [];
			var items = GlobalBanDataJSON;
			var deletedItem = {phoneBan: item.phoneban()}
			var result = $.grep(items, function(e){
				if (JSON.stringify(e) != JSON.stringify(deletedItem)) {
					newitems.push(e)
				}
			});
			GlobalBanDataJSON = newitems;
			newitems = JSON.stringify(newitems);
			 $.post('/apps/telegram/signbans', { bans: newitems }, function(resp) {
			 //	console.log('posted to python');
			 });
		};

		// zaken inladen werkt nog niet
		self.loadbans = function(){
			// haven't tested, but probably won't work. I think you'd have to convert your JSON to observables
			$.get( '/apps/telegram/getbans', function( data ) {
				var json_data = JSON.parse(data);
				GlobalBanDataJSON = JSON.parse(json_data.bans);
				 $.each(GlobalBanDataJSON, function(idx, line){
					 	self.phoneBan(line.phoneBan+" ");
				  	self.bans.push(new Ban( self.phoneBan()));
				 });
			});
		};

		// opslaan als er op de save knop gedurk is, het object otevoegen
		self.saveBan = function(){

			var data_line = {
		    phoneBan : self.phoneBan(),
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
		return self.templateBan
	};

	var TelegramModel = (function(){

		var self = this;
		self.general = ko.observable(new GeneralTelegram());
		self.contacts = ko.observable(new ContactsTelegram());
		self.bans = ko.observable(new BlockedTelegram());
	});

	model = new TelegramModel();
	ko.applyBindings(model);

	loadingData = function(){

		model.contacts().loadContacts();
		model.bans().loadbans();
	}

	function Contact(name,phone){

		var self = this;
		self.conName = ko.observable(name)
		self.phone = ko.observable(phone)
	};

	function Ban(phoneBan){

		var self = this;
		self.phoneBan = ko.observable(phoneBan);
	};

})();

// de zaken binden met de waardes
