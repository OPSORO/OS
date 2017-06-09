(function BanManager(){
		var self = this;
		var GlobalDataJSON = [];

		//data binden
		self.templateBan = 'blacklistTemplate';

		self.phoneBan = ko.observable();

		self.bans = ko.observableArray();

		self.addBanItem = function(){
			self.bans.push(new Ban( self.phoneBan()));
		};

		self.removeBanItem = function(item){
			self.bans.remove(item);
		};

		// zaken inladen werkt nog niet
		self.loadbans = function(){
			// haven't tested, but probably won't work. I think you'd have to convert your JSON to observables
			$.getJSON( '/apps/banned_contacts/getbans', function( data ) {
				var json_data = JSON.parse(data);
				GlobalDataJSON = JSON.parse(json_data.bans);
				console.log(GlobalDataJSON);
				 $.each(GlobalDataJSON, function(idx, line){
					 console.log(GlobalDataJSON);
				  	//self.bans.push(new Ban( self.phoneBan()));
				 });
			});
		};

		// opslaan als er op de save knop gedurk is, het object otevoegen
		self.saveBan = function(){
	    console.log('savingBan');
			self.addBanItem();
			var data_line = {
		    phoneBan : self.phoneBan(),
			};
			ko.toJSON(data_line);
			self.saveJson(data_line);
		};

		self.saveJson = function(data_line){

			// get data first
			var dataJSON = GlobalDataJSON;
			console.log(dataJSON);
			console.log(data_line);
			if (dataJSON != null || dataJSON != "" || dataJSON.length != 0 ) {
				console.log("niet leeg");
				dataJSON.push(data_line);
			}else{
				console.log("leeg");
				dataJSON = data_line;
			}

			//console.log(dataJSON);
			dataJSON = JSON.stringify(dataJSON);
			console.log(dataJSON);

			$.post('/apps/banned_contacts/signbans', { bans: dataJSON }, function(resp) {
				console.log('posted')
			});

		};

		//	ko.cleanNode(self.templateName);
		ko.applyBindings(self.templateBan);

})();


function Ban(phoneBan){
	var self = this;

	self.phoneban = ko.observable(phoneBan);
}
