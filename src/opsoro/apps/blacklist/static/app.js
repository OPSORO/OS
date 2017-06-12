(function BlacklistManager(){
		var self = this;
		GlobalDataJSON = [];

		self.templateBan = 'blacklistTemplate';

		self.wordBan = ko.observable();
		self.replacedWord = ko.observable();
		self.bans = ko.observableArray();

		self.addBanItem = function(){
			self.bans.push(new Ban( self.wordBan(), self.replacedWord()));
		};

		self.removeBanItem = function(item){

			self.bans.remove(item);

			var newitems = [];
			var items = GlobalDataJSON;
			var deletedItem = {banWord: item.wordBan(), replacedWord: item.replacedWord()}
			var result = $.grep(items, function(e){
				if (JSON.stringify(e) != JSON.stringify(deletedItem)) {
					newitems.push(e)
				}
			});
			GlobalDataJSON = newitems;
			newitems = JSON.stringify(newitems);
			 $.post('/apps/blacklist/signblacklist', { banlist: newitems }, function(resp) {
			 	console.log('posted to python');
			 });
		};

		// de bestaande objecten inladen en i nde html steken
		self.loadBlacklist = function(){

			$.get('/apps/blacklist/getblacklist', function( data ) {
				if (data != "{}") {
					var json_data = JSON.parse(data);
					GlobalDataJSON = JSON.parse(json_data.banlist);
					console.log(GlobalDataJSON);
					 $.each(JSON.parse(json_data.banlist), function(idx, line){
							self.wordBan(line.banWord);
							self.replacedWord(line.replacedWord);
							self.bans.push(new Ban( self.wordBan(), self.replacedWord()));
					 });
				}
			});
		};


		// als er op de save knop geduwdt word et object opstlaan
		self.saveBannedWord = function(){

			$( "#error_exists").empty();
			self.replacedWord("swear word");

			var exists = false;
			var data_line = {
				banWord : self.wordBan(),
				replacedWord : self.replacedWord()
			};

			ko.toJSON(data_line);
			$.grep(GlobalDataJSON, function(e){
				if (JSON.stringify(e) == JSON.stringify(data_line)) {
					exists = true;
				}
			});
			if (!exists) {
				self.saveJson(data_line);
			}else{
				$("#error_exists").append("<br /><small>Word exists</small>");

			}

		};

		self.saveAll = function(){

			console.log('savig all');
			var newitems = [];
			$.grep(bans(), function(e){
				var data_line = {
					banWord : e.wordBan(),
					replacedWord : e.replacedWord()
				};
				newitems.push(data_line);
			});

			GlobalDataJSON = newitems;
			newitems = JSON.stringify(newitems);
			$.post('/apps/blacklist/signblacklist', { banlist: newitems }, function(resp) {

			});
		};

		// bedoeling op te slaan in de python
		self.saveJson = function(data_line){

			var dataJSON = GlobalDataJSON;
			dataJSON.push(data_line);
			dataJSON = JSON.stringify(dataJSON);
			$.post('/apps/blacklist/signblacklist', { banlist: dataJSON }, function(resp) {
			 	self.addBanItem();
			});
		};

		ko.applyBindings(self.templateBan);

})();

// data binden met de objecten
function Ban(wodBan, replacedWord){
	var self = this;

	self.wordBan = ko.observable(wodBan);
	self.replacedWord = ko.observable(replacedWord);
}
