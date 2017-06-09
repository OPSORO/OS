(function BanManager(){
		var self = this;
		var GlobalDataJSON = "";
		
		self.templateBan = 'blacklistTemplate';

		self.wordBan = ko.observable();
		self.replacedWord = ko.observable("pudding");

		self.bans = ko.observableArray();

		self.addBanItem = function(){
			self.bans.push(new Ban( self.wordBan(), self.replacedWord()));
		};

		self.removeBanItem = function(item){
			self.bans.remove(item);
		};

		// de bestaande objecten inladen en i nde html steken
		self.load = function(){

			var dataobj = JSON.parse(dummy);
			$.each(dataobj.bannedwords, function(idx, line){
			 	self.bans.push(new Ban( line.wordBan, line.replacedWord));

			 });
		};


		// als er op de save knop geduwdt word et object opstlaan
		self.saveBan = function(){
	    console.log('savingBan');
			self.addBanItem();
			localStorage.setItem("stored_bans", ko.toJSON(self.wordBan(), self.replacedWord()));
			// na python
			var data_line = {
				name : self.wordBan(),
				phone : self.replacedWord()
			};
			ko.toJSON(data_line);
			self.saveJson(data_line);
		};

		self.saveAll = function(){
			console.log('savig all');
		}

		// bedoeling op te slaan in de python
		self.saveJson = function(data_line){

			// get data first
			var dataJSON = JSON.parse(dummy);
			dataJSON.bannedwords.push(ko.toJSON(data_line));

			// $.ajax({
		  //   url: '/signcontacts',
		  //   dataType: 'json',
		  //   data: JSON.stringify(dataJSON),
		  //   type: 'POST',
		  //   success: function(response) {
		  //       console.log(response);
		  //   },
		  //   error: function(error) {
		  //       console.log(error);
		  //   }
			// });

		};

		//	ko.cleanNode(self.templateName);
		ko.applyBindings(self.templateBan);

})();

// data binden met de objecten
function Ban(wodBan, replacedWord){
	var self = this;

	self.wordBan = ko.observable(wodBan);
	self.replacedWord = ko.observable(replacedWord);
}
