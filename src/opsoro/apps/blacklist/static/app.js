(function BanManager(){
		var self = this;

		var dummy = JSON.stringify({"bannedwords": [
				{
					"wordBan": "shit",
					"replacedWord": "pudding"
				},
				{
					"wordBan": "fuck",
					"replacedWord": "puddle"
				}
			]});

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

		self.load = function(){

			var dataobj = JSON.parse(dummy);
			$.each(dataobj.bannedwords, function(idx, line){
			 	self.bans.push(new Ban( line.wordBan, line.replacedWord));

			 });
		};


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

function Ban(wodBan, replacedWord){
	var self = this;

	self.wordBan = ko.observable(wodBan);
	self.replacedWord = ko.observable(replacedWord);
}
